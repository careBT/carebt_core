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

from carebt.behaviorTree import BehaviorTree
from carebt.controlNode import ControlNode
from carebt.executionContext import ExecutionContext
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode


class ParallelNode(ControlNode):  # abstract

    def __init__(self, bt: 'BehaviorTree', success_threshold: int, params: str = None):
        super().__init__(bt, params)

        # list for the child nodes
        self._child_ec_list = []

        self._success_threshold = success_threshold
        self._success_count = 0
        self._fail_count = 0

    def _on_tick(self) -> None:
        self.get_logger().info('ticking {}'.format(self.__class__.__name__))

        ################################################
        # create all children
        if(self.get_status() == NodeStatus.IDLE):
            for self._child_ptr, child_ec in enumerate(self._child_ec_list):
                # create node instance
                child_ec.instance = child_ec.node_as_class(self.get_bt())
            self.set_status(NodeStatus.RUNNING)

        ################################################
        # tick all children
        for self._child_ptr, child_ec in enumerate(self._child_ec_list):
            self._tick_child(child_ec)
            self._apply_rules(child_ec)
            cur_child_state = child_ec.instance.get_status()
            if(cur_child_state == NodeStatus.SUCCESS):
                child_ec.instance = None
                self._success_count += 1
            elif(cur_child_state == NodeStatus.FAILURE or
                 cur_child_state == NodeStatus.ABORTED):
                child_ec.instance = None
                self._fail_count += 1

        ################################################
        # finally, check how to proceed
        if(self.get_status() != NodeStatus.ABORTED):
            if(self._success_count >= self._success_threshold):
                self.get_logger().debug('_success_count >= _success_threshold -- {} >= {}'
                                        .format(self._success_count,
                                                self._success_threshold))
                self.set_status(NodeStatus.SUCCESS)
            elif(self._fail_count >
                 len(self._child_ec_list) - self._success_threshold):
                self.get_logger().debug('_fail_count > len(_current_children) - '
                                        '_success_threshold -- {} > {} - {}'
                                        .format(self._fail_count,
                                                len(self._child_ec_list),
                                                self._success_threshold))
                self.set_status(NodeStatus.FAILURE)

    def _on_abort(self) -> None:
        self.get_logger().info('aborting {}'.format(self.__class__.__name__))
        # abort children if RUNNING or SUSPENDED
        for child_ec in self._child_ec_list:
            if(child_ec.instance is not None and
               (child_ec.instance.get_status() == NodeStatus.RUNNING or
                    child_ec.instance.get_status() == NodeStatus.SUSPENDED)):
                child_ec.instance._on_abort()
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
