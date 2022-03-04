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

from threading import Timer

from carebt.nodeStatus import NodeStatus
from carebt.parallelNode import ParallelNode
from tests.actionNodes import AddTwoNumbersAction
from tests.actionNodes import FailOnCountAction
from tests.actionNodes import HelloWorldAction
from tests.actionNodes import TickCountingAction
from tests.global_mock import mock

########################################################################


class AddTwoNumbersParallel(ParallelNode):
    """The `AddTwoNumbersParallel` example node.

    The `AddTwoNumbersParallel` runs three `AddTwoNumbersAction` in parallel.
    As the success_threshold is set to 3, the `AddTwoNumbersParallel` completes
    also with `SUCCESS`.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 3, '')
        mock('__init__ AddTwoNumbersParallel')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersParallel')
        self.add_child(AddTwoNumbersAction, '1 2 => ?a')
        self.add_child(AddTwoNumbersAction, '2 3 => ?b')
        self.add_child(AddTwoNumbersAction, '3 4 => ?c')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersParallel')

    def __del__(self):
        mock('__del__ AddTwoNumbersParallel')

########################################################################


class TickCountingParallel(ParallelNode):
    """The `TickCountingParallel` example node.

    The `TickCountingParallel` runs three `TickCountingAction` in parallel.

    Input Parameters
    ----------------
    ?success_threshold: int
        The success_threshold
    ?g1: int
        The goal of child 1
    ?s1: int
        Wether child 1 should succeed or fail
    ?g2: int
        The goal of child 1
    ?s2: int
        Wether child 1 should succeed or fail
    ?g3: int
        The goal of child 1
    ?s3: int
        Wether child 1 should succeed or fail

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, None, '?success_threshold ?g1 ?s1 ?g2 ?s2 ?g3 ?s3')
        mock('__init__ TickCountingParallel')

    def on_init(self) -> None:
        mock(f'on_init TickCountingParallel success_threshold = {self.get_success_threshold()}')
        self.set_success_threshold(self._success_threshold)
        self.add_child(TickCountingAction, '1 ?g1 ?s1 => ?cnt1')
        self.add_child(TickCountingAction, '2 ?g2 ?s2 => ?cnt2')
        self.add_child(TickCountingAction, '3 ?g3 ?s3 => ?cnt3')

    def on_delete(self) -> None:
        mock('on_delete TickCountingParallel')

    def __del__(self):
        mock('__del__ TickCountingParallel')

########################################################################


class TickCountingParallelWithAbort(ParallelNode):
    """The `TickCountingParallelWithAbort` example node.

    The `TickCountingParallelWithAbort` is a variant of `TickCountingParallel`
    which aborts on failure.

    Input Parameters
    ----------------
    ?success_threshold: int
        The success_threshold
    ?g1: int
        The goal of child 1
    ?s1: int
        Wether child 1 should succeed or fail
    ?g2: int
        The goal of child 1
    ?s2: int
        Wether child 1 should succeed or fail
    ?g3: int
        The goal of child 1
    ?s3: int
        Wether child 1 should succeed or fail

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, None, '?success_threshold ?g1 ?s1 ?g2 ?s2 ?g3 ?s3')
        mock('__init__ TickCountingParallelWithAbort')

    def on_init(self) -> None:
        mock('on_init TickCountingParallelWithAbort success_threshold = '
             + f'{self.get_success_threshold()}')
        self.set_success_threshold(self._success_threshold)
        self.add_child(TickCountingAction, '1 ?g1 ?s1 => ?cnt1')
        self.add_child(TickCountingAction, '2 ?g2 ?s2 => ?cnt2')
        self.add_child(TickCountingAction, '3 ?g3 ?s3 => ?cnt3')

        self.register_contingency_handler(TickCountingAction,
                                          [NodeStatus.FAILURE],
                                          'COUNTING_ERROR',
                                          self.handle_error)

    def handle_error(self) -> None:
        self.abort()
        self.set_contingency_message('ANOTHER_COUNTING_ERROR')

    def on_delete(self) -> None:
        mock('on_delete TickCountingParallelWithAbort')

    def __del__(self):
        mock('__del__ TickCountingParallelWithAbort')

########################################################################


class TickCountingParallelDelAdd1(ParallelNode):
    """The `TickCountingParallelDelAdd1` example node.

    The `TickCountingParallelDelAdd1` is a variant of `TickCountingParallel`
    which deletes child 2 (id=3) and adds one new child on failure.

    Input Parameters
    ----------------
    ?success_threshold: int
        The success_threshold
    ?g1: int
        The goal of child 1
    ?s1: int
        Wether child 1 should succeed or fail
    ?g2: int
        The goal of child 1
    ?s2: int
        Wether child 1 should succeed or fail
    ?g3: int
        The goal of child 1
    ?s3: int
        Wether child 1 should succeed or fail

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, None, '?success_threshold ?g1 ?s1 ?g2 ?s2 ?g3 ?s3')
        mock('__init__ TickCountingParallelDelAdd1')

    def on_init(self) -> None:
        mock('on_init TickCountingParallelDelAdd1 success_threshold = '
             + f'{self.get_success_threshold()}')
        self.set_success_threshold(self._success_threshold)
        self.add_child(TickCountingAction, '1 ?g1 ?s1 => ?cnt1')
        self.add_child(TickCountingAction, '2 ?g2 ?s2 => ?cnt2')
        self.add_child(TickCountingAction, '3 ?g3 ?s3 => ?cnt3')

        self.register_contingency_handler(TickCountingAction,
                                          [NodeStatus.FAILURE],
                                          'COUNTING_ERROR',
                                          self.handle_error)

    def handle_error(self) -> None:
        self.remove_child(2)
        self.add_child(TickCountingAction, '4 3 True => ?cnt4')
        self.set_success_threshold(2)

    def on_delete(self) -> None:
        mock('on_delete TickCountingParallelDelAdd1')

    def __del__(self):
        mock('__del__ TickCountingParallelDelAdd1')

