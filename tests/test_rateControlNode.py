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
from tests.helloActions import MultiTickHelloWorldAction

from unittest.mock import call

from carebt.abstractLogger import LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from carebt.rateControlNode import RateControlNode

########################################################################


class RateControlledMultiTickHelloWorld(RateControlNode):

    def __init__(self, bt_runner):
        super().__init__(bt_runner, 500)
        mock('__init__ {}'.format(self.__class__.__name__))

    def _on_init(self) -> None:
        mock('_on_init')
        self.set_child(MultiTickHelloWorldAction)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class TestSequenceNode:

    def test_rate_controlled_multi_tick_hello_world(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.INFO)
        start = datetime.now()
        bt_runner.run(RateControlledMultiTickHelloWorld)
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1500
        assert int(delta.total_seconds() * 1000) < 1600
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ RateControlledMultiTickHelloWorld'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('__init__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('_on_init'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 1)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 2)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 3)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('__del__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('__del__ RateControlledMultiTickHelloWorld'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
