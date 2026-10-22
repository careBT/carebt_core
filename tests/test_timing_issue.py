# Copyright 2021 Andreas Steck (steck.andi@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import threading
from time import sleep
from unittest.mock import patch

import pytest

from carebt.actionNode import ActionNode
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode


class SuspendedActionWithAsyncFailure(ActionNode):
    """Suspends itself and reports a FAILURE from a foreign thread.

    Simulates a real-world scenario where a node is waiting for an async
    operation (e.g., a ROS service call, a network request, a hardware
    response) and the operation fails asynchronously. The foreign thread
    hands over to the careBT execution engine with `create_timer(0, ...)`.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_tick(self) -> None:
        self.set_status(NodeStatus.SUSPENDED)
        self._thread = threading.Thread(target=self._foreign_thread, daemon=True)
        self._thread.start()

    def _foreign_thread(self) -> None:
        sleep(0.02)
        self.create_timer(0, self._on_failure)

    def _on_failure(self) -> None:
        self.set_status(NodeStatus.FAILURE)
        self.set_contingency_message('ASYNC_OPERATION_FAILED')

    def on_delete(self) -> None:
        self._thread.join(timeout=1.0)


class SequenceWithContingencyHandler(SequenceNode):

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_init(self) -> None:
        self.append_child(SuspendedActionWithAsyncFailure)
        self.register_contingency_handler(SuspendedActionWithAsyncFailure,
                                          [NodeStatus.FAILURE],
                                          'ASYNC_OPERATION_FAILED',
                                          self.handle_async_failure)

    def handle_async_failure(self) -> None:
        self.fix_current_child()


class TimeoutVsDoneAction(ActionNode):
    """Has a timeout and a done timer which both expire before the next tick."""

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?timeout ?calctime')
        self.calls = []

    def on_init(self) -> None:
        self.set_timeout(self._timeout)
        self.create_timer(self._calctime, self.done_callback)
        self.set_status(NodeStatus.SUSPENDED)

    def done_callback(self) -> None:
        self.calls.append('done')
        self.set_status(NodeStatus.SUCCESS)

    def on_timeout(self) -> None:
        self.calls.append('timeout')
        self.abort()
        self.set_contingency_message('TIMEOUT')


class LateForeignResultAction(ActionNode):
    """A foreign thread reports the result after the node timed out."""

    release_thread = threading.Event()
    done_called = threading.Event()

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_init(self) -> None:
        self.set_timeout(10)
        self.set_status(NodeStatus.SUSPENDED)
        threading.Thread(target=self._foreign_thread, daemon=True).start()

    def _foreign_thread(self) -> None:
        LateForeignResultAction.release_thread.wait(timeout=2.0)
        self.create_timer(0, self.done_callback)

    def done_callback(self) -> None:
        LateForeignResultAction.done_called.set()
        self.set_status(NodeStatus.SUCCESS)


class IdleActionWithTimeout(ActionNode):
    """Never changes its status and thus remains IDLE."""

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        self.timeout_called = False

    def on_init(self) -> None:
        self.set_timeout(0)

    def on_timeout(self) -> None:
        self.timeout_called = True  # pragma: no cover


class TestTimingIssue:

    def setup_method(self):
        LateForeignResultAction.release_thread.clear()
        LateForeignResultAction.done_called.clear()

    def test_contingency_handler_called_for_async_failure(self):
        """Another thread reports a failure for a SUSPENDED node via
        create_timer(0, ...). The failure is applied on the tick thread
        before the next tick, the parent sequence sees it, and its
        contingency handler fixes it. The tree ends with SUCCESS.
        """
        bt_runner = BehaviorTreeRunner()
        bt_runner.set_tick_rate_ms(5)
        bt_runner.run(SequenceWithContingencyHandler)

        assert bt_runner.get_status() == NodeStatus.SUCCESS

    def test_done_before_timeout(self):
        """The done timer (10 ms) and the timeout (20 ms) both expire before
        the second tick. Due timers fire in deadline order, so done_callback
        runs first and sets SUCCESS, which cancels the timeout. Only 'done'
        is recorded.
        """
        bt_runner = BehaviorTreeRunner()
        bt_runner.initialize(TimeoutVsDoneAction, '20 10')
        bt_runner.tick()
        action = bt_runner._instance._child_ec_list[0].instance
        sleep(0.05)
        assert bt_runner.tick() == NodeStatus.SUCCESS
        assert action.calls == ['done']

    def test_timeout_before_done(self):
        """The reverse case for test_done_before_timeout: timeout at 10 ms,
        done timer at 20 ms. on_timeout aborts the node, and the abort cancels
        all of its timers. The result is ABORTED with message TIMEOUT, and only
        'timeout' is recorded.
        """
        bt_runner = BehaviorTreeRunner()
        bt_runner.initialize(TimeoutVsDoneAction, '10 20')
        bt_runner.tick()
        action = bt_runner._instance._child_ec_list[0].instance
        sleep(0.05)
        assert bt_runner.tick() == NodeStatus.ABORTED
        assert bt_runner.get_contingency_message() == 'TIMEOUT'
        assert action.calls == ['timeout']

    def test_late_foreign_result_is_dropped(self):
        """The node times out and is deleted. Only then does the other thread hand
        over its result. The test runs the scheduler by hand and checks that
        done_callback is never called, because callbacks on a deleted node are
        dropped.
        """
        bt_runner = BehaviorTreeRunner()
        bt_runner.set_tick_rate_ms(5)
        bt_runner.run(LateForeignResultAction)
        assert bt_runner.get_status() == NodeStatus.ABORTED
        assert bt_runner.get_contingency_message() == 'TIMEOUT'

        # the foreign thread hands over after the node was deleted
        LateForeignResultAction.release_thread.set()
        sleep(0.05)
        bt_runner._BehaviorTreeRunner__scheduler.run(blocking=False)
        assert not LateForeignResultAction.done_called.is_set()

    def test_tick_after_completion(self):
        """Calling tick() on a finished tree returns the final status. It does
        not tick the tree again and does not increase the tick count.
        """
        bt_runner = BehaviorTreeRunner()
        bt_runner.initialize(TimeoutVsDoneAction, '1000 0')
        while bt_runner.tick() in (NodeStatus.IDLE, NodeStatus.RUNNING):
            sleep(0.005)
        tick_count = bt_runner.get_tick_count()
        assert bt_runner.tick() == NodeStatus.SUCCESS
        assert bt_runner.get_tick_count() == tick_count

    def test_tick_before_initialize(self):
        """Calling tick() without initialize() raises RuntimeError."""
        bt_runner = BehaviorTreeRunner()
        with pytest.raises(RuntimeError):
            bt_runner.tick()

    def test_initialize_cancels_pending_timers(self):
        """A runner-level timer created before initialize() is cancelled by
        initialize(), so the next tick doesn't fire it. Timers can't leak from
        one run into the next.
        """
        bt_runner = BehaviorTreeRunner()
        called = []
        bt_runner.create_timer(0, lambda: called.append(True))
        bt_runner.initialize(TimeoutVsDoneAction, '1000 0')
        bt_runner.tick()
        assert called == []

    def test_timer_cancel(self):
        """Covers the basic CareBTTimer behaviour:
        - a cancelled timer never fires;
        - cancelling twice is safe;
        - is_active() is False after cancelling and after firing;
        - cancelling a timer that already fired is safe.
        """
        bt_runner = BehaviorTreeRunner()
        called = []
        timer1 = bt_runner.create_timer(0, lambda: called.append(1))
        timer2 = bt_runner.create_timer(0, lambda: called.append(2))
        assert timer1.is_active()
        timer2.cancel()
        timer2.cancel()
        assert not timer2.is_active()
        bt_runner._BehaviorTreeRunner__scheduler.run(blocking=False)
        assert called == [1]
        assert not timer1.is_active()
        timer1.cancel()

    def test_timer_cancel_after_initialize(self):
        """Canceling a timer which was dropped by initialize must not fail."""
        bt_runner = BehaviorTreeRunner()
        timer = bt_runner.create_timer(1000, lambda: None)
        bt_runner.initialize(TimeoutVsDoneAction, '1000 0')
        timer.cancel()
        assert not timer.is_active()

    def test_timeout_ignored_while_idle(self):
        """A timeout must only call on_timeout if the node is RUNNING or SUSPENDED."""
        bt_runner = BehaviorTreeRunner()
        bt_runner.initialize(IdleActionWithTimeout)
        for _ in range(3):
            bt_runner.tick()
            sleep(0.005)
        action = bt_runner._instance._child_ec_list[0].instance
        assert action.get_status() == NodeStatus.IDLE
        assert not action.timeout_called


def _run_in_thread(function) -> None:
    thread = threading.Thread(target=function)
    thread.start()
    thread.join()


def _thread_warnings(warn) -> list:
    return [c.args[0] for c in warn.call_args_list if 'another thread' in c.args[0]]


class TestThreadCheck:

    def setup_method(self):
        self.bt_runner = BehaviorTreeRunner()
        self.bt_runner.initialize(TimeoutVsDoneAction, '1000 1000')

    def test_set_status_from_other_thread_warns(self):
        """After the first tick, set_status from another thread logs exactly one
        warning that names TimeoutVsDoneAction.set_status.
        """
        self.bt_runner.tick()
        action = self.bt_runner._instance._child_ec_list[0].instance
        with patch.object(self.bt_runner.get_logger(), 'warn') as warn:
            _run_in_thread(lambda: action.set_status(NodeStatus.SUCCESS))
        assert len(_thread_warnings(warn)) == 1
        assert 'TimeoutVsDoneAction.set_status' in _thread_warnings(warn)[0]

    def test_set_contingency_message_from_other_thread_warns(self):
        """The same check as test_set_status_from_other_thread_warns
        for set_contingency_message.
        """
        self.bt_runner.tick()
        action = self.bt_runner._instance._child_ec_list[0].instance
        with patch.object(self.bt_runner.get_logger(), 'warn') as warn:
            _run_in_thread(lambda: action.set_contingency_message('MSG'))
        assert len(_thread_warnings(warn)) == 1
        assert 'TimeoutVsDoneAction.set_contingency_message' in _thread_warnings(warn)[0]

    def test_tick_from_other_thread_warns(self):
        """After the first tick on the main thread, a tick() from another thread
        logs a BehaviorTreeRunner.tick warning.
        """
        self.bt_runner.tick()
        with patch.object(self.bt_runner.get_logger(), 'warn') as warn:
            _run_in_thread(self.bt_runner.tick)
        assert any('BehaviorTreeRunner.tick' in w for w in _thread_warnings(warn))