########################################################################


class TickCountingParallelDelAdd2(ParallelNode):
    """The `TickCountingParallelDelAdd2` example node.

    The `TickCountingParallelDelAdd2` is a variant of `TickCountingParallel`
    which deletes child 2 (id=3) and adds two new children on failure.

    Input Parameters
    ----------------
    ?success_threshold: int
        The success_threshold
    ?g1: int
        The goal of child 1
    ?s1: int
        Wether child 1 should succeed or fail
    ?g2: int
        The goal of child 1
    ?s2: int
        Wether child 1 should succeed or fail
    ?g3: int
        The goal of child 1
    ?s3: int
        Wether child 1 should succeed or fail

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, None, '?success_threshold ?g1 ?s1 ?g2 ?s2 ?g3 ?s3')
        mock('__init__ TickCountingParallelDelAdd2')

    def on_init(self) -> None:
        mock('on_init TickCountingParallelDelAdd2 success_threshold = '
             + f'{self.get_success_threshold()}')
        self.set_success_threshold(self._success_threshold)
        self.add_child(TickCountingAction, '1 ?g1 ?s1 => ?cnt1')
        self.add_child(TickCountingAction, '2 ?g2 ?s2 => ?cnt2')
        self.add_child(TickCountingAction, '3 ?g3 ?s3 => ?cnt3')

        self.register_contingency_handler(TickCountingAction,
                                          [NodeStatus.FAILURE],
                                          'COUNTING_ERROR',
                                          self.handle_error)

    def handle_error(self) -> None:
        self.remove_child(2)
        self.add_child(TickCountingAction, '4 3 True => ?cnt4')
        self.add_child(TickCountingAction, '5 5 True => ?cnt5')
        self.set_success_threshold(3)

    def on_delete(self) -> None:
        mock('on_delete TickCountingParallelDelAdd2')

    def __del__(self):
        mock('__del__ TickCountingParallelDelAdd2')

########################################################################


class TickCountingParallelDel(ParallelNode):
    """The `TickCountingParallelWithAbort` example node.

    The `TickCountingParallelWithAbort` is a variant of `TickCountingParallel`
    which deletes child 2 (id=3) on failure.

    Input Parameters
    ----------------
    ?success_threshold: int
        The success_threshold
    ?g1: int
        The goal of child 1
    ?s1: int
        Wether child 1 should succeed or fail
    ?g2: int
        The goal of child 1
    ?s2: int
        Wether child 1 should succeed or fail
    ?g3: int
        The goal of child 1
    ?s3: int
        Wether child 1 should succeed or fail

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, None, '?success_threshold ?g1 ?s1 ?g2 ?s2 ?g3 ?s3')
        mock('__init__ TickCountingParallelDel')

    def on_init(self) -> None:
        mock('on_init TickCountingParallelDel success_threshold = '
             + f'{self.get_success_threshold()}')
        self.set_success_threshold(self._success_threshold)
        self.add_child(TickCountingAction, '1 ?g1 ?s1 => ?cnt1')
        self.add_child(TickCountingAction, '2 ?g2 ?s2 => ?cnt2')
        self.add_child(TickCountingAction, '3 ?g3 ?s3 => ?cnt3')

        self.register_contingency_handler(TickCountingAction,
                                          [NodeStatus.FAILURE],
                                          'COUNTING_ERROR',
                                          self.handle_error)

    def handle_error(self) -> None:
        self.remove_child(2)
        self.set_success_threshold(1)

    def on_delete(self) -> None:
        mock('on_delete TickCountingParallelDel')

    def __del__(self):
        mock('__del__ TickCountingParallelDel')

########################################################################


