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

import gc
import sys
import pytest

from carebt.abstractLogger import LogLevel

from tests.actionNodes import AddTwoNumbersLongRunnungActionWithAbort
from tests.actionNodes import HelloWorldAction

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.behaviorTreeRunner import RootNode
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode


class TestBehaviorTreeRunner:

    ########################################################################

    # The 'serial' marker is registered in pytest.ini and excluded in vscode
    # .vscode/setting.json
    @pytest.mark.serial
    def test_BehaviorTreeRunner_cleanup(self):
        """
        Tests if after the the bt execution all careBT nodes are cleaned up,
        expect the RootNode which remains, but is reused by the next call of
        run.

        """

        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.OFF)
        bt_runner.run(HelloWorldAction)
        bt_runner.run(AddTwoNumbersLongRunnungActionWithAbort, '100 3 5 => ?result')
        bt_runner.run(AddTwoNumbersLongRunnungActionWithAbort, '1500 3 5 => ?result')
        assert not hasattr(bt_runner._instance, '_result')
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == 'TIMEOUT'
        node_count = 0
        for o in gc.get_objects().copy():
            if(isinstance(o, TreeNode)):
                print('--------------------------------------')
                print(o)
                print('sys.getrefcount(o) = {}'.format(sys.getrefcount(o)))
                node_count += 1
                assert isinstance(o, RootNode)
        assert node_count == 1
