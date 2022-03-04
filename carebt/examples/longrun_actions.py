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

from carebt import ActionNode
from carebt import NodeStatus


class AddTwoNumbersMultiTickAction(ActionNode):
    """The `AddTwoNumbersMultiTickAction` example node.

    The `AddTwoNumbersMultiTickAction` demonstrates how it looks like when a
    `ActionNode` requires more ticks to complete. To make things simple the
    amount of ticks required to complete the action is provided as input
    parameter.

    Input Parameters
    ----------------
    ?ticks : int
        Number of ticks requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?ticks ?x ?y => ?z')

    def on_init(self) -> None:
        self._tick_count = 1

    def on_tick(self) -> None:
        if(self._tick_count < self._ticks):
            print(f'AddTwoNumbersMultiTickAction: (tick_count = '
                  + f'{self._tick_count}/{self._ticks})')
            self._tick_count += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            self._z = self._x + self._y
            print(f'AddTwoNumbersMultiTickAction: DONE {self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)

########################################################################


class AddTwoNumbersMultiTickActionWithTimeout(ActionNode):
    """The `AddTwoNumbersMultiTickActionWithTimeout` example node.

    The `AddTwoNumbersMultiTickActionWithTimeout` adds a timeout to the
    `AddTwoNumbersMultiTickAction`.

    Input Parameters
    ----------------
    ?ticks : int
        Number of ticks requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?ticks ?x ?y => ?z')

    def on_init(self) -> None:
        self._tick_count = 1
        # without throttling / with timeout
        self.set_timeout(500)
        # with throttling and timeout
        # self.set_throttle_ms(1000)
        # self.set_timeout(5000)

    def on_tick(self) -> None:
        if(self._tick_count < self._ticks):
            print(f'AddTwoNumbersMultiTickActionWithTimeout: (tick_count = '
                  + f'{self._tick_count}/{self._ticks})')
            self._tick_count += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            self._z = self._x + self._y
            print(f'AddTwoNumbersMultiTickActionWithTimeout: '
                  + f'DONE {self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)

    def on_timeout(self) -> None:
        print('AddTwoNumbersMultiTickActionWithTimeout: on_timeout')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def on_abort(self) -> None:
        print('AddTwoNumbersMultiTickActionWithTimeout: on_abort')

########################################################################


class AddTwoNumbersLongRunningAction(ActionNode):
    """The `AddTwoNumbersLongRunningAction` example node.

    The `AddTwoNumbersLongRunningAction` demonstrates how it looks like when a
    `ActionNode` executes an asynchronous function. To make things simple the
    asynchronous function is implemented with a simple Python timer and
    the amount of milliseconds the asynchronous function requires to complete
    is provided as input parameter.

    Input Parameters
    ----------------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?x ?y => ?z')

    def on_init(self) -> None:
        print(f'AddTwoNumbersLongRunningAction: calculating {self._calctime} ms ...')
        self.set_status(NodeStatus.SUSPENDED)
        Timer(self._calctime / 1000, self.done_callback).start()

    def on_tick(self) -> None:
        print('AddTwoNumbersLongRunningAction: on_tick')

    def done_callback(self) -> None:
        self._z = self._x + self._y
        print(f'AddTwoNumbersLongRunningAction: DONE {self._x} + {self._y} = {self._z}')
        self.set_status(NodeStatus.SUCCESS)
