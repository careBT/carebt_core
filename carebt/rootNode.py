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

from abc import ABC

from typing import TYPE_CHECKING

from carebt.controlNode import ControlNode
from carebt.executionContext import ExecutionContext
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode

if TYPE_CHECKING:
    from carebt.behaviorTreeRunner import BehaviorTreeRunner  # pragma: no cover


class RootNode(ControlNode, ABC):

    def __init__(self, bt_runner: 'BehaviorTreeRunner', params: str = None):
        super().__init__(bt_runner, params)

    # PROTECTED

    def _internal_on_tick(self) -> None:
        self.set_status(NodeStatus.RUNNING)

        ################################################
        # create instance
        if(self._child_ec_list[0].instance is None):
            # create node instance
            self._child_ec_list[0].instance = \
                self._child_ec_list[0].node(self._internal_get_bt_runner())
            self._internal_bind_in_params(self._child_ec_list[self._child_ptr])
            self._child_ec_list[0].instance.on_init()

        # tick child
        self._internal_tick_child(self._child_ec_list[0])

        # finally, check how to proceed
        if(self.get_status() == NodeStatus.RUNNING):
            cur_child_state = self._child_ec_list[0].instance.get_status()

            # if the current child tick returned with FAILURE or ABORTED
            if(cur_child_state == NodeStatus.FAILURE or
                    cur_child_state == NodeStatus.ABORTED):
                self.set_status(cur_child_state)
                self.set_contingency_message(self._child_ec_list[0]
                                             .instance.get_contingency_message())

            # if the current child tick returned with SUCCESS or FIXED
            elif(cur_child_state == NodeStatus.SUCCESS
                 or cur_child_state == NodeStatus.FIXED):
                # if current child state is FIXED -> do not bind out_params
                # as the 'fix' implementation is done in the contingency-handler
                if(cur_child_state != NodeStatus.FIXED):
                    self._internal_bind_out_params(self._child_ec_list[self._child_ptr])
                self.set_status(NodeStatus.SUCCESS)
                self.set_contingency_message(self._child_ec_list[0]
                                             .instance.get_contingency_message())

        if(self.get_status() == NodeStatus.SUCCESS
           or self.get_status() == NodeStatus.FAILURE
           or self.get_status() == NodeStatus.ABORTED
           or self.get_status() == NodeStatus.FIXED):
            self._child_ec_list[0].instance.on_delete()
            # forward status and contingency-message to RootNode
            self.set_status(self._child_ec_list[0].instance.get_status())
            self.set_contingency_message(self._child_ec_list[0]
                                         .instance.get_contingency_message())
            # forward contingency-history to RootNode
            for entry in self._child_ec_list[0].instance.get_contingency_history():
                self._internal_append_to_contingency_history(entry)
            self._child_ec_list[0].instance = None

    # PUBLIC

    def set_child(self, node: TreeNode, params: str = None) -> None:
        self._child_ptr = 0
        self._child_ec_list.clear()
        self._child_ec_list.append(ExecutionContext(self, node, params))
