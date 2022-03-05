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

from carebt.contingencyHistoryEntry import ContingencyHistoryEntry
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode
from tests.actionNodes import AddTwoNumbersAction
from tests.actionNodes import AddTwoNumbersActionWithFailure
from tests.actionNodes import AddTwoNumbersLongRunningActionWithAbort
from tests.actionNodes import FixMissingNumbersAction
from tests.actionNodes import HelloWorldAction
from tests.actionNodes import HelloWorldActionWithMessage
from tests.actionNodes import ProvideMissingNumbersAction
from tests.actionNodes import ShowNumberAction
from tests.global_mock import mock

########################################################################


class AddTwoNumbersSequence1(SequenceNode):
    """The `AddTwoNumbersSequence1` example node.

    The `AddTwoNumbersSequence1` shows how an ouput parameter of a Node
    can be used as an input for another subsequent Node.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersSequence1')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence1')
        self.append_child(AddTwoNumbersAction, '3 6 => ?result')
        self.append_child(ShowNumberAction, '?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence1')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence1')

########################################################################


class AddTwoNumbersSequence1a(SequenceNode):
    """The `AddTwoNumbersSequence1a` example node.

    The `AddTwoNumbersSequence1a` is the same one as the `AddTwoNumbersSequence1` but
    with the `on_tick` function callback implemented and a throttling rate of 200ms.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        self.set_throttle_ms(200)
        mock('__init__ AddTwoNumbersSequence1a')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence1a')
        self.append_child(AddTwoNumbersAction, '3 6 => ?result')
        self.append_child(ShowNumberAction, '?result')

    def on_tick(self) -> None:
        mock('on_tick AddTwoNumbersSequence1a')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence1a')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence1a')

########################################################################


class AddTwoNumbersSequence2(SequenceNode):
    """The `AddTwoNumbersSequence2` example node.

    The `AddTwoNumbersSequence2` shows how the contingency, that at least
    one input parameter is missing, looks like. The `AddTwoNumbersActionWithFailure`
    completes with status `FAILURE` and provides the message `NOT_TWO_NUMBERS_PROVIDED`.
    As `AddTwoNumbersActionWithFailure` fails, the subsequent `ShowNumberAction`
    is not executed. As the contingency is not handeled, the `AddTwoNumbersSequence2`
    completes with `FAILURE` and also provides the message `NOT_TWO_NUMBERS_PROVIDED`.

    Input Parameters
    ----------------
    ?a : int
        The first number
    ?b : int
        The second number

    Contingencies
    -------------
    FAILURE:
        NOT_TWO_NUMBERS_PROVIDED
            At least one of the two input parameters is missing.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')
        mock('__init__ AddTwoNumbersSequence2')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence2')
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence2')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence2')

########################################################################


class AddTwoNumbersSequence3(SequenceNode):
    """The `AddTwoNumbersSequence3` example node.

    The `AddTwoNumbersSequence3` is an extension of the `AddTwoNumbersSequence2`.
    The contingency that `AddTwoNumbersActionWithFailure` completes with status
    `FAILURE` and provides the message `NOT_TWO_NUMBERS_PROVIDED` is handeled by
    the contingency-handler `fix_missing_numbers_handler`. This contingency-handler
    sets the status of the `AddTwoNumbersActionWithFailure` to `FIXED`
    and sets the ?result the `AddTwoNumbersActionWithFailure` should have provided
    to 999. Thus, the subsequent `ShowNumberAction` is executed.

    Input Parameters
    ----------------
    ?a : int
        The first number
    ?b : int
        The second number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')
        mock('__init__ AddTwoNumbersSequence3')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence3')
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

        self.register_contingency_handler(AddTwoNumbersActionWithFailure,
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.fix_missing_numbers_handler)

    def fix_missing_numbers_handler(self):
        mock('AddTwoNumbersSequence3: fix_missing_numbers_handler: set result to 999')
        print('AddTwoNumbersSequence3: fix_missing_numbers_handler: set result to 999')
        self.fix_current_child()
        self._result = 999

    def on_delete(self) -> None:
        if len(self.get_contingency_history()) > 0:
            entry: ContingencyHistoryEntry = self.get_contingency_history()[-1]
            if(entry.status == NodeStatus.FAILURE
                    and entry.contingency_message == 'NOT_TWO_NUMBERS_PROVIDED'
                    and entry.function == 'fix_missing_numbers_handler'):
                self.set_contingency_message('MISSING_NUMBERS_FIXED')
        mock('on_delete AddTwoNumbersSequence3')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence3')

