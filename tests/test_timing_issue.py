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

from carebt.actionNode import ActionNode
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode


_contingency_checked_event = threading.Event()
_callback_done_event = threading.Event()


class SuspendedActionWithAsyncFailure(ActionNode):
    """An action node that suspends itself and has an async callback that
    sets it to FAILURE.

    Simulates a real-world scenario where a node is waiting for an async
    operation (e.g., a ROS service call, a network request, a hardware
    response) and the operation fails asynchronously.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_init(self):
        self._tick_count = 0

    def on_tick(self) -> None:
        self._tick_count += 1
        if self._tick_count == 1:
            # start the async operation and suspend
            self.set_status(NodeStatus.SUSPENDED)
            self._callback_thread = threading.Thread(
                target=self._async_failure_callback, daemon=True)
            self._callback_thread.start()

    def _async_failure_callback(self):
        # wait for contingency checked event
        _contingency_checked_event.wait(timeout=5.0)
        self.set_status(NodeStatus.FAILURE)
        self.set_contingency_message('ASYNC_OPERATION_FAILED')
        _callback_done_event.set()

    def on_delete(self) -> None:
        if hasattr(self, '_callback_thread') and self._callback_thread.is_alive():
            self._callback_thread.join(timeout=1.0)


class SequenceWithContingencyHandler(SequenceNode):
    """A sequence that registers a contingency handler for the FAILURE case.

    The contingency handler should fix the failure.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_init(self) -> None:
        self.append_child(SuspendedActionWithAsyncFailure)
        
        self.register_contingency_handler(
            SuspendedActionWithAsyncFailure,
            [NodeStatus.FAILURE],
            '.*',
            self.handle_async_failure
        )

    def on_tick(self) -> None:
        child_instance = self._child_ec_list[self._child_ptr].instance
        if child_instance is not None and child_instance.get_status() == NodeStatus.SUSPENDED:
            # Signal the callback thread to attempt set_status.
            _contingency_checked_event.set()
            # Wait for the callback to actually complete before proceeding with the tick.
            _callback_done_event.wait(timeout=0.05)

    def handle_async_failure(self) -> None:
        self.fix_current_child()


class TestTimingIssue:

    def setup_method(self):
        """Reset synchronization events before each test."""
        _contingency_checked_event.clear()
        _callback_done_event.clear()

    def test_contingency_handler_called_for_async_failure(self):
        """The contingency handler MUST be called when an async callback
        sets a SUSPENDED node to FAILURE.
        """
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithContingencyHandler)

        assert bt_runner.get_status() == NodeStatus.SUCCESS