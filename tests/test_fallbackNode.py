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

from carebt.abstractLogger import LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from tests.fallbackNodes import AddTwoNumbersFallback1
from tests.fallbackNodes import AddTwoNumbersFallback2
from tests.fallbackNodes import AddTwoNumbersFallback3
from tests.fallbackNodes import AddTwoNumbersFallback4
from tests.fallbackNodes import AddTwoNumbersFallback5
from tests.fallbackNodes import AddTwoNumbersFallback6
from tests.fallbackNodes import AddTwoNumbersFallback7
from tests.fallbackNodes import AsyncAddChildFallback
from tests.fallbackNodes import RemoveAllChildrenFallback
from tests.global_mock import mock

########################################################################


class TestFallbackNode:
    """Tests the `AddTwoNumbersFallback1`."""

    ########################################################################

    def test_AddTwoNumbersFallback1(self):
        """Tests the AddTwoNumbersFallback1."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersFallback1)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersFallback1'),
                                       call('on_init AddTwoNumbersFallback1'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 2 + 4 = 6'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('on_delete AddTwoNumbersFallback1'),
                                       call('__del__ AddTwoNumbersFallback1')]

    ########################################################################

    def test_AddTwoNumbersFallback2(self):
        """Tests the AddTwoNumbersFallback2."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersFallback2)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersFallback2'),
                                       call('on_init AddTwoNumbersFallback2'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 3 + 6 = 9'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('on_delete AddTwoNumbersFallback2'),
                                       call('__del__ AddTwoNumbersFallback2')]

    ########################################################################

    def test_AddTwoNumbersFallback3(self):
        """Tests the AddTwoNumbersFallback3."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersFallback3)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersFallback3'),
                                       call('on_init AddTwoNumbersFallback3'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 2 + 4 = 6'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('on_delete AddTwoNumbersFallback3'),
                                       call('__del__ AddTwoNumbersFallback3')]

    ########################################################################

    def test_AddTwoNumbersFallback4(self):
        """Tests the AddTwoNumbersFallback4."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersFallback4)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'NOT_TWO_NUMBERS_PROVIDED'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersFallback4'),
                                       call('on_init AddTwoNumbersFallback4'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('on_delete AddTwoNumbersFallback4'),
                                       call('__del__ AddTwoNumbersFallback4')]

    ########################################################################

    def test_AddTwoNumbersFallback5(self):
        """Tests the AddTwoNumbersFallback5."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.DEBUG)
        bt_runner.run(AddTwoNumbersFallback5)
        assert mock.called
        assert bt_runner.get_status() == NodeStatus.ABORTED
        assert bt_runner.get_contingency_message() == 'NOT_TWO_NUMBERS_PROVIDED'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersFallback5'),
                                       call('on_init AddTwoNumbersFallback5'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('AddTwoNumbersFallback5: handle_missing_numbers'),
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('on_abort AddTwoNumbersFallback5'),
                                       call('on_delete AddTwoNumbersFallback5'),
                                       call('__del__ AddTwoNumbersFallback5')]

    ########################################################################

    def test_AddTwoNumbersFallback6(self):
        """Tests the AddTwoNumbersFallback6."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.DEBUG)
        bt_runner.run(AddTwoNumbersFallback6)
        assert mock.called
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersFallback6'),
                                       call('on_init AddTwoNumbersFallback6'),
                                       call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('AddTwoNumbersFallback6: handle_missing_numbers'),
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure'),
                                       call('__init__ HelloWorldAction'),
                                       call('HelloWorldAction: Hello World !!!'),
                                       call('__del__ HelloWorldAction'),
                                       call('on_delete AddTwoNumbersFallback6'),
                                       call('__del__ AddTwoNumbersFallback6')]

    ########################################################################

    def test_AddTwoNumbersFallback7(self):
        """Tests the AddTwoNumbersFallback7."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.DEBUG)
        bt_runner.run(AddTwoNumbersFallback7)
        assert mock.called
        assert bt_runner.get_status() == NodeStatus.ABORTED
        assert bt_runner.get_contingency_message() == 'TIMEOUT'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersFallback7'),
                                       call('on_init AddTwoNumbersFallback7'),
                                       call('__init__ AddTwoNumbersLongRunningAction'),
                                       call('on_init AddTwoNumbersLongRunningAction'),
                                       call('AddTwoNumbersLongRunningAction: calculating 2000 ms ...'),  # noqa: E501
                                       call('on_timeout AddTwoNumbersFallback7'),
                                       call('on_abort AddTwoNumbersLongRunningAction'),
                                       call('on_delete AddTwoNumbersLongRunningAction'),
                                       call('on_abort AddTwoNumbersFallback7'),
                                       call('__del__ AddTwoNumbersLongRunningAction'),
                                       call('on_delete AddTwoNumbersFallback7'),
                                       call('__del__ AddTwoNumbersFallback7')]

    ########################################################################

    def test_AsyncAddChildFallback(self):
        """Tests the AsyncAddChildFallback."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AsyncAddChildFallback, '')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AsyncAddChildFallback'),
                                       call('on_init AsyncAddChildFallback'),
                                       call('AsyncAddChildFallback: DONE'),
                                       call('__init__ HelloWorldAction'),
                                       call('HelloWorldAction: Hello World !!!'),
                                       call('__del__ HelloWorldAction')]

    ########################################################################

    def test_RemoveAllChildrenFallback(self):
        """Test the `RemoveAllChildrenFallback` node."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(RemoveAllChildrenFallback, '')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ RemoveAllChildrenFallback'),
                                       call('on_init RemoveAllChildrenFallback')]
