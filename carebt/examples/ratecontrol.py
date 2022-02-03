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

from carebt import RateControlNode
from carebt.examples.longrun_actions import AddTwoNumbersMultiTickAction


class SimpleRateControl(RateControlNode):
    """The `SimpleRateControl` example node.

    The `SimpleRateControl` has one child. In this example this is the
    `AddTwoNumbersMultiTickAction`. This node has no throttling. Due to
    the `RateControlNode` such a throttling can be implemented without
    changing the original source code of the node. Here, this throttling
    rate is set to 1000 ms.

    Input Parameters
    ----------------
    ?ticks : int
        The number of ticks the calculation takes
    ?a : int
        The first value
    ?b : int
        The second value

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 1000, '?ticks ?a ?b')

    def on_init(self) -> None:
        self.set_child(AddTwoNumbersMultiTickAction, '?ticks ?a ?b => ?result')
