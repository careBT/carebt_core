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
from carebt.examples.helloworld import HelloWorldAction
from carebt.nodeStatus import NodeStatus


class TestHelloWorld:

    @patch('sys.stdout', new_callable=StringIO)
    def test_HelloWorldAction(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(HelloWorldAction)
        assert bt_runner.get_status() == NodeStatus.SUCCESS
        assert bt_runner.get_contingency_message() == ''
        regex = re.compile(r'HelloWorldAction: Hello World !!!\n')
        assert bool(re.match(regex, mock_print.getvalue()))