########################################################################


class AddTwoNumbersSequence4(SequenceNode):
    """The `AddTwoNumbersSequence4` example node.

    The `AddTwoNumbersSequence4` is a variant of the `AddTwoNumbersSequence3`.
    The contingency that `AddTwoNumbersActionWithFailure` completes with status
    `FAILURE` and provides the message `NOT_TWO_NUMBERS_PROVIDED` is handeled by
    the contingency-handler `fix_missing_numbers_handler`. This contingency-handler
    sets the status of the `AddTwoNumbersActionWithFailure` to `FIXED`
    and inserts the `FixMissingNumbersAction` right after
    `AddTwoNumbersActionWithFailure`. The `FixMissingNumbersAction` provides the
    ?result = 42 and this can then be printed by `ShowNumberAction`.

    Input Parameters
    ----------------
    ?a : int
        The first number
    ?b : int
        The second number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')
        mock('__init__ AddTwoNumbersSequence4')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence4')
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

        self.register_contingency_handler(AddTwoNumbersActionWithFailure,
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.fix_missing_numbers_handler)

    def fix_missing_numbers_handler(self):
        print('AddTwoNumbersSequence4: fix_missing_numbers_handler: '
              'insert FixMissingNumbersAction')
        self.fix_current_child()
        self.insert_child_after_current(FixMissingNumbersAction, '=> ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence4')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence4')

########################################################################


class AddTwoNumbersSequence5(SequenceNode):
    """The `AddTwoNumbersSequence5` example node.

    The `AddTwoNumbersSequence5` is another variant of the `AddTwoNumbersSequence3`.
    In this case the contingency is handled by (i) removing all children
    and (ii) adding the three new children: `ProvideMissingNumbersAction`,
    `AddTwoNumbersActionWithFailure` and `ShowNumberAction`.

    Input Parameters
    ----------------
    ?a : int
        The first number
    ?b : int
        The second number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')
        mock('__init__ AddTwoNumbersSequence5')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence5')
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

        self.register_contingency_handler(AddTwoNumbersActionWithFailure,
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.fix_missing_numbers_handler)

    def fix_missing_numbers_handler(self):
        mock('AddTwoNumbersSequence5: fix_missing_numbers_handler: provide two numbers')
        print('AddTwoNumbersSequence5: fix_missing_numbers_handler: provide two numbers')
        self.fix_current_child()
        self.remove_all_children()
        self.append_child(ProvideMissingNumbersAction, '=> ?a ?b')
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence5')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence5')

########################################################################


