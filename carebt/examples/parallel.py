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

from carebt import ParallelNode
from carebt.examples.longrun_actions import AddTwoNumbersMultiTickActionWithTimeout


class SimpleParallel(ParallelNode):
    """The `SimpleParallel` example node.

    The `SimpleParallel` node has three child nodes of the same type
    (`AddTwoNumbersMultiTickActionWithTimeout`). With the three input parameters it can be
    controlled how many tick each of the nodes take to complete. The
    `success_threshold` of the `SimpleParallel` node is set to two. That means,
    that the whole node succeeds as soon as two nodes have completed with
    `SUCCESS` or `FIXED` or fails as soon as one of the child nodes complete
    with `FAILURE` or `ABORTED`.

    Input Parameters
    ----------------
    ?ticks1 : int
        The ticks for the first child
    ?ticks2 : int
        The ticks for the second child
    ?ticks3 : int
        The ticks for the third child

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 2, '?ticks1 ?ticks2 ?ticks3')

    def on_init(self) -> None:
        self.add_child(AddTwoNumbersMultiTickActionWithTimeout, '?ticks1 1 1 => ?c1')
        self.add_child(AddTwoNumbersMultiTickActionWithTimeout, '?ticks2 2 2 => ?c2')
        self.add_child(AddTwoNumbersMultiTickActionWithTimeout, '?ticks3 3 3 => ?c3')
