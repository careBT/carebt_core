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

from tests.global_mock import mock
from tests.helloActions import LongRunningHelloWorldAction
from tests.helloActions import MultiTickHelloWorldAction

from unittest.mock import call

from carebt.abstractLogger import LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode

########################################################################


class MultiTickSequence(SequenceNode):

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?name')
        mock('__init__ {}'.format(self.__class__.__name__))

    def _on_init(self) -> None:
        mock('_on_init')
        self.add_child(MultiTickHelloWorldAction)

        self.attach_contingency_handler(MultiTickHelloWorldAction,
                                        [NodeStatus.SUCCESS],
                                        '*',
                                        self.contingency_handler_success)

        self.attach_contingency_handler(MultiTickHelloWorldAction,
                                        [NodeStatus.RUNNING],
                                        '*',
                                        self.contingency_handler_running)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

    def contingency_handler_success(self):
        mock('contingency_handler_success')

    def contingency_handler_running(self):
        mock('contingency_handler_running')

########################################################################


class LongRunningHelloWorldSequence(SequenceNode):

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
                                        [NodeStatus.SUSPENDED],
                                        '*',
                                        self.contingency_handler_suspended)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

    def contingency_handler_success(self):
        mock('contingency_handler_success')

    def contingency_handler_suspended(self):
        mock('contingency_handler_suspended')

########################################################################


class TestActionNode:

    def test_multi_tick_sequence(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.run(MultiTickSequence)
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ MultiTickSequence'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('__init__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 1)'),  # noqa: E501
                                       call('contingency_handler_running'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 2)'),  # noqa: E501
                                       call('contingency_handler_running'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 3)'),  # noqa: E501
                                       call('contingency_handler_running'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('contingency_handler_success'),  # noqa: E501
                                       call('__del__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('__del__ MultiTickSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    def test_long_running_sequence(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        bt_runner.set_tick_rate_ms(100)
        bt_runner.run(LongRunningHelloWorldSequence, '"Alice"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningHelloWorldSequence'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('contingency_handler_suspended'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.SUCCESS'),  # noqa: E501
                                       call('contingency_handler_success'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
