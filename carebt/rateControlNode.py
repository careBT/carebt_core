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


class RateControlNode(ControlNode, ABC):
    """The careBT `RateControlNode` class.

    The `RateControlNode` is a special node to throttle the tick rate of its
    only child. It is similar to the `throttle` mechanism of the `ActionNode`.
    But the `ActionNode` needs to be already implemented with the throttling.
    The `RateControlNode` on the other hand can throttle all careBT nodes, such
    as `SequenceNode`, `ParallelNode` or as already mentioned an `ActionNode`.
    For the latter one this is especially useful if the implementation of the
    custon `ActionNode` should or could not be modified.

    Parameters
    ----------
    bt_runner: 'BehaviorTreeRunner'
        The behavior tree runner which started the tree.
    rate_ms: int
        Throttling rate in milliseconds
    params: str
        The input/Output parameters of the node
        e.g. '?x ?y => ?z'

    """

    def __init__(self, bt_runner: 'BehaviorTreeRunner', throttle_ms: int, params: str = None):
        """Init the `ActionNode` with bt_runner,rate_ms and params."""
        super().__init__(bt_runner, params)

        self._throttle_ms = throttle_ms
        self.set_status(NodeStatus.IDLE)

    # PROTECTED

    def _internal_create_child_nodes(self) -> None:
        if(self._child_ec_list[0].instance is None):
            # create node instance
            self._child_ec_list[0].instance = \
                self._child_ec_list[0].node(self._internal_get_bt_runner())
            self._internal_bind_in_params(self._child_ec_list[self._child_ptr])
            self._child_ec_list[0].instance.on_init()

    def _internal_tick_child_nodes(self, tick: bool) -> None:
        if(tick is True):
            self._internal_tick_child(self._child_ec_list[self._child_ptr])

        self._internal_bind_out_params(self._child_ec_list[self._child_ptr])
        self._internal_apply_contingencies(self._child_ec_list[self._child_ptr])

    def _internal_prepare_next_tick(self) -> None:
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
            self.get_logger().info(f'finished {self.__class__.__name__}')
            self._child_ec_list[0].instance.on_delete()
            self._child_ec_list[0].instance = None

    def _internal_on_abort(self) -> None:
        super()._internal_on_abort()
        self.get_logger().info(f'aborting {self.__class__.__name__}')
        if(self._child_ec_list[self._child_ptr].instance is not None):
            self.set_status(NodeStatus.ABORTED)
            self.set_contingency_message(self._child_ec_list[self._child_ptr]
                                         .instance.get_contingency_message())
        # abort child if RUNNING or SUSPENDED
        if(self._child_ec_list[0].instance.get_status() == NodeStatus.RUNNING or
           self._child_ec_list[0].instance.get_status() == NodeStatus.SUSPENDED):
            self._child_ec_list[0].instance._internal_on_abort()

        if(self._child_ec_list[0].instance is not None):
            self._child_ec_list[0].instance.on_delete()
            self._child_ec_list[0].instance = None
        self.on_abort()

    # PUBLIC

    def set_child(self, node: TreeNode, params: str = None) -> None:
        """Set the child node.

        Set the child node to this `RateControlNode`. There can only be one child at
        the same time.

        Parameters
        ----------
        node: TreeNode
            The node to be set

        params: str (Default=None)
            The parameters of the added child node

        """
        self._child_ptr = 0
        self._child_ec_list.clear()
        self._child_ec_list.append(ExecutionContext(self, node, params))
