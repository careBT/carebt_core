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


class FallbackNode(ControlNode, ABC):
    """The careBT `FallbackNode` class.

    In a `FallbackNode` the added child nodes are executed one after another until
    one node completes with `SUCCESS` or `FIXED`. The child nodes are executed in the
    order they were added to the sequence. If all children complete with `FAILURE`
    or `ABORTED` the `FallbackNode` completes with `FAILURE` or `ABORTED`.

    The `FallbackNode` forwards the ticks to the currently executing child - which can
    only be one at a time - if the status is `RUNNING`. If the status is `SUSPENDED`
    the ticks are not forwarded.

    Parameters
    ----------
    bt_runner: 'BehaviorTreeRunner'
        The behavior tree runner which started the tree.
    params: str
        The input/Output parameters of the node
        e.g. '?x ?y => ?z'

    """

    def __init__(self, bt_runner: 'BehaviorTreeRunner', params: str = None):
        """Init the `FallbackNode` with bt_runner and params."""
        super().__init__(bt_runner, params)

    # PROTECTED

    def _internal_create_child_nodes(self) -> None:
        if(self._child_ec_list[self._child_ptr].instance is None):
            # create node instance
            self._child_ec_list[self._child_ptr].instance = \
                self._child_ec_list[self._child_ptr].node(self._internal_get_bt_runner())
            self._internal_bind_in_params(self._child_ec_list[self._child_ptr])
            self._child_ec_list[self._child_ptr].instance.on_init()

    def _internal_tick_child_nodes(self, tick: bool) -> None:
        if(tick is True):
            self._internal_tick_child(self._child_ec_list[self._child_ptr])

        self._internal_bind_out_params(self._child_ec_list[self._child_ptr])
        self._internal_apply_contingencies(self._child_ec_list[self._child_ptr])

    def _internal_prepare_next_tick(self) -> None:
        if(self.get_status() == NodeStatus.RUNNING):
            if self._child_ec_list[self._child_ptr].instance is not None:
                cur_child_state = self._child_ec_list[self._child_ptr].instance.get_status()

                # if the current child tick returned with SUCCESS or FIXED
                if(cur_child_state == NodeStatus.SUCCESS
                   or cur_child_state == NodeStatus.FIXED):
                    self.set_status(cur_child_state)
                    self.set_contingency_message(self._child_ec_list[self._child_ptr]
                                                 .instance.get_contingency_message())

                cur_child_state = self._child_ec_list[self._child_ptr].instance.get_status()
                # if the current child tick returned with FAILURE or ABORTED
                if(cur_child_state == NodeStatus.FAILURE
                   or cur_child_state == NodeStatus.ABORTED):
                    self._contingency_message = self._child_ec_list[self._child_ptr]\
                        .instance.get_contingency_message()
                    if(self._child_ec_list[self._child_ptr].instance is not None):
                        self._child_ec_list[self._child_ptr].instance.on_delete()
                        self._child_ec_list[self._child_ptr].instance = None
                    # check if there is at least one more node to run
                    if(self._child_ptr + 1 < len(self._child_ec_list)):
                        self._child_ptr += 1
                    else:
                        # no more nodes to run -> sequence = SUCCESS
                        self.set_status(cur_child_state)
                        self.set_contingency_message(self._contingency_message)

        if(self.get_status() == NodeStatus.SUCCESS
           or self.get_status() == NodeStatus.FAILURE
           or self.get_status() == NodeStatus.ABORTED
           or self.get_status() == NodeStatus.FIXED):
            self.get_logger().info(f'finished {self.__class__.__name__}')
            if(self._child_ec_list[self._child_ptr].instance is not None):
                self._child_ec_list[self._child_ptr].instance.on_delete()
                self._child_ec_list[self._child_ptr].instance = None

    def _internal_on_abort(self) -> None:
        super()._internal_on_abort()
        self.get_logger().info(f'aborting {self.__class__.__name__}')
        if(self._child_ec_list[self._child_ptr].instance is not None):
            self.set_status(NodeStatus.ABORTED)
            self.set_contingency_message(self._child_ec_list[self._child_ptr]
                                         .instance.get_contingency_message())
        # abort current child if RUNNING or SUSPENDED
        if(self._child_ec_list[self._child_ptr].instance.get_status() == NodeStatus.RUNNING or
           self._child_ec_list[self._child_ptr].instance.get_status() == NodeStatus.SUSPENDED):
            self._child_ec_list[self._child_ptr].instance._internal_on_abort()

        if(self._child_ec_list[self._child_ptr].instance is not None):
            self._child_ec_list[self._child_ptr].instance.on_delete()
            self._child_ec_list[self._child_ptr].instance = None
        self.on_abort()

    # PUBLIC

    def append_child(self, node: TreeNode, params: str = None) -> None:
        """Append a child.

        Append a child node at the end of the sequence of this `FallbackNode`.

        Parameters
        ----------
        node: TreeNode
            The node to be added

        params: str (Default=None)
            The parameters of the added child node

        """
        self._child_ec_list.append(ExecutionContext(self, node, params))

    def insert_child_after_current(self, node: TreeNode, params: str = None) -> None:
        """Insert a child node after the current.

        Insert a child node right after the currently executing child node. NOTE: When
        inserting more than one node, they should be inserted in reverse order. This is
        because each node will be inserted right after the currently executing!

        Parameters
        ----------
        node: TreeNode
            The node to be added

        params: str (Default=None)
            The parameters of the added child node

        """
        # if all children were removed
        if(len(self._child_ec_list) != 0
           and self._child_ec_list[self._child_ptr].instance is None
           and self._child_ptr == 0):
            self._child_ec_list.insert(0, ExecutionContext(self, node, params))
        else:
            self._child_ec_list.insert(self._child_ptr + 1, ExecutionContext(self, node, params))

    def remove_all_children(self) -> None:
        """Remove all child nodes.

        Remove all child nodes from the `FallbackNode`. This is typically done in a contingency
        handler to modify the current execution sequence and adjust it to the current situation.
        New children which should be executed afterwards can be added with `append_child` or
        `insert_child_after_current`.
        """
        if(len(self._child_ec_list) != 0
           and self._child_ec_list[self._child_ptr].instance is not None):
            self._child_ec_list[self._child_ptr].instance.on_delete()
        self._child_ec_list.clear()
        self._child_ptr = 0