class AddTwoNumbersSequence6(SequenceNode):
    """The `AddTwoNumbersSequence6` example node.

    The `AddTwoNumbersSequence6` is a variant of the `AddTwoNumbersSequence5`.
    In this variant the values of `?a` and `?b` are hard coded in the contingency-handler,
    instead of using the `ProvideMissingNumbersAction`.

    Input Parameters
    ----------------
    ?a : int
        The first number
    ?b : int
        The second number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')
        mock('__init__ AddTwoNumbersSequence6')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence6')
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

        self.register_contingency_handler(AddTwoNumbersActionWithFailure,
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.fix_missing_numbers_handler)

    def fix_missing_numbers_handler(self):
        mock('AddTwoNumbersSequence6: fix_missing_numbers_handler: provide two numbers')
        print('AddTwoNumbersSequence6: fix_missing_numbers_handler: provide two numbers')
        self.fix_current_child()
        self._a = 111
        self._b = 222
        self.remove_all_children()
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence6')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence6')

########################################################################


class AddTwoNumbersSequence7(SequenceNode):
    """The `AddTwoNumbersSequence7` example node.

    The `AddTwoNumbersSequence7` has four children and two different
    contingency_handlers. One to handle the `FAILURE` of `AddTwoNumbersActionWithFailure`
    and `AddTwoNumbersLongRunningActionWithAbort`, and the other one to handle the
    `ABORTED` of `AddTwoNumbersLongRunningActionWithAbort`. For the former the
    regex 'AddTwoNumbers.*' is used in order to activate the contingency-handler for
    both `ActionNodes`.

    Input Parameters
    ----------------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?a : int
        The first number
    ?b : int
        The second number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?a ?b')
        mock('__init__ AddTwoNumbersSequence7')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence7')
        self.set_timeout(500)

        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')
        self.append_child(AddTwoNumbersLongRunningActionWithAbort, '?calctime ?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

        self.register_contingency_handler(r'AddTwoNumbers.*',
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.fix_missing_numbers_handler)

        self.register_contingency_handler(AddTwoNumbersLongRunningActionWithAbort,
                                          [NodeStatus.ABORTED],
                                          'TIMEOUT',
                                          self.fix_timeout_handler)

    def on_timeout(self) -> None:
        mock('AddTwoNumbersSequence7: on_timeout')
        print('AddTwoNumbersSequence7: on_timeout')
        self.abort_current_child()  # abort currently running child
        self.fix_current_child()  # fix it that execution can continue
        self._result = 9999

    def fix_missing_numbers_handler(self):
        mock('AddTwoNumbersSequence7: fix_missing_numbers_handler')
        print('AddTwoNumbersSequence7: fix_missing_numbers_handler')
        self.fix_current_child()
        self._result = 1234

    def fix_timeout_handler(self):
        mock('AddTwoNumbersSequence7: fix_timeout_handler')
        print('AddTwoNumbersSequence7: fix_timeout_handler')
        self.fix_current_child()
        self._result = 4321

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence7')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence7')

########################################################################


class AddTwoNumbersSequence8(SequenceNode):
    """The `AddTwoNumbersSequence8` example node.

    The `AddTwoNumbersSequence8` has four children and two different
    contingency_handlers. One to handle the `FAILURE` of `AddTwoNumbersActionWithFailure`
    and `AddTwoNumbersLongRunningActionWithAbort`, and the other one to handle the
    `ABORTED` of `AddTwoNumbersLongRunningActionWithAbort`. For the former the
    regex 'AddTwoNumbers.*' is used in order to activate the contingency-handler for
    both `ActionNodes`.

    In this variant the timout in the `AddTwoNumbersSequence8` aborts the sequence.

    Input Parameters
    ----------------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?a : int
        The first number
    ?b : int
        The second number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?a ?b')
        mock('__init__ AddTwoNumbersSequence8')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence8')
        self.set_timeout(500)

        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')
        self.append_child(AddTwoNumbersLongRunningActionWithAbort, '?calctime ?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

        self.register_contingency_handler(r'AddTwoNumbers.*',
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.fix_missing_numbers_handler)

        self.register_contingency_handler(AddTwoNumbersLongRunningActionWithAbort,
                                          [NodeStatus.ABORTED],
                                          'TIMEOUT',
                                          self.fix_timeout_handler)

    def on_timeout(self) -> None:
        mock('AddTwoNumbersSequence8: on_timeout')
        print('AddTwoNumbersSequence8: on_timeout')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def fix_missing_numbers_handler(self):
        mock('AddTwoNumbersSequence8: fix_missing_numbers_handler')
        print('AddTwoNumbersSequence8: fix_missing_numbers_handler')
        self.fix_current_child()
        self._result = 1234

    def fix_timeout_handler(self):
        mock('AddTwoNumbersSequence8: fix_timeout_handler')
        print('AddTwoNumbersSequence8: fix_timeout_handler')
        self.fix_current_child()
        self._result = 4321

    def on_abort(self) -> None:
        mock('on_abort AddTwoNumbersSequence8')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence8')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence8')

########################################################################


class SequenceWithSuccessMessage_1(SequenceNode):
    """The `SequenceWithSuccessMessage_1` example node.

    The `SequenceWithSuccessMessage_1` has two child nodes. The first one
    provides a contingency-message, the second one not. Thus, the sequence
    should not provide a contingency-message.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ SequenceWithSuccessMessage_1')

    def on_init(self) -> None:
        mock('on_init SequenceWithSuccessMessage_1')
        self.append_child(HelloWorldActionWithMessage)
        self.append_child(HelloWorldAction)

    def on_delete(self) -> None:
        mock('on_delete SequenceWithSuccessMessage_1')

    def __del__(self):
        mock('__del__ SequenceWithSuccessMessage_1')


