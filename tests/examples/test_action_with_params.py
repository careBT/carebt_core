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

from io import StringIO
import re
from unittest.mock import patch

from carebt.abstractLogger import LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.examples.action_with_params import AddTwoNumbersAction
from carebt.nodeStatus import NodeStatus


class TestActionWithParams:

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersAction_ok(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersAction, '1 2 => ?x')
        regex = re.compile(r'AddTwoNumbersAction: calculating: 1 \+ 2 = 3\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersAction_one_missing(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.OFF)
        bt_runner.run(AddTwoNumbersAction, '1 => ?x')
        regex = re.compile(r'AddTwoNumbersAction: calculating: 1 \+ 0 = 1\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersAction_both_missing(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.OFF)
        bt_runner.run(AddTwoNumbersAction, '=> ?x')
        regex = re.compile(r'AddTwoNumbersAction: calculating: 0 \+ 0 = 0\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
