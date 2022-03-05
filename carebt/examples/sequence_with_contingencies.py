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
from carebt import ContingencyHistoryEntry
from carebt import NodeStatus
from carebt import SequenceNode
from carebt.examples.simple_sequence import CreateRandomNumberAction
from carebt.examples.simple_sequence import PrintNumberAction


class AddTwoNumbersActionWithFailures(ActionNode):
    """The `AddTwoNumbersActionWithFailures` example node.

    The `AddTwoNumbersActionWithFailures` demonstrates a careBT `ActionNode`
    with two input parameters and one output parameter. It takes the two inputs,
    adds them and returns the result. Furthermore, this node can complete with
    `FAILURE`. This happend in case that one or both input parameters are missing
    or that the result of the sum is greater than ten.

    Input Parameters
    ----------------
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    Contingencies
    -------------
    FAILURE:
        ONE_PARAM_MISSING
            One input parameter is missing.

        BOTH_PARAMS_MISSING
            Both input parameters are missing.

        RESULT_TOO_LARGE
            The result is greater than 10.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?x ?y => ?z')

    def on_init(self) -> None:
        if(self._x is None and self._y is None):
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('BOTH_PARAMS_MISSING')
        elif(self._y is None):
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('ONE_PARAM_MISSING')

    def on_tick(self) -> None:
        self._z = self._x + self._y
        if(self._z > 10):
            print(f'AddTwoNumbersActionWithFailures: calculating: '
                  + f'{self._x} + {self._y} = {self._z} -> RESULT_TOO_LARGE')
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('RESULT_TOO_LARGE')
        else:
            print(f'AddTwoNumbersActionWithFailures: calculating: '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)

########################################################################


class SimpleSequence(SequenceNode):
    """The `SimpleSequence` example node.

    The `SimpleSequence` shows what happens if a child node in the sequence fails.
    The used `AddTwoNumbersActionWithFailures` can fail in case that one or both
    input parameters are missing or that the result of the sum is greater than ten.
    These contingencies are not handled, and thus forwarded to the `SequenceNode`
    and finally to the `bt_runner`.

    Input Parameters
    ----------------
    ?a : int
        The first value
    ?b : int
        The second value

    Output Parameters
    -----------------
    ?c : int
        The result

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')

    def on_init(self) -> None:
        self.append_child(AddTwoNumbersActionWithFailures, '?a ?b => ?c')
        self.append_child(PrintNumberAction, '?c')

########################################################################


class ContingencySequence(SequenceNode):
    """The `ContingencySequence` example node.

    The `ContingencySequence` extends the `Sequence` by showing how contingency
    handlers can be registered. In case of the contingency `RESULT_TOO_LARGE` all
    child nodes are removed and the two nodes `CreateRandomNumberAction` and
    `PrintNumberAction` are added. For the two contingencies `ONE_PARAM_MISSING`
    and `BOTH_PARAMS_MISSING` one contingency-handler using a wildcard `*_MISSING`
    is registered. In this case the output parameter *?c* is set to 0 and the
    current child is set to fixed. Setting a chiuld to fixed deletes the current
    contingency message and sets the status to `FIXED`. As `FIXED` is handled
    in the same way as `SUCCESS`, the sequence continues as everythig was normal.

    Input Parameters
    ----------------
    ?a : int
        The first value
    ?b : int
        The second value

    Output Parameters
    -----------------
    ?c : int
        The result

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')

    def on_init(self) -> None:
        self.append_child(AddTwoNumbersActionWithFailures, '?a ?b => ?c')
        self.append_child(PrintNumberAction, '?c')

        self.register_contingency_handler(AddTwoNumbersActionWithFailures,
                                          [NodeStatus.FAILURE],
                                          'RESULT_TOO_LARGE',
                                          self.fix_large_result)

        self.register_contingency_handler(AddTwoNumbersActionWithFailures,
                                          [NodeStatus.FAILURE],
                                          # r'ONE_PARAM_MISSING|BOTH_PARAMS_MISSING',
                                          # r'.*_MISSING',
                                          r'.*_PARAM(S)?_MISSING',
                                          self.fix_missing_input)

    def fix_large_result(self) -> None:
        print('fix_large_result')
        self.remove_all_children()
        self.append_child(CreateRandomNumberAction, '=> ?c')
        self.append_child(PrintNumberAction, '?c')

    def fix_missing_input(self) -> None:
        print('fix_missing_input: set ?c = 0')
        self._c = 0
        self.fix_current_child()

    def on_delete(self) -> None:
        if len(self.get_contingency_history()) > 0:
            entry: ContingencyHistoryEntry = self.get_contingency_history()[-1]
            if(entry.contingency_message == 'ONE_PARAM_MISSING'
               or entry.contingency_message == 'BOTH_PARAMS_MISSING'):
                self.set_contingency_message('MISSING_PARAM_FIXED')
            elif entry.contingency_message == 'RESULT_TOO_LARGE':
                self.set_contingency_message('TOO_LARGE_RESULT_FIXED')
