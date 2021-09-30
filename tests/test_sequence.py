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

from tests.global_mock import mock
from tests.helloActions import HelloWorldAction
from tests.helloActions import LongRunningHelloWorldAction
from tests.helloActions import SayHelloAction

from unittest.mock import call

from carebt.abstractLogger import LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode

########################################################################


class SimpleSequence(SequenceNode):

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?name')
        mock('__init__ {}'.format(self.__class__.__name__))

    def _on_init(self) -> None:
        mock('_on_init')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class LongRunningSequence(SequenceNode):

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?name')
        mock('__init__ {}'.format(self.__class__.__name__))

    def _on_init(self) -> None:
        mock('_on_init')
        self.add_child(LongRunningHelloWorldAction, '?name')

        self.attach_contingency_handler(LongRunningHelloWorldAction,
                                        [NodeStatus.SUCCESS],
                                        '*',
                                        self.contingency_handler_success)

        self.attach_contingency_handler(LongRunningHelloWorldAction,
                                        [NodeStatus.FAILURE],
                                        'BOB_IS_NOT_ALLOWED',
                                        self.contingency_handler_failure_bob)

        self.attach_contingency_handler(LongRunningHelloWorldAction,
                                        [NodeStatus.FAILURE],
                                        'CHUCK_IS_NOT_ALLOWED',
                                        self.contingency_handler_failure_chuck)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

    def _on_abort(self) -> None:
        mock('_on_abort LongRunningSequence')

    def contingency_handler_success(self):
        mock('contingency_handler_success')

    def contingency_handler_failure_bob(self):
        mock('contingency_handler_failure_bob')
        self.abort()

    def contingency_handler_failure_chuck(self):
        mock('contingency_handler_failure_chuck')

########################################################################


class TestSequenceNode:

    def test_sequence(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.run(SimpleSequence, '"Dave"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SimpleSequence'),
                                       call('_on_init'),
                                       call('__init__ HelloWorldAction'),
                                       call('_on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('_on_tick - Dave'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('_on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SimpleSequence'),
                                       call('bt finished')]
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_sequence_failure(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.run(SimpleSequence, '"Bob"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SimpleSequence'),
                                       call('_on_init'),
                                       call('__init__ HelloWorldAction'),
                                       call('_on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('_on_tick - Bob'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SimpleSequence'),
                                       call('bt finished')]
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'BOB_IS_NOT_ALLOWED'

    def test_tick_rate_and_count(self):
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        assert bt_runner.get_tick_count() == 0
        bt_runner.set_tick_rate_ms(1000)
        start = datetime.now()
        bt_runner.run(SimpleSequence, '"Dave"')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 2950
        assert int(delta.total_seconds() * 1000) < 3050
        assert bt_runner.get_tick_count() == 3

    def test_long_running_sequence_success(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.run(LongRunningSequence, '"Alice"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningSequence'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.SUCCESS'),  # noqa: E501
                                       call('contingency_handler_success'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_long_running_sequence_failure_chuck(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.run(LongRunningSequence, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningSequence'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.FAILURE'),  # noqa: E501
                                       call('contingency_handler_failure_chuck'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'CHUCK_IS_NOT_ALLOWED'

    def test_long_running_sequence_failure_bob(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.run(LongRunningSequence, '"Bob"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningSequence'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.FAILURE'),  # noqa: E501
                                       call('contingency_handler_failure_bob'),  # noqa: E501
                                       call('_on_abort LongRunningSequence'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == 'BOB_IS_NOT_ALLOWED'