class SequenceWithSuccessMessage_2(SequenceNode):
    """The `SequenceWithSuccessMessage_2` example node.

    The `SequenceWithSuccessMessage_2` two child nodes. The first one
    provides no contingency-message, the second one provides one. Thus,
    the sequence should provide the contingency-message of the second node.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ SequenceWithSuccessMessage_2')

    def on_init(self) -> None:
        mock('on_init SequenceWithSuccessMessage_2')
        self.append_child(HelloWorldAction)
        self.append_child(HelloWorldActionWithMessage)

    def on_delete(self) -> None:
        mock('on_delete SequenceWithSuccessMessage_2')

    def __del__(self):
        mock('__del__ SequenceWithSuccessMessage_2')

########################################################################


class AddTwoNumbersSequence9(SequenceNode):
    """The `AddTwoNumbersSequence9` example node.

    The `AddTwoNumbersSequence9` is a variant of the `AddTwoNumbersSequence4`.

    Input Parameters
    ----------------
    ?a : int
        The first number
    ?b : int
        The second number

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?a ?b')
        mock('__init__ AddTwoNumbersSequence9')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersSequence9')
        self.append_child(AddTwoNumbersActionWithFailure, '?a ?b => ?result')
        self.append_child(ShowNumberAction, '?result')

        self.register_contingency_handler(AddTwoNumbersActionWithFailure,
                                          [NodeStatus.FAILURE],
                                          'NOT_TWO_NUMBERS_PROVIDED',
                                          self.fix_missing_numbers_handler)

    def fix_missing_numbers_handler(self):
        print('AddTwoNumbersSequence9: fix_missing_numbers_handler: '
              'insert FixMissingNumbersAction')
        self.remove_all_children()
        self.insert_child_after_current(ShowNumberAction, '?result')
        self.insert_child_after_current(FixMissingNumbersAction, '=> ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersSequence9')

    def __del__(self):
        mock('__del__ AddTwoNumbersSequence9')

########################################################################


class AsyncAddChildSequence(SequenceNode):
    """The `AsyncAddChildSequence` example node.

    The `AsyncAddChildSequence` starts with an empty child list and adds the
    `HelloWorldAction` child after the timer expires.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '')
        mock('__init__ AsyncAddChildSequence')

    def on_init(self) -> None:
        mock('on_init AsyncAddChildSequence')
        Timer(0.5, self.done_callback).start()

    def done_callback(self) -> None:
        mock('AsyncAddChildSequence: DONE')
        self.set_status(NodeStatus.RUNNING)
        self.append_child(HelloWorldAction)

########################################################################


class RemoveAllChildrenSequence(SequenceNode):
    """The `RemoveAllChildrenSequence` node.

    The `RemoveAllChildrenSequence` starts with an empty child list and calls
    remove_all_children().
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '')
        mock('__init__ RemoveAllChildrenSequence')

    def on_init(self) -> None:
        mock('on_init RemoveAllChildrenSequence')
        self.remove_all_children()
        self.set_status(NodeStatus.SUCCESS)

########################################################################


class AddTwoNumbersDynamic(SequenceNode):
    """The `AddTwoNumbersDynamic` example node.

    The `AddTwoNumbersDynamic` shows.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_init(self) -> None:
        values = [(2, 11), (5, 22), (9, 33)]
        for self.v in values:
            self.append_child(AddTwoNumbersAction, 'v[0] 5 => ?result')
            self.append_child(ShowNumberAction, '?result')
