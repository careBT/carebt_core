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

from typing import TYPE_CHECKING

from carebt.controlNode import ControlNode
from carebt.executionContext import ExecutionContext
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode

if TYPE_CHECKING:
    from carebt.behaviorTree import BehaviorTree


class RateControlNode(ControlNode):  # abstract

    def __init__(self, bt: 'BehaviorTree', rate_ms: int, params: str = None):
        super().__init__(bt, params)

        self.__rate_ms = rate_ms
        self.__last_ts = datetime.min
        self.set_status(NodeStatus.IDLE)

    def _on_tick(self) -> None:
        self.get_logger().info(1, 'ticking {}'.format(self.__class__.__name__))
        self.set_status(NodeStatus.RUNNING)

        ################################################
        # create instance
        if(self._child_ec_list[0].instance is None):
            # create node instance
            self._child_ec_list[0].instance = \
                self._child_ec_list[0].node_as_class(self.get_bt())

        # tick child if __rate_ms has elapsed
        current_ts = datetime.now()
        if(int((current_ts - self.__last_ts).total_seconds() * 1000) >= self.__rate_ms):
            self._tick_child(self._child_ec_list[0])
            self._apply_rules(self._child_ec_list[0])
            self.__last_ts = current_ts
        else:
            self._bind_out_params(self._child_ec_list[0])
            self._apply_rules(self._child_ec_list[0])

        ################################################
        # finally, check how to proceed in the sequence
        if(self.get_status() == NodeStatus.RUNNING):
            cur_child_state = self._child_ec_list[0].instance.get_status()

            # if the current child tick returned with FAILURE or ABORTED
            if(cur_child_state == NodeStatus.FAILURE or
                    cur_child_state == NodeStatus.ABORTED):
                self.set_status(cur_child_state)
                self.set_message(self._child_ec_list[0].instance.get_message())

            # if the current child tick returned with SUCCESS
            elif(cur_child_state == NodeStatus.SUCCESS):
                self.set_status(NodeStatus.SUCCESS)

        if(self.get_status() == NodeStatus.SUCCESS or
                self.get_status() == NodeStatus.FAILURE or
                self.get_status() == NodeStatus.ABORTED):
            self.get_logger().info(1, 'finished {}'.format(self.__class__.__name__))
            self._child_ec_list[0].instance = None

    def _on_abort(self) -> None:
        self.get_logger().info(1, 'aborting {}'.format(self.__class__.__name__))
        # abort child if RUNNING or SUSPENDED
        if(self._child_ec_list[0].instance.get_status() == NodeStatus.RUNNING or
           self._child_ec_list[0].instance.get_status() == NodeStatus.SUSPENDED):
            self._child_ec_list[0].instance._on_abort()
        self.set_status(NodeStatus.ABORTED)
        self.set_message(self._child_ec_list[0].instance.get_message())
        if(self._abort_handler is not None):
            exec('self.{}()'.format(self._abort_handler))

    # set the child
    def set_child(self, child_as_class: TreeNode, params: str = None) -> None:
        self._child_ptr = 0
        self._child_ec_list.clear()
        self._child_ec_list.append(ExecutionContext(child_as_class, params))
