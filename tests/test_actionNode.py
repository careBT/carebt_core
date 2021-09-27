from datetime import datetime

from tests.addNumbersAction import AddTwoNumbersAction
from tests.global_mock import mock
from tests.helloActions import HelloWorldAction
from tests.helloActions import LongRunningHelloWorldAction
from tests.helloActions import MultiTickHelloWorldAction
from tests.helloActions import MultiTickThrottledHelloWorldAction
from tests.helloActions import SayHelloAction

from unittest.mock import call

from carebt.behaviorTree import BehaviorTree
from carebt.nodeStatus import NodeStatus


class TestActionNode:

    def test_action(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(HelloWorldAction)
        assert mock.called
        assert mock.call_count == 3
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_action_with_in_param_success(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SayHelloAction, '"Alice"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_action_with_in_param_failure(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SayHelloAction, '"Bob"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SayHelloAction'),
                                       call('on_tick - Bob'),
                                       call('__del__ SayHelloAction'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.FAILURE
        assert bt._instance.get_message() == 'BOB_IS_NOT_ALLOWED'

    def test_action_with_missing_param(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SayHelloAction)
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SayHelloAction'),
                                       call('on_tick - Default Name'),
                                       call('__del__ SayHelloAction'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_action_add_two_numbers(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt._instance._result = None  # to supress the no-member warning
        bt.run(AddTwoNumbersAction, '3 5 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 3 + 5'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt._instance._result == 8
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_action_add_two_numbers_one_missing_input(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt._instance._result = None  # to supress the no-member warning
        bt.run(AddTwoNumbersAction, '3 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 3 + 999'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt._instance._result == 1002
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_action_add_two_numbers_missing_input(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt._instance._result = None  # to supress the no-member warning
        bt.run(AddTwoNumbersAction, ' => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 999 + 999'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt._instance._result == 1998
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_action_add_two_numbers_zeros(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt._instance._result = None  # to supress the no-member warning
        bt.run(AddTwoNumbersAction, '0 0 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 0 + 0'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt._instance._result == 0
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_action_add_two_numbers_no_output(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt._instance._result = None  # to supress the no-member warning
        bt.run(AddTwoNumbersAction, '123 123 => ?result')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersAction'),
                                       call('on_tick - 123 + 123'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('bt finished')]
        assert bt._instance._result is None
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_long_running_hello_world(self):
        mock.reset_mock()
        bt = BehaviorTree()
        assert bt.get_tick_count() == 0
        bt.set_tick_rate_ms(50)
        start = datetime.now()
        bt.run(LongRunningHelloWorldAction, '"Alice"')
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1900
        assert int(delta.total_seconds() * 1000) < 2100
        assert bt.get_tick_count() >= 35
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.SUCCESS'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_long_running_hello_world_dave(self):
        mock.reset_mock()
        bt = BehaviorTree()
        assert bt.get_tick_count() == 0
        bt.set_tick_rate_ms(50)
        start = datetime.now()
        bt.run(LongRunningHelloWorldAction, '"Dave"')
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1900
        assert int(delta.total_seconds() * 1000) < 2100
        assert bt.get_tick_count() >= 35
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: abort'),  # noqa: E501
                                       call('abort_handler LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == ''

    def test_multi_tick_hello_world(self):
        mock.reset_mock()
        bt = BehaviorTree()
        assert bt.get_tick_count() == 0
        bt.set_tick_rate_ms(50)
        start = datetime.now()
        bt.run(MultiTickHelloWorldAction)
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 180
        assert int(delta.total_seconds() * 1000) < 220
        assert bt.get_tick_count() == 4
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 1)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 2)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 3)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('__del__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_multi_tick_throtteled_hello_world(self):
        mock.reset_mock()
        bt = BehaviorTree()
        start = datetime.now()
        bt.run(MultiTickThrottledHelloWorldAction)
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
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''
