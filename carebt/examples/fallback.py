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

from carebt import FallbackNode
from carebt.examples.sequence_with_contingencies import AddTwoNumbersActionWithFailures


class SimpleFallback(FallbackNode):
    """The `SimpleFallback` example node.

    The `SimpleFallback` has three input parameters and contains three child
    nodes of the same type (`AddTwoNumbersActionWithFailures`). Each of the child
    nodes has the first input parameter fixed and the second one is taken from the
    input of the `SimpleFallback`. This structure allows to provoke a failure in
    each of the child nodes, for example, by setting the input (*?b1 ?b2 ?b3*) to
    a number that the sum of this value and the fixed one is greater than ten.


    Input Parameters
    ----------------
    ?b1 : int
        The first value
    ?b2 : int
        The second value
    ?b3 : int
        The second value

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?b1 ?b2 ?b3')

    def on_init(self) -> None:
        self.append_child(AddTwoNumbersActionWithFailures, '1 ?b1 => ?c1')
        self.append_child(AddTwoNumbersActionWithFailures, '2 ?b2 => ?c2')
        self.append_child(AddTwoNumbersActionWithFailures, '3 ?b3 => ?c3')
