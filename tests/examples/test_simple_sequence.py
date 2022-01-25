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
from carebt.examples.simple_sequence import CreateRandomNumberAction
from carebt.examples.simple_sequence import PrintNumberAction
from carebt.examples.simple_sequence import SimpleSequence1
from carebt.examples.simple_sequence import SimpleSequence2
from carebt.examples.simple_sequence import SimpleSequence3
from carebt.nodeStatus import NodeStatus


class TestSimpleSequence1:

    @patch('sys.stdout', new_callable=StringIO)
    def test_CreateRandomNumberAction(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(CreateRandomNumberAction, '=> ?x')
        regex = re.compile(r'CreateRandomNumberAction: number = [0-9]+\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_PrintNumberAction(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(PrintNumberAction, '5')
        regex = re.compile(r'PrintNumberAction: number = 5\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleSequence1(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleSequence1, '=> ?x')
        regex = re.compile(r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'AddTwoNumbersAction: calculating: [0-9]+ \+ [0-9]+ = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleSequence2(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleSequence2, '5 => ?x')
        regex = re.compile(r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'AddTwoNumbersAction: calculating: [0-9]+ \+ [0-9]+ = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n'
                           + r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'AddTwoNumbersAction: calculating: [0-9]+ \+ [0-9]+ = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_SimpleSequence3(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SimpleSequence3)
        regex = re.compile(r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'AddTwoNumbersAction: calculating: [0-9]+ \+ [0-9]+ = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n'
                           + r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'AddTwoNumbersAction: calculating: [0-9]+ \+ [0-9]+ = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n'
                           + r'CreateRandomNumberAction: number = [0-9]+\n'
                           + r'AddTwoNumbersAction: calculating: [0-9]+ \+ [0-9]+ = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n'
                           + r'PrintNumberAction: number = [0-9]+\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
