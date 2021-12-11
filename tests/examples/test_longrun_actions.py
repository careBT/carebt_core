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
from carebt.examples.longrun_actions import AddTwoNumbersLongRunningAction
from carebt.examples.longrun_actions import AddTwoNumbersMultiTickAction
from carebt.examples.longrun_actions import AddTwoNumbersMultiTickActionWithTimeout
from carebt.nodeStatus import NodeStatus


class TestLongrunActions:

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersMultiTickAction_1tick(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersMultiTickAction, '1 3 4 => ?result')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersMultiTickAction: DONE 3 \+ 4 = 7\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersMultiTickAction_3ticks(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersMultiTickAction, '3 3 4 => ?result')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersMultiTickAction: \(tick_count = 1/3\)\n'
                           r'AddTwoNumbersMultiTickAction: \(tick_count = 2/3\)\n'
                           r'AddTwoNumbersMultiTickAction: DONE 3 \+ 4 = 7\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    ########################################################################

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersMultiTickActionWithTimeout_1tick(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersMultiTickActionWithTimeout, '1 3 4 => ?result')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersMultiTickActionWithTimeout: DONE 3 \+ 4 = 7\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersMultiTickActionWithTimeout_3ticks(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersMultiTickActionWithTimeout, '3 3 4 => ?result')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/3\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 2/3\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: DONE 3 \+ 4 = 7\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersMultiTickActionWithTimeout_15ticks(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.OFF)
        bt_runner.run(AddTwoNumbersMultiTickActionWithTimeout, '15 3 4 => ?result')
        assert bt_runner.get_status() == NodeStatus.ABORTED
        assert bt_runner.get_contingency_message() == 'TIMEOUT'
        regex = re.compile(r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 2/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 3/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 4/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 5/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 6/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 7/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 8/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 9/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 10/15\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: on_timeout\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: on_abort\n')
        assert bool(re.match(regex, mock_print.getvalue()))

########################################################################

    @patch('sys.stdout', new_callable=StringIO)
    def test_AddTwoNumbersLongRunningAction_ok(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersLongRunningAction, '2000 3 4 => ?result')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersLongRunningAction: calculating 2000 ms ...\n'
                           r'AddTwoNumbersLongRunningAction: DONE 3 \+ 4 = 7\n')
        assert bool(re.match(regex, mock_print.getvalue()))
