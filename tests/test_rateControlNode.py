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

from datetime import datetime
from unittest.mock import call

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from tests.global_mock import mock
from tests.rateControlNodes import AsyncAddChildRateControl
from tests.rateControlNodes import RateControlledAddTwoNumbersMultiTickAction
from tests.rateControlNodes import RateControlledAddTwoNumbersMultiTickActionOwnTimeout
from tests.rateControlNodes import RateControlledAddTwoNumbersMultiTickActionWithTimeout
from tests.rateControlNodes import RateControlledHelloWorldActionWithMessage

########################################################################


class TestRateControlNode:
    """Test the `RateControlledAddTwoNumbersMultiTickAction`."""

    ########################################################################

    def test_RateControlledAddTwoNumbersMultiTickAction(self):
        """Test the `RateControlledAddTwoNumbersMultiTickAction` node.

        Test the `RateControlledAddTwoNumbersMultiTickAction`. The `RateControlNode`
        throttles down the AddTwoNumbersMultiTickAction.
        """
        mock.reset_mock()
        bt = BehaviorTreeRunner()
        start = datetime.now()
        bt.run(RateControlledAddTwoNumbersMultiTickAction)
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1250
        assert int(delta.total_seconds() * 1000) < 1350
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ RateControlledAddTwoNumbersMultiTickAction'),  # noqa: E501
                                       call('on_init RateControlledAddTwoNumbersMultiTickAction'),  # noqa: E501
                                       call('__init__ AddTwoNumbersMultiTickAction'),
                                       call('on_init AddTwoNumbersMultiTickAction'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 1/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 2/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 3/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 4/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 5/5)'),
                                       call('AddTwoNumbersMultiTickAction: DONE 1 + 2 = 3'),
                                       call('on_delete AddTwoNumbersMultiTickAction'),
                                       call('__del__ AddTwoNumbersMultiTickAction'),
                                       call('on_delete RateControlledAddTwoNumbersMultiTickAction'),  # noqa: E501
                                       call('__del__ RateControlledAddTwoNumbersMultiTickAction')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_contingency_message() == ''

    ########################################################################

    def test_RateControlledAddTwoNumbersMultiTickActionWithTimeout(self):
        """Test the `RateControlledAddTwoNumbersMultiTickActionWithTimeout` node.

        Test the test_RateControlledAddTwoNumbersMultiTickActionWithTimeout. The
        `RateControlNode` throttles down the AddTwoNumbersMultiTickAction. But in
        this case the timeout in the `AddTwoNumbersMultiTickAction` aborts the
        AddTwoNumbersMultiTickAction.
        """
        mock.reset_mock()
        bt = BehaviorTreeRunner()
        start = datetime.now()
        bt.run(RateControlledAddTwoNumbersMultiTickActionWithTimeout)
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1000
        assert int(delta.total_seconds() * 1000) < 1200
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ RateControlledAddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('on_init RateControlledAddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('__init__ AddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('on_init AddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 1/5)'),  # noqa: E501
                                       call('AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 2/5)'),  # noqa: E501
                                       call('AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 3/5)'),  # noqa: E501
                                       call('on_timeout AddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('on_delete AddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('__del__ AddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('on_delete RateControlledAddTwoNumbersMultiTickActionWithTimeout'),  # noqa: E501
                                       call('__del__ RateControlledAddTwoNumbersMultiTickActionWithTimeout')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_contingency_message() == 'TIMEOUT'

    ########################################################################

    def test_RateControlledAddTwoNumbersMultiTickAction_timeout(self):
        """Test the `RateControlledAddTwoNumbersMultiTickActionOwnTimeout` node.

        Test the RateControlledAddTwoNumbersMultiTickAction. The `RateControlNode`
        throttles down the AddTwoNumbersMultiTickAction. This time a timeout in the
        `RateControlNode` aborts the `RateControlNode`.
        """
        mock.reset_mock()
        bt = BehaviorTreeRunner()
        start = datetime.now()
        bt.run(RateControlledAddTwoNumbersMultiTickActionOwnTimeout)
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1000
        assert int(delta.total_seconds() * 1000) < 1200
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ RateControlledAddTwoNumbersMultiTickActionOwnTimeout'),  # noqa: E501
                                       call('on_init RateControlledAddTwoNumbersMultiTickActionOwnTimeout'),  # noqa: E501
                                       call('__init__ AddTwoNumbersMultiTickAction'),
                                       call('on_init AddTwoNumbersMultiTickAction'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 1/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 2/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 3/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 4/5)'),
                                       call('on_timeout RateControlledAddTwoNumbersMultiTickActionOwnTimeout'),  # noqa: E501
                                       call('on_delete AddTwoNumbersMultiTickAction'),
                                       call('__del__ AddTwoNumbersMultiTickAction'),
                                       call('on_delete RateControlledAddTwoNumbersMultiTickActionOwnTimeout'),  # noqa: E501
                                       call('__del__ RateControlledAddTwoNumbersMultiTickActionOwnTimeout')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_contingency_message() == 'TIMEOUT'

    ########################################################################

    def test_RateControlledHelloWorldActionWithMessage(self):
        """Test the `RateControlledHelloWorldActionWithMessage` node."""
        mock.reset_mock()
        bt = BehaviorTreeRunner()
        bt.run(RateControlledHelloWorldActionWithMessage)
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_contingency_message() == 'HELLOWORLD_PRINTED'

    ########################################################################

    def test_AsyncAddChildSequence(self):
        """Tests the AsyncAddChildSequence node."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AsyncAddChildRateControl, '')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AsyncAddChildRateControl'),
                                       call('on_init AsyncAddChildRateControl'),
                                       call('AsyncAddChildRateControl: DONE'),
                                       call('__init__ HelloWorldAction'),
                                       call('HelloWorldAction: Hello World !!!'),
                                       call('__del__ HelloWorldAction')]
