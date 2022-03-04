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

import random

from carebt import ActionNode
from carebt import NodeStatus
from carebt import SequenceNode
from carebt.examples.action_with_params import AddTwoNumbersAction


########################################################################


class CreateRandomNumberAction(ActionNode):
    """The `CreateRandomNumberAction` example node.

    The `CreateRandomNumberAction` creates a random number between 1 and 10
    and binds it to the output parameter.

    Output Parameters
    -----------------
    ?number : int
        The randomly generated number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '=> ?number')

    def on_tick(self) -> None:
        self._number = random.randint(1, 10)
        print(f'CreateRandomNumberAction: number = {self._number}')
        self.set_status(NodeStatus.SUCCESS)

########################################################################


class PrintNumberAction(ActionNode):
    """The `PrintNumberAction` example node.

    The `PrintNumberAction` prints the, as input parameter provided, number on
    standard output.

    Input Parameters
    ----------------
    ?number : int
        The number to print

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?number')

    def on_tick(self) -> None:
        print(f'PrintNumberAction: number = {self._number}')
        self.set_status(NodeStatus.SUCCESS)

########################################################################


class SimpleSequence1(SequenceNode):
    """The `SimpleSequence1` example node.

    The `SimpleSequence` runs the nodes `CreateRandomNumberAction`,
    `CreateRandomNumberAction`, `AddTwoNumbersAction` and `PrintNumberAction`
    in a sequence. The first two nodes create random numbers, the third one
    adds them together and the last one prints the result. Furthermore, the
    result is returned by the ouput parameter *?c*.

    Output Parameters
    -----------------
    ?c : int
        The result

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '=> ?c')

    def on_init(self) -> None:
        self.append_child(CreateRandomNumberAction, '=> ?a')
        self.append_child(CreateRandomNumberAction, '=> ?b')
        self.append_child(AddTwoNumbersAction, '?a ?b => ?c')
        self.append_child(PrintNumberAction, '?c')

########################################################################


class SimpleSequence2(SequenceNode):
    """The `SimpleSequence2` example node.

    The `SimpleSequence2` demonstrates a modified version of the
    `SimpleSequence1`. The value provided as an input parameter is
    added to a randomly generated value. The result is then added
    to another randomly generated value. This final result is then
    provided as an output of the `SequenceNode`.

    Input Parameters
    ----------------
    ?a : int
        A number for the calculations

    Output Parameters
    -----------------
    ?e : int
        The result

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a => ?e')

    def on_init(self) -> None:
        self.append_child(CreateRandomNumberAction, '=> ?b')
        self.append_child(AddTwoNumbersAction, '?a ?b => ?c')
        self.append_child(PrintNumberAction, '?c')
        self.append_child(CreateRandomNumberAction, '=> ?d')
        self.append_child(AddTwoNumbersAction, '?c ?d => ?e')
        self.append_child(PrintNumberAction, '?e')

########################################################################


class SimpleSequence3(SequenceNode):
    """The `SimpleSequence3` example node.

    The `SimpleSequence3` shows another example sequence where the two sequences
    implemented above are reused.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_init(self) -> None:
        self.append_child(SimpleSequence1, '=> ?x')
        self.append_child(PrintNumberAction, '?x')
        self.append_child(SimpleSequence2, '?x => ?y')
        self.append_child(PrintNumberAction, '?y')
