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

from unittest.mock import call

from tests.global_mock import mock
from tests.sequenceNodes import AddTwoNumbersSequence1
from tests.sequenceNodes import AddTwoNumbersSequence2
from tests.sequenceNodes import AddTwoNumbersSequence3
from tests.sequenceNodes import AddTwoNumbersSequence4
from tests.sequenceNodes import AddTwoNumbersSequence5
from tests.sequenceNodes import AddTwoNumbersSequence6
from tests.sequenceNodes import AddTwoNumbersSequence7
from tests.sequenceNodes import AddTwoNumbersSequence8

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus

########################################################################


class TestSequenceNode:
    """
    Tests the `ActionNode`.

    """

    ########################################################################

    def test_AddTwoNumbersSequence1(self):
        """
        Tests the AddTwoNumbersSequence1

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence1)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence1'),
                                       call('on_init AddTwoNumbersSequence1'),
                                       call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 3 + 6 = 9'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 9!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence1'),
                                       call('__del__ AddTwoNumbersSequence1')]

    ########################################################################

    def test_AddTwoNumbersSequence2_1_2(self):
        """
        Tests the AddTwoNumbersSequence2 with two valid inputs.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence2, '1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence2'),
                                       call('on_init AddTwoNumbersSequence2'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence2'),
                                       call('__del__ AddTwoNumbersSequence2')]

    def test_AddTwoNumbersSequence2_1(self):
        """
        Tests the AddTwoNumbersSequence2 with one missing input. The
        `AddTwoNumbersActionWithFailure` fails, thus the ShowNumberAction`
        is not executed and the `AddTwoNumbersSequence2` also fails.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence2, '1')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'NOT_TWO_NUMBERS_PROVIDED'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence2'),
                                       call('on_init AddTwoNumbersSequence2'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('on_delete AddTwoNumbersSequence2'),
                                       call('__del__ AddTwoNumbersSequence2')]

    ########################################################################

    def test_AddTwoNumbersSequence3_1_2(self):
        """
        Tests the AddTwoNumbersSequence3 with two valid inputs.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence3, '1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence3'),
                                       call('on_init AddTwoNumbersSequence3'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence3'),
                                       call('__del__ AddTwoNumbersSequence3')]

    def test_AddTwoNumbersSequence3_1(self):
        """
        Tests the AddTwoNumbersSequence3 with one missing input. The
        `AddTwoNumbersActionWithFailure` fails, thus the ShowNumberAction`
        is not executed and the `AddTwoNumbersSequence2` also fails.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence3, '1')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence3'),
                                       call('on_init AddTwoNumbersSequence3'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('AddTwoNumbersSequence3: fix_missing_numbers_handler: set result to 999'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 999!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence3'),
                                       call('__del__ AddTwoNumbersSequence3')]

    ########################################################################

    def test_AddTwoNumbersSequence4_1_2(self):
        """
        Tests the AddTwoNumbersSequence4 with two valid inputs.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence4, '1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence4'),
                                       call('on_init AddTwoNumbersSequence4'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence4'),
                                       call('__del__ AddTwoNumbersSequence4')]

    def test_AddTwoNumbersSequence4_1(self):
        """
        Tests the AddTwoNumbersSequence4 with one missing input. The
        `AddTwoNumbersActionWithFailure` fails. The contingency-handler
        inserts the child `FixMissingNumbersAction` which sets the `?result` to 42
        and thus, the sequence continues as desired with the `ShowNumberAction`.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence4, '1')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence4'),
                                       call('on_init AddTwoNumbersSequence4'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ FixMissingNumbersAction'),
                                       call('on_init FixMissingNumbersAction'),
                                       call('FixMissingNumbersAction: fix missing numbers!'),
                                       call('on_delete FixMissingNumbersAction'),
                                       call('__del__ FixMissingNumbersAction'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 42!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence4'),
                                       call('__del__ AddTwoNumbersSequence4')]

    ########################################################################

    def test_AddTwoNumbersSequence5_1_2(self):
        """
        Tests the AddTwoNumbersSequence5 with two valid inputs.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence5, '1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence5'),
                                       call('on_init AddTwoNumbersSequence5'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence5'),
                                       call('__del__ AddTwoNumbersSequence5')]

    def test_AddTwoNumbersSequence5_1(self):
        """
        Tests the AddTwoNumbersSequence5 with one missing input. The
        `AddTwoNumbersActionWithFailure` fails. The contingency-handler
        removes all subsequent children and adds the following three nodes:
        `ProvideMissingNumbersAction`, `AddTwoNumbersActionWithFailure`
        and `ShowNumberAction`

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence5, '1')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence5'),
                                       call('on_init AddTwoNumbersSequence5'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('AddTwoNumbersSequence5: fix_missing_numbers_handler: provide two numbers'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ProvideMissingNumbersAction'),
                                       call('on_init ProvideMissingNumbersAction'),
                                       call('ProvideMissingNumbersAction: provide missing numbers!'),  # noqa: E501
                                       call('on_delete ProvideMissingNumbersAction'),
                                       call('__del__ ProvideMissingNumbersAction'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 11 + 22 = 33'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 33!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence5'),
                                       call('__del__ AddTwoNumbersSequence5')]

    ########################################################################

    def test_AddTwoNumbersSequence6_1_2(self):
        """
        Tests the AddTwoNumbersSequence6 with two valid inputs.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence6, '1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence6'),
                                       call('on_init AddTwoNumbersSequence6'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence6'),
                                       call('__del__ AddTwoNumbersSequence6')]

    def test_AddTwoNumbersSequence6_1(self):
        """
        Tests the AddTwoNumbersSequence6 with one missing input. The
        `AddTwoNumbersActionWithFailure` fails. The contingency-handler
        removes all subsequent children, sets ?a to 111 and ?b to 222 and
        adds the following two nodes: `AddTwoNumbersActionWithFailure`
        and `ShowNumberAction`

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence6, '1')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence6'),
                                       call('on_init AddTwoNumbersSequence6'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('AddTwoNumbersSequence6: fix_missing_numbers_handler: provide two numbers'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 111 + 222 = 333'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 333!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence6'),
                                       call('__del__ AddTwoNumbersSequence6')]

    ########################################################################

    def test_AddTwoNumbersSequence7_50_1_2(self):
        """
        Tests the AddTwoNumbersSequence7 with two valid inputs and ?calctime = 50ms,
        which is faster than the timeout of the `AddTwoNumbersLongRunnungActionWithAbort`
        (1000ms) and the `AddTwoNumbersSequence7`(500ms).

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence7, '50 1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence7'),
                                       call('on_init AddTwoNumbersSequence7'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('__init__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_init AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('AddTwoNumbersLongRunnungActionWithAbort: calculating 50 ms ... (timeout = 1000 ms)'),  # noqa: E501
                                       call('AddTwoNumbersLongRunnungActionWithAbort: done_callback: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__del__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence7'),
                                       call('__del__ AddTwoNumbersSequence7')]

    def test_AddTwoNumbersSequence7_750_1_2(self):
        """
        Tests the AddTwoNumbersSequence7 with two valid inputs and ?calctime = 750ms,
        which is slower as the timeout in `AddTwoNumbersSequence7`(500ms).

        The timeout in the `AddTwoNumbersSequence7` aborts the current child, fixes it that
        the sequence can continue and sets the ?result to 9999.
        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence7, '750 1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence7'),
                                       call('on_init AddTwoNumbersSequence7'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('__init__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_init AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('AddTwoNumbersLongRunnungActionWithAbort: calculating 750 ms ... (timeout = 1000 ms)'),  # noqa: E501
                                       call('AddTwoNumbersSequence7: on_timeout'),
                                       call('on_abort AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_delete AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__del__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 9999!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence7'),
                                       call('__del__ AddTwoNumbersSequence7')]

    def test_AddTwoNumbersSequence7_50_1(self):
        """
        Tests the `AddTwoNumbersSequence7` with ONLY one valid input and ?calctime = 50ms,
        which is faster than the timeout of the `AddTwoNumbersLongRunnungActionWithAbort`
        (1000ms) and the `AddTwoNumbersSequence7`(500ms).

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence7, '1250 1')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence7'),
                                       call('on_init AddTwoNumbersSequence7'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('AddTwoNumbersSequence7: fix_missing_numbers_handler'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 1234!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('__init__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_init AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('AddTwoNumbersLongRunnungActionWithAbort: You did not provide two numbers!'),  # noqa: E501
                                       call('AddTwoNumbersSequence7: fix_missing_numbers_handler'),  # noqa: E501
                                       call('on_delete AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__del__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 1234!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('on_delete AddTwoNumbersSequence7'),
                                       call('__del__ AddTwoNumbersSequence7')]

    ########################################################################

    def test_AddTwoNumbersSequence8_750_1_2(self):
        """
        Tests the AddTwoNumbersSequence8 with two valid inputs and ?calctime = 750ms,
        which slower as the `AddTwoNumbersSequence7`(500ms).

        The timeout in the `AddTwoNumbersSequence7` aborts the sequence.
        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersSequence8, '750 1 2')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == 'TIMEOUT'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersSequence8'),
                                       call('on_init AddTwoNumbersSequence8'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 1 + 2 = 3'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ ShowNumberAction'),
                                       call('on_init ShowNumberAction'),
                                       call('ShowNumberAction: The numer is: 3!'),
                                       call('on_delete ShowNumberAction'),
                                       call('__del__ ShowNumberAction'),
                                       call('__init__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_init AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('AddTwoNumbersLongRunnungActionWithAbort: calculating 750 ms ... (timeout = 1000 ms)'),  # noqa: E501
                                       call('AddTwoNumbersSequence8: on_timeout'),
                                       call('on_abort AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_delete AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_abort AddTwoNumbersSequence8'),
                                       call('__del__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_delete AddTwoNumbersSequence8'),
                                       call('__del__ AddTwoNumbersSequence8')]
