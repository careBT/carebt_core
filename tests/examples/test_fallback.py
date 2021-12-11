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

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.examples.fallback import SimpleFallback
from carebt.nodeStatus import NodeStatus


class TestSimpleFallback:

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleFallback_1(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleFallback, '1 2 3')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersActionWithFailures: calculating: 1 \+ 1 = 2\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleFallback_2(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleFallback, '10 2 3')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersActionWithFailures: calculating: 1 \+ 10 = 11 -> RESULT_TOO_LARGE\n'  # noqa: E501
                           r'AddTwoNumbersActionWithFailures: calculating: 2 \+ 2 = 4\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleFallback_3(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleFallback, '10 20 3')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersActionWithFailures: calculating: 1 \+ 10 = 11 -> RESULT_TOO_LARGE\n'  # noqa: E501
                           r'AddTwoNumbersActionWithFailures: calculating: 2 \+ 20 = 22 -> RESULT_TOO_LARGE\n'  # noqa: E501
                           r'AddTwoNumbersActionWithFailures: calculating: 3 \+ 3 = 6\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleFallback_4(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleFallback, '10 20 30')
        assert bt_runner.get_status() == NodeStatus.FAILURE
        assert bt_runner.get_contingency_message() == 'RESULT_TOO_LARGE'
        regex = re.compile(r'AddTwoNumbersActionWithFailures: calculating: 1 \+ 10 = 11 -> RESULT_TOO_LARGE\n'  # noqa: E501
                           r'AddTwoNumbersActionWithFailures: calculating: 2 \+ 20 = 22 -> RESULT_TOO_LARGE\n'  # noqa: E501
                           r'AddTwoNumbersActionWithFailures: calculating: 3 \+ 30 = 33 -> RESULT_TOO_LARGE\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))
