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

from typing import TYPE_CHECKING

from carebt.controlNode import ControlNode
from carebt.executionContext import ExecutionContext
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode

if TYPE_CHECKING:
    from carebt.behaviorTreeRunner import BehaviorTreeRunner  # pragma: no cover


class SequenceNode(ControlNode):  # abstract

    def __init__(self, bt_runner: 'BehaviorTreeRunner', params: str = None):
        super().__init__(bt_runner, params)

    def _on_tick(self) -> None:
        self.get_logger().info('ticking {}'.format(self.__class__.__name__))
        self.set_status(NodeStatus.RUNNING)

        ################################################
        # if there is no current child to be ticked, create one
        if(self._child_ec_list[self._child_ptr].instance is None):
            # create node instance
            self._child_ec_list[self._child_ptr].instance = \
                self._child_ec_list[self._child_ptr].node_as_class(self.get_bt_runner())
            self._bind_in_params(self._child_ec_list[self._child_ptr])

        # tick child
        self._tick_child(self._child_ec_list[self._child_ptr])
        self._apply_rules(self._child_ec_list[self._child_ptr])

        ################################################
        # finally, check how to proceed in the sequence
        if(self.get_status() == NodeStatus.RUNNING):
            cur_child_state = self._child_ec_list[self._child_ptr].instance.get_status()

            # if the current child tick returned with FAILURE or ABORTED
            if(cur_child_state == NodeStatus.FAILURE or
               cur_child_state == NodeStatus.ABORTED):
                self.set_status(cur_child_state)
                self.set_message(self._child_ec_list[self._child_ptr].instance.get_message())

            # if the current child tick returned with SUCCESS
            elif(cur_child_state == NodeStatus.SUCCESS):
                self._bind_out_params(self._child_ec_list[self._child_ptr])
                self._child_ec_list[self._child_ptr].instance = None
                # check if there is at least one more node to run
                if(self._child_ptr + 1 < len(self._child_ec_list)):
                    self._child_ptr += 1
                else:
                    # no more nodes to run -> sequence = SUCCESS
                    self.set_status(NodeStatus.SUCCESS)

        if(self.get_status() == NodeStatus.SUCCESS or
           self.get_status() == NodeStatus.FAILURE or
           self.get_status() == NodeStatus.ABORTED):
            self.get_logger().info('finished {}'.format(self.__class__.__name__))
            self._child_ec_list[self._child_ptr].instance = None

    def _on_abort(self) -> None:
        self.get_logger().info('aborting {}'.format(self.__class__.__name__))
        # abort current child if RUNNING or SUSPENDED
        if(self._child_ec_list[self._child_ptr].instance.get_status() == NodeStatus.RUNNING or
           self._child_ec_list[self._child_ptr].instance.get_status() == NodeStatus.SUSPENDED):
            self._child_ec_list[self._child_ptr].instance._on_abort()
        self.set_status(NodeStatus.ABORTED)
        self.set_message(self._child_ec_list[self._child_ptr].instance.get_message())
        if(self._abort_handler is not None):
            exec('self.{}()'.format(self._abort_handler))

    # add a child to the list
    def add_child(self, child_as_class: TreeNode, params: str = None) -> None:
        self._child_ec_list.append(ExecutionContext(child_as_class, params))

    # remove child by index from the list
    def remove_child(self, pos: int) -> None:
        del self._child_ec_list[pos]
        if(pos <= self._child_ptr):
            self._child_ptr -= 1

    # remove all children from the list
    def remove_all_children(self) -> None:
        self._child_ptr = 0
        self._child_ec_list.clear()

    # remove all susequent children from the list
    def remove_susequent_children(self) -> None:
        for _ in range(self._child_ptr, len(self._child_ec_list) - 1):
            del self._child_ec_list[-1]
