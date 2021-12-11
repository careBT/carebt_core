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
from carebt.examples.parallel import SimpleParallel
from carebt.nodeStatus import NodeStatus


class TestSimpleParallel:

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleParallel_1(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleParallel, '2 4 6')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/2\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/4\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: DONE 1 \+ 1 = 2\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 2/4\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 2/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 3/4\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 3/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: DONE 2 \+ 2 = 4\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 4/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: on_abort\n')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleParallel_2(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleParallel, '6 4 2')
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/4\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 1/2\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 2/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 2/4\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: DONE 3 \+ 3 = 6\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 3/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 3/4\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: \(tick_count = 4/6\)\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: DONE 2 \+ 2 = 4\n'
                           r'AddTwoNumbersMultiTickActionWithTimeout: on_abort\n')
        assert bool(re.match(regex, mock_print.getvalue()))
