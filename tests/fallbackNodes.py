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

from carebt.fallbackNode import FallbackNode
from carebt.nodeStatus import NodeStatus
from tests.actionNodes import AddTwoNumbersActionWithFailure
from tests.actionNodes import AddTwoNumbersLongRunningAction
from tests.actionNodes import HelloWorldAction
from tests.global_mock import mock

########################################################################


class AddTwoNumbersFallback1(FallbackNode):
    """The `AddTwoNumbersFallback1` example node.

    The `AddTwoNumbersFallback1` has two child nodes which both complete with
    `SUCCESS`. The second one should not be executed as the first one already
    succeeds.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback1')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback1')
        self.append_child(AddTwoNumbersActionWithFailure, '2 4 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '3 6 => ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback1')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback1')

########################################################################


class AddTwoNumbersFallback2(FallbackNode):
    """The `AddTwoNumbersFallback2` example node.

    The `AddTwoNumbersFallback2` has two child nodes. The first one fails,
    the second one succeeds. Thus, both should be executed.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback2')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback2')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '3 6 => ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback2')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback2')

########################################################################


class AddTwoNumbersFallback3(FallbackNode):
    """The `AddTwoNumbersFallback3` example node.

    The `AddTwoNumbersFallback3` has four child nodes. The first two fail and the
    following two succeed. Thus, the first three should be executed.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback3')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback3')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '=> ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '2 4 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '3 6 => ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback3')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback3')

########################################################################


class AddTwoNumbersFallback4(FallbackNode):
    """The `AddTwoNumbersFallback4` example node.

    The `AddTwoNumbersFallback4` has two child nodes which both fail. In
    this case the `FallbackSequence` should also fail.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback4')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback4')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '=> ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback4')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback4')

########################################################################


class AddTwoNumbersFallback5(FallbackNode):
    """The `AddTwoNumbersFallback5` example node.

    The `AddTwoNumbersFallback5` is the same as `AddTwoNumbersFallback2`,
    but has a contingency-handler which aborts the `Fallbackode`.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback5')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback5')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '3 6 => ?result')

        self.register_contingency_handler(AddTwoNumbersActionWithFailure,
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.handle_missing_numbers)

    def handle_missing_numbers(self):
        mock('AddTwoNumbersFallback5: handle_missing_numbers')
        self.abort()

    def on_abort(self) -> None:
        mock('on_abort AddTwoNumbersFallback5')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback5')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback5')

########################################################################


class AddTwoNumbersFallback6(FallbackNode):
    """The `AddTwoNumbersFallback6` example node."""

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback6')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback6')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '3 6 => ?result')

        self.register_contingency_handler(AddTwoNumbersActionWithFailure,
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.handle_missing_numbers)

    def handle_missing_numbers(self):
        mock('AddTwoNumbersFallback6: handle_missing_numbers')
        self.remove_all_children()
        self.insert_child_after_current(AddTwoNumbersActionWithFailure, '3 6 => ?result')
        self.insert_child_after_current(HelloWorldAction)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback6')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback6')

########################################################################


class AddTwoNumbersFallback7(FallbackNode):
    """The `AddTwoNumbersFallback7` example node."""

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback7')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback7')
        self.set_timeout(1000)
        self.append_child(AddTwoNumbersLongRunningAction, '2000 2 4 => ?result')
        self.append_child(HelloWorldAction)

    def on_timeout(self) -> None:
        mock('on_timeout AddTwoNumbersFallback7')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def on_abort(self) -> None:
        mock('on_abort AddTwoNumbersFallback7')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback7')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback7')

########################################################################


class AsyncAddChildFallback(FallbackNode):
    """The `AsyncAddChildFallback` example node.

    The `AsyncAddChildFallback` starts with an empty child list and adds the
    `HelloWorldAction` child after the timer expires.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '')
        mock('__init__ AsyncAddChildFallback')

    def on_init(self) -> None:
        mock('on_init AsyncAddChildFallback')
        Timer(0.5, self.done_callback).start()

    def done_callback(self) -> None:
        mock('AsyncAddChildFallback: DONE')
        self.set_status(NodeStatus.RUNNING)
        self.append_child(HelloWorldAction)

########################################################################


class RemoveAllChildrenFallback(FallbackNode):
    """The `RemoveAllChildrenFallback` node.

    The `RemoveAllChildrenFallback` starts with an empty child list and calls
    remove_all_children().
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '')
        mock('__init__ RemoveAllChildrenFallback')

    def on_init(self) -> None:
        mock('on_init RemoveAllChildrenFallback')
        self.remove_all_children()
        self.set_status(NodeStatus.SUCCESS)
