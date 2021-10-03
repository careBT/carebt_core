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

from carebt.abstractLogger import LogLevel

from tests.actionNodes import AddTwoNumbersAction
from tests.actionNodes import AddTwoNumbersActionWithFailure
from tests.actionNodes import AddTwoNumbersLongRunnungAction
from tests.actionNodes import AddTwoNumbersLongRunnungActionWithAbort
from tests.actionNodes import AddTwoNumbersMultiTickAction
from tests.actionNodes import AddTwoNumbersThrottledMultiTickAction
from tests.actionNodes import HelloWorldAction
from tests.global_mock import mock

from unittest.mock import call

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus


class TestActionNode:

    ########################################################################

    def test_HelloWorldAction(self):
        """
        Tests if a simple `ActionNode` runs.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.run(HelloWorldAction)
        assert mock.called
        assert bt_runner.get_tick_count() == 1
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(print(mock.call_args_list))
        assert mock.call_args_list == [call('__init__ HelloWorldAction'),
                                       call('on_init HelloWorldAction'),
                                       call('HelloWorldAction: Hello World !!!'),
                                       call('on_delete HelloWorldAction'),
                                       call('__del__ HelloWorldAction')]

    ########################################################################

    def test_AddTwoNumbersAction_3_5(self):
        """
        Test two valid inputs one output

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '3 5 => ?result')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 3 + 5 = 8'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction')]
        assert bt_runner._instance._result == 8
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_AddTwoNumbersAction_0_0(self):
        """
        Test two valid inputs (0 + 0) one output

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '0 0 => ?result')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 0 + 0 = 0'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction')]
        assert bt_runner._instance._result == 0
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_AddTwoNumbersAction_9(self):
        """
        Test one input is missing, but default of missing ?y is 5678

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '9 => ?result')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 9 + 5678 = 5687'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction')]
        assert bt_runner._instance._result == 5687
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_AddTwoNumbersAction(self):
        """
        Test both inputs are missing, but default of missing ?x is 1234 and
        ?y is 5678

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '=> ?result')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 1234 + 5678 = 6912'),  # noqa: E501
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction')]
        assert bt_runner._instance._result == 6912
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_AddTwoNumbersAction_missing_out(self):
        """
        Test both inputs present, but output is missing

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '1 2')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 1 + 2 = 3'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction')]
        assert not hasattr(bt_runner._instance, '_result')
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    ########################################################################

    def test_AddTwoNumbersActionWithFailure_3_5(self):
        """
        Test two valid inputs one output

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersActionWithFailure, '3 5 => ?result')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: calculating: 3 + 5 = 8'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure')]
        assert bt_runner._instance._result == 8
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_AddTwoNumbersActionWithFailure_7(self):
        """
        Test one input missing -> node should fail

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersActionWithFailure, '7 => ?result')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersActionWithFailure'),
                                       call('on_init AddTwoNumbersActionWithFailure'),
                                       call('AddTwoNumbersActionWithFailure: You did not provide two numbers!'),  # noqa: E501
                                       call('on_delete AddTwoNumbersActionWithFailure'),
                                       call('__del__ AddTwoNumbersActionWithFailure')]
        assert not hasattr(bt_runner._instance, '_result')
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'NOT_TWO_NUMBERS_PROVIDED'

    ########################################################################

    def test_AddTwoNumbersMultiTickAction_5_3_5(self):
        """
        Test that calculation takes 5 ticks and one tick takes 10ms

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.set_tick_rate_ms(10)
        start = datetime.now()
        bt_runner.run(AddTwoNumbersMultiTickAction, '5 3 5 => ?result')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 55
        assert int(delta.total_seconds() * 1000) < 70
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersMultiTickAction'),
                                       call('on_init AddTwoNumbersMultiTickAction'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 1/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 2/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 3/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 4/5)'),
                                       call('AddTwoNumbersMultiTickAction: (tick_count = 5/5)'),
                                       call('AddTwoNumbersMultiTickAction: DONE 3 + 5 = 8'),
                                       call('on_delete AddTwoNumbersMultiTickAction'),
                                       call('__del__ AddTwoNumbersMultiTickAction')]
        assert bt_runner._instance._result == 8
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        assert bt_runner.get_tick_count() == 6

    ########################################################################

    def test_AddTwoNumbersThrottledMultiTickAction_5_3_5(self):
        """
        Test that calculation takes 5 ticks and this forwarded ticks
        are throttled to 500ms.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.set_tick_rate_ms(10)
        start = datetime.now()
        bt_runner.run(AddTwoNumbersThrottledMultiTickAction, '5 3 5 => ?result')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 2400
        assert int(delta.total_seconds() * 1000) < 2600
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersThrottledMultiTickAction'),
                                       call('on_init AddTwoNumbersThrottledMultiTickAction'),
                                       call('AddTwoNumbersThrottledMultiTickAction: (tick_count = 1/5)'),  # noqa: E501
                                       call('AddTwoNumbersThrottledMultiTickAction: (tick_count = 2/5)'),  # noqa: E501
                                       call('AddTwoNumbersThrottledMultiTickAction: (tick_count = 3/5)'),  # noqa: E501
                                       call('AddTwoNumbersThrottledMultiTickAction: (tick_count = 4/5)'),  # noqa: E501
                                       call('AddTwoNumbersThrottledMultiTickAction: (tick_count = 5/5)'),  # noqa: E501
                                       call('AddTwoNumbersThrottledMultiTickAction: DONE 3 + 5 = 8'),  # noqa: E501
                                       call('on_delete AddTwoNumbersThrottledMultiTickAction'),
                                       call('__del__ AddTwoNumbersThrottledMultiTickAction')]
        assert bt_runner._instance._result == 8
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    ########################################################################

    def test_AddTwoNumbersLongRunnungAction_500_3_5(self):
        """
        Tests a long running calculation

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        start = datetime.now()
        bt_runner.run(AddTwoNumbersLongRunnungAction, '500 3 5 => ?result')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 500
        assert int(delta.total_seconds() * 1000) < 600
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersLongRunnungAction'),
                                       call('on_init AddTwoNumbersLongRunnungAction'),
                                       call('AddTwoNumbersLongRunnungAction: calculating 500 ms ...'),  # noqa: E501
                                       call('AddTwoNumbersLongRunnungAction: done: 3 + 5 = 8'),  # noqa: E501
                                       call('on_delete AddTwoNumbersLongRunnungAction'),
                                       call('__del__ AddTwoNumbersLongRunnungAction')]
        assert bt_runner._instance._result == 8
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    ########################################################################

    def test_AddTwoNumbersLongRunnungActionWithAbort_100_3_5(self):
        """
        Tests a long running calculation which is faster (100ms) than
        the timeout (1000ms)

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.set_tick_rate_ms(10)
        start = datetime.now()
        bt_runner.run(AddTwoNumbersLongRunnungActionWithAbort, '100 3 5 => ?result')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 100
        assert int(delta.total_seconds() * 1000) < 200
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_init AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('AddTwoNumbersLongRunnungActionWithAbort: calculating 100 ms ... (timeout = 1000 ms)'),  # noqa: E501
                                       call('AddTwoNumbersLongRunnungActionWithAbort: done_callback: 3 + 5 = 8'),  # noqa: E501
                                       call('on_delete AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__del__ AddTwoNumbersLongRunnungActionWithAbort')]
        assert bt_runner._instance._result == 8
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_AddTwoNumbersLongRunnungActionWithAbort_1500_3_5(self):
        """
        Tests a long running calculation which is slower (1500ms) than
        the timeout (1000ms). In the timeout handler, the node is aborted
        with message `TIMEOUT`. The `?result` is not set.

        """

        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        start = datetime.now()
        bt_runner.run(AddTwoNumbersLongRunnungActionWithAbort, '1500 3 5 => ?result')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1000
        assert int(delta.total_seconds() * 1000) < 1100
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_init AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('AddTwoNumbersLongRunnungActionWithAbort: calculating 1500 ms ... (timeout = 1000 ms)'),  # noqa: E501
                                       call('on_timeout AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_abort AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('on_delete AddTwoNumbersLongRunnungActionWithAbort'),
                                       call('__del__ AddTwoNumbersLongRunnungActionWithAbort')]
        assert not hasattr(bt_runner._instance, '_result')
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == 'TIMEOUT'
