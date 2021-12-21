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

from carebt.rateControlNode import NodeStatus
from carebt.rateControlNode import RateControlNode
from tests.actionNodes import AddTwoNumbersMultiTickAction
from tests.actionNodes import AddTwoNumbersMultiTickActionWithTimeout
from tests.actionNodes import HelloWorldAction
from tests.actionNodes import HelloWorldActionWithMessage
from tests.global_mock import mock

########################################################################


class RateControlledAddTwoNumbersMultiTickAction(RateControlNode):
    """The `RateControlledAddTwoNumbersMultiTickAction` example node.

    The `RateControlledAddTwoNumbersMultiTickAction` throttles down the
    AddTwoNumbersMultiTickAction.
    """

    def __init__(self, bt):
        super().__init__(bt, 250)
        mock('__init__ RateControlledAddTwoNumbersMultiTickAction')

    def on_init(self) -> None:
        mock('on_init RateControlledAddTwoNumbersMultiTickAction')
        self.set_child(AddTwoNumbersMultiTickAction, '5 1 2 => ?result')

    def on_delete(self) -> None:
        mock('on_delete RateControlledAddTwoNumbersMultiTickAction')

    def __del__(self):
        mock('__del__ RateControlledAddTwoNumbersMultiTickAction')

########################################################################


class RateControlledAddTwoNumbersMultiTickActionWithTimeout(RateControlNode):
    """The `RateControlledAddTwoNumbersMultiTickActionWithTimeout` example node.

    The `RateControlledAddTwoNumbersMultiTickActionWithTimeout` throttles down the
    AddTwoNumbersMultiTickActionWithTimeout.
    """

    def __init__(self, bt):
        super().__init__(bt, 400)
        mock('__init__ RateControlledAddTwoNumbersMultiTickActionWithTimeout')

    def on_init(self) -> None:
        mock('on_init RateControlledAddTwoNumbersMultiTickActionWithTimeout')
        self.set_child(AddTwoNumbersMultiTickActionWithTimeout, '5 1 2 => ?result')

    def on_delete(self) -> None:
        mock('on_delete RateControlledAddTwoNumbersMultiTickActionWithTimeout')

    def __del__(self):
        mock('__del__ RateControlledAddTwoNumbersMultiTickActionWithTimeout')

########################################################################


class RateControlledAddTwoNumbersMultiTickActionOwnTimeout(RateControlNode):
    """The `RateControlledAddTwoNumbersMultiTickActionOwnTimeout` example node.

    The `RateControlledAddTwoNumbersMultiTickActionOwnTimeout` throttles down the
    AddTwoNumbersMultiTickAction, but has its own timeout set.
    """

    def __init__(self, bt):
        super().__init__(bt, 250)
        mock('__init__ RateControlledAddTwoNumbersMultiTickActionOwnTimeout')

    def on_init(self) -> None:
        mock('on_init RateControlledAddTwoNumbersMultiTickActionOwnTimeout')
        self.set_child(AddTwoNumbersMultiTickAction, '5 1 2 => ?result')
        self.set_timeout(1000)

    def on_delete(self) -> None:
        mock('on_delete RateControlledAddTwoNumbersMultiTickActionOwnTimeout')

    def on_timeout(self) -> None:
        mock('on_timeout RateControlledAddTwoNumbersMultiTickActionOwnTimeout')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def __del__(self):
        mock('__del__ RateControlledAddTwoNumbersMultiTickActionOwnTimeout')

########################################################################


class RateControlledHelloWorldActionWithMessage(RateControlNode):
    """The `RateControlledHelloWorldActionWithMessage` example node.

    The `RateControlledHelloWorldActionWithMessage` throttles down the
    HelloWorldActionWithMessage. The idea is to test if the contingency-
    message is correctly provided in case the state is `SUCCESS`.
    """

    def __init__(self, bt):
        super().__init__(bt, 250)
        mock('__init__ RateControlledHelloWorldActionWithMessage')

    def on_init(self) -> None:
        mock('on_init RateControlledHelloWorldActionWithMessage')
        self.set_child(HelloWorldActionWithMessage)

    def on_delete(self) -> None:
        mock('on_delete RateControlledHelloWorldActionWithMessage')

    def __del__(self):
        mock('__del__ RateControlledHelloWorldActionWithMessage')

########################################################################


class AsyncAddChildRateControl(RateControlNode):
    """The `AsyncAddChildRateControl` example node.

    The `AsyncAddChildRateControl` starts with an empty child list and adds the
    `HelloWorldAction` child after the timer expires.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 200, '')
        mock('__init__ AsyncAddChildRateControl')

    def on_init(self) -> None:
        mock('on_init AsyncAddChildRateControl')
        Timer(0.5, self.done_callback).start()

    def done_callback(self) -> None:
        mock('AsyncAddChildRateControl: DONE')
        self.set_status(NodeStatus.RUNNING)
        self.set_child(HelloWorldAction)
