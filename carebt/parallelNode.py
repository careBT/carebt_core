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
from typing import List

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.controlNode import ControlNode
from carebt.executionContext import ExecutionContext
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode


class ParallelNode(ControlNode, ABC):
    """The careBT `ParallelNode` class.

    In a `ParallelNode` the added child nodes are executed in parallel at the same time.
    A `ParallelNode` completes with `SUCCESS` if equal or more than `success_threshold`
    children complete with `SUCCESS` or `FIXED`.

    If as many children as necessary to beeing able to reach the `success_threshold` already
    completed with `FAILURE` or `ABORTED` the `ParallelNode` completes with `FAILURE` and sets
    its contingency_message to the contingency_message of the child which failed last. If two
    children fail in the same tick, the contingency_message of the latter one is used!

    The `ParallelNode` forwards the ticks to all children in a quasi-parallel manner. If
    the `ParallelNode` gets ticked, it ticks the children in the order they were added - but
    within the same received tick.

    Parameters
    ----------
    bt_runner: 'BehaviorTreeRunner'
        The behavior tree runner which started the tree.
    success_threshold: int
        Threshold how many of the children should complete with `SUCCESS`
        or `FIXED` that the `ParallelNode` completes with `SUCCESS`.
    params: str
        The input/Output parameters of the node
        e.g. '?x ?y => ?z'

    """

    def __init__(self, bt_runner: 'BehaviorTreeRunner',
                 success_threshold: int, params: str = None):
        """Init the `ParallelNode` with bt_runner, success_threshold and params."""
        super().__init__(bt_runner, params)

        self.__last_child_contingency_msg = ''

        # list for the child nodes
        self._child_ec_list: List[ExecutionContext] = []
        self._created_child_size = 0

        self._success_threshold = success_threshold
        self._success_count = 0
        self._fail_count = 0

    # PROTECTED

    def _internal_create_child_nodes(self) -> None:
        if((self.get_status() == NodeStatus.IDLE
            or self.get_status() == NodeStatus.RUNNING
            or self.get_status() == NodeStatus.SUSPENDED)
           and self._created_child_size < len(self._child_ec_list)):
            for _ in range(len(self._child_ec_list) - self._created_child_size):
                child_ec = self._child_ec_list[self._created_child_size]
                # create node instance
                child_ec.instance = child_ec.node(self._internal_get_bt_runner())
                self._internal_bind_out_params(child_ec)
                self._internal_bind_in_params(child_ec)
                child_ec.instance.on_init()
                self._created_child_size += 1

    def _internal_tick_child_nodes(self, tick: bool) -> None:
        if(tick is True):
            for self._child_ptr, child_ec in enumerate(self._child_ec_list[:]):
                if(child_ec.instance is not None):
                    self._internal_bind_in_params(child_ec)
                    self._internal_tick_child(child_ec)
                    self._internal_apply_contingencies(child_ec)
                    if(child_ec.instance is not None):
                        self._internal_bind_out_params(child_ec)
                        cur_child_state = child_ec.instance.get_status()
                        if(cur_child_state == NodeStatus.SUCCESS
                           or cur_child_state == NodeStatus.FIXED):
                            child_ec.instance.on_delete()
                            child_ec.instance = None
                            self._success_count += 1
                        elif(cur_child_state == NodeStatus.FAILURE
                             or cur_child_state == NodeStatus.ABORTED):
                            self.__last_child_contingency_msg = child_ec.instance\
                                                                .get_contingency_message()
                            child_ec.instance.on_delete()
                            child_ec.instance = None
                            self._fail_count += 1

    def _internal_prepare_next_tick(self) -> None:
        if(self.get_status() != NodeStatus.ABORTED):
            if(self._success_count >= self._success_threshold):
                self.get_logger().debug(f'_success_count >= _success_threshold -- '
                                        + f'{self._success_count} >= {self._success_threshold}')
                self.set_status(NodeStatus.SUCCESS)
            elif(self._fail_count >
                 len(self._child_ec_list) - self._success_threshold):
                self.get_logger().debug('_fail_count > len(_current_children) - '
                                        + f'_success_threshold -- {self._fail_count} > '
                                        + f'{len(self._child_ec_list)} - '
                                        + f'{self._success_threshold}')
                self.set_status(NodeStatus.FAILURE)
                self.set_contingency_message(self.__last_child_contingency_msg)

            if(self.get_status() == NodeStatus.SUCCESS
               or self.get_status() == NodeStatus.FAILURE):
                # abort children if RUNNING or SUSPENDED
                for child_ec in self._child_ec_list:
                    if(child_ec.instance is not None and
                       (child_ec.instance.get_status() == NodeStatus.RUNNING or
                            child_ec.instance.get_status() == NodeStatus.SUSPENDED)):
                        child_ec.instance._internal_on_abort()
                        child_ec.instance.on_delete()
                        child_ec.instance = None

    def _internal_on_abort(self) -> None:
        super()._internal_on_abort()
        self.get_logger().info(f'aborting {self.__class__.__name__}')
        if(self._child_ec_list[self._child_ptr].instance is not None):
            self.set_status(NodeStatus.ABORTED)
            self.set_contingency_message(self._child_ec_list[self._child_ptr]
                                         .instance.get_contingency_message())
        # abort children if RUNNING or SUSPENDED
        for child_ec in self._child_ec_list:
            if(child_ec.instance is not None and
               (child_ec.instance.get_status() == NodeStatus.RUNNING or
                    child_ec.instance.get_status() == NodeStatus.SUSPENDED)):
                child_ec.instance._internal_on_abort()
                child_ec.instance.on_delete()
                child_ec.instance = None
        self.on_abort()

    # PUBLIC

    def set_success_threshold(self, success_threshold: int) -> None:
        """Set the success_threshold.

        Parameters
        ----------
        success_threshold: int
            Threshold how many of the children should complete with `SUCCESS`
            or `FIXED` that the `ParallelNode` completes with `SUCCESS`.

        """
        self._success_threshold = success_threshold

    def get_success_threshold(self) -> int:
        """Return the success_threshold.

        Returns
        -------
        success_threshold: int
            The success_threshold

        """
        return self._success_threshold

    def add_child(self, node: TreeNode, params: str = None) -> None:
        """Add a child node.

        Parameters
        ----------
        node: TreeNode
            The node to be added

        params: str (Default=None)
            The parameters of the added child node

        """
        self._child_ec_list.append(ExecutionContext(self, node, params))

    def remove_child(self, pos: int) -> None:
        """Remove a child node.

        Remove the child node at the provided position. The positions are in
        the order the children are added starting with zero.

        Parameters
        ----------
        pos: int
            Position of the child to remove

        """
        self._created_child_size -= 1
        if(self._child_ec_list[pos].instance is not None):
            self._child_ec_list[pos].instance._internal_on_abort()
            self._child_ec_list[pos].instance.on_delete()
            self._child_ec_list[pos].instance = None
        del self._child_ec_list[pos]

    def remove_all_children(self) -> None:
        """Remove all child nodes."""
        self._success_count = 0
        self._fail_count = 0

        for _ in range(self._created_child_size):
            self.remove_child(0)