class TickCountingParallelDelAllAdd(ParallelNode):
    """The `TickCountingParallelDelAllAdd` example node.

    The `TickCountingParallelDelAllAdd` is a variant of `TickCountingParallel`
    which deletes all children and adds three new children on failure.

    Input Parameters
    ----------------
    ?success_threshold: int
        The success_threshold
    ?g1: int
        The goal of child 1
    ?s1: int
        Wether child 1 should succeed or fail
    ?g2: int
        The goal of child 1
    ?s2: int
        Wether child 1 should succeed or fail
    ?g3: int
        The goal of child 1
    ?s3: int
        Wether child 1 should succeed or fail

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, None, '?success_threshold ?g1 ?s1 ?g2 ?s2 ?g3 ?s3')
        mock('__init__ TickCountingParallelDelAllAdd')

    def on_init(self) -> None:
        mock('on_init TickCountingParallelDelAllAdd success_threshold = '
             + f'{self.get_success_threshold()}')
        self.set_success_threshold(self._success_threshold)
        self.add_child(TickCountingAction, '1 ?g1 ?s1 => ?cnt1')
        self.add_child(TickCountingAction, '2 ?g2 ?s2 => ?cnt2')
        self.add_child(TickCountingAction, '3 ?g3 ?s3 => ?cnt3')

        self.register_contingency_handler(TickCountingAction,
                                          [NodeStatus.FAILURE],
                                          'COUNTING_ERROR',
                                          self.handle_error)

    def handle_error(self) -> None:
        self.remove_all_children()
        self.add_child(TickCountingAction, '4 3 True => ?cnt4')
        self.add_child(TickCountingAction, '5 5 True => ?cnt5')
        self.add_child(TickCountingAction, '6 6 True => ?cnt6')
        self.set_success_threshold(3)

    def on_delete(self) -> None:
        mock('on_delete TickCountingParallelDelAllAdd')

    def __del__(self):
        mock('__del__ TickCountingParallelDelAllAdd')

########################################################################


class CountAbortParallel(ParallelNode):
    """The `CountAbortParallel` example node.

    The `CountAbortParallel` runs one child that increments the ?count and
    a second one to check the ?count and fails if ?goal is reached. Thus,
    thue whole `ParallelNode` fails.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 2, '')
        mock('__init__ CountAbortParallel')

    def on_init(self) -> None:
        mock('on_init CountAbortParallel')
        self.add_child(TickCountingAction, '1 99 True => ?cnt')
        self.add_child(FailOnCountAction, '5 ?cnt')

    def on_delete(self) -> None:
        mock('on_delete CountAbortParallel')

    def __del__(self):
        mock('__del__ CountAbortParallel')

########################################################################


class CountAbortParallelWithTick(ParallelNode):
    """The `CountAbortParallelWithTick` example node.

    The `CountAbortParallelWithTick` is the same one as the `CountAbortParallel` but
    with the `on_tick` function callback implemented and a throttling rate of 200ms.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 2, '')
        self.set_throttle_ms(200)
        mock('__init__ CountAbortParallelWithTick')

    def on_init(self) -> None:
        mock('on_init CountAbortParallelWithTick')
        self.add_child(TickCountingAction, '1 99 True => ?cnt')
        self.add_child(FailOnCountAction, '5 ?cnt')

    def on_tick(self) -> None:
        mock('on_tick CountAbortParallelWithTick')

    def on_delete(self) -> None:
        mock('on_delete CountAbortParallelWithTick')

    def __del__(self):
        mock('__del__ CountAbortParallelWithTick')

########################################################################


class ParallelRemoveSuccess(ParallelNode):
    """The `ParallelRemoveSuccess` example node."""

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 2, '')
        mock('__init__ ParallelRemoveSuccess')

    def on_init(self) -> None:
        mock('on_init ParallelRemoveSuccess')
        self.add_child(TickCountingAction, '1 2 True => ?cnt')
        self.add_child(TickCountingAction, '2 4 False => ?cnt')
        self.add_child(TickCountingAction, '3 6 True => ?cnt')
        self.add_child(TickCountingAction, '4 8 True => ?cnt')
        self.add_child(TickCountingAction, '5 99 True => ?cnt')

        self.register_contingency_handler(TickCountingAction,
                                          [NodeStatus.FAILURE],
                                          'COUNTING_ERROR',
                                          self.handle_error)

    def handle_error(self) -> None:
        self.remove_child(0)

    def on_delete(self) -> None:
        mock('on_delete ParallelRemoveSuccess')

    def __del__(self):
        mock('__del__ ParallelRemoveSuccess')

########################################################################


class AsyncAddChildParallel(ParallelNode):
    """The `AsyncAddChildParallel` example node.

    The `AsyncAddChildParallel` starts with an empty child list and adds the
    `HelloWorldAction` child after the timer expires.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 2, '')
        mock('__init__ AsyncAddChildParallel')

    def on_init(self) -> None:
        mock('on_init AsyncAddChildParallel')
        Timer(0.5, self.done_callback).start()

    def done_callback(self) -> None:
        mock('AsyncAddChildParallel: DONE')
        self.set_status(NodeStatus.RUNNING)
        self.add_child(HelloWorldAction)
        self.add_child(HelloWorldAction)
