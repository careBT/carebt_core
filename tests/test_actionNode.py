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

from tests.addNumbersAction import AddTwoNumbersAction
from tests.global_mock import mock
from tests.helloActions import HelloWorldAction
from tests.helloActions import LongRunningHelloWorldAction
from tests.helloActions import MultiTickHelloWorldAction
from tests.helloActions import MultiTickThrottledHelloWorldAction
from tests.helloActions import SayHelloAction

from unittest.mock import call

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus


class TestActionNode:

    def test_action(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(HelloWorldAction)
        assert mock.called
        assert mock.call_count == 3
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_action_with_in_param_success(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SayHelloAction, '"Alice"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('bt finished')]
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_action_with_in_param_failure(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SayHelloAction, '"Bob"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SayHelloAction'),
                                       call('on_tick - Bob'),
                                       call('__del__ SayHelloAction'),
                                       call('bt finished')]
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'BOB_IS_NOT_ALLOWED'

    def test_action_with_missing_param(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SayHelloAction)
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SayHelloAction'),
                                       call('on_tick - Default Name'),
                                       call('__del__ SayHelloAction'),
                                       call('bt finished')]
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_action_add_two_numbers(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '3 5 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 3 + 5'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt_runner._instance._result == 8
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_action_add_two_numbers_one_missing_input(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '3 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 3 + 999'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt_runner._instance._result == 1002
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_action_add_two_numbers_missing_input(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, ' => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 999 + 999'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt_runner._instance._result == 1998
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_action_add_two_numbers_zeros(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '0 0 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 0 + 0'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt_runner._instance._result == 0
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_action_add_two_numbers_no_output(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '123 123 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 123 + 123'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_long_running_hello_world(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        assert bt_runner.get_tick_count() == 0
        bt_runner.set_tick_rate_ms(50)
        start = datetime.now()
        bt_runner.run(LongRunningHelloWorldAction, '"Alice"')
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1900
        assert int(delta.total_seconds() * 1000) < 2100
        assert bt_runner.get_tick_count() >= 35
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.SUCCESS'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_long_running_hello_world_dave(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        assert bt_runner.get_tick_count() == 0
        bt_runner.set_tick_rate_ms(50)
        start = datetime.now()
        bt_runner.run(LongRunningHelloWorldAction, '"Dave"')
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1900
        assert int(delta.total_seconds() * 1000) < 2100
        assert bt_runner.get_tick_count() >= 35
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: abort'),  # noqa: E501
                                       call('abort_handler LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == ''

    def test_multi_tick_hello_world(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        assert bt_runner.get_tick_count() == 0
        bt_runner.set_tick_rate_ms(50)
        start = datetime.now()
        bt_runner.run(MultiTickHelloWorldAction)
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 180
        assert int(delta.total_seconds() * 1000) < 220
        assert bt_runner.get_tick_count() == 4
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 1)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 2)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 3)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('__del__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_multi_tick_throtteled_hello_world(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        start = datetime.now()
        bt_runner.run(MultiTickThrottledHelloWorldAction)
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1500
        assert int(delta.total_seconds() * 1000) < 1600
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ MultiTickThrottledHelloWorldAction'),  # noqa: E501
                                       call('MultiTickThrottledHelloWorldAction: Hello World ... takes several ticks ... (attempts = 1)'),  # noqa: E501
                                       call('MultiTickThrottledHelloWorldAction: Hello World ... takes several ticks ... (attempts = 2)'),  # noqa: E501
                                       call('MultiTickThrottledHelloWorldAction: Hello World ... takes several ticks ... (attempts = 3)'),  # noqa: E501
                                       call('MultiTickThrottledHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('__del__ MultiTickThrottledHelloWorldAction'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
