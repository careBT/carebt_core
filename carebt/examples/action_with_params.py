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

from carebt import ActionNode
from carebt import NodeStatus


class AddTwoNumbersAction(ActionNode):
    """The `AddTwoNumbersAction` demonstrates a careBT `ActionNode`.

    The `AddTwoNumbersAction` demonstrates a careBT `ActionNode` with two
    input parameters and one output parameter. It takes the two inputs,
    adds them and returns the result.

    Input Parameters
    ----------------
    ?x : int, default = 0
        The first value
    ?y : int, default = 0
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?x ?y => ?z')

    def on_init(self) -> None:
        if(self._x is None):
            self._x = 0
        if(self._y is None):
            self._y = 0

    def on_tick(self) -> None:
        self._z = self._x + self._y
        print(f'AddTwoNumbersAction: calculating: {self._x} + {self._y} = {self._z}')
        self.set_status(NodeStatus.SUCCESS)
