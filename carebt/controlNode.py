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
from datetime import datetime
import re
from typing import Callable
from typing import final
from typing import List
from typing import TYPE_CHECKING

from carebt.contingencyHistoryEntry import ContingencyHistoryEntry
from carebt.executionContext import ExecutionContext
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode

if TYPE_CHECKING:
    from carebt.behaviorTreeRunner import BehaviorTreeRunner  # pragma: no cover


class ControlNode(TreeNode, ABC):
    """The careBT `ControlNode` class.

    `ControlNode` is the basic class for all nodes in careBT which provide a
    control flow functionality, like `SequenceNode` and `ParallelNode`.

    """

    def __init__(self, bt_runner: 'BehaviorTreeRunner', params: str = None):
        """Init the `ControlNode` with bt_runner and params."""
        super().__init__(bt_runner, params)

        # list for the child nodes
        self._child_ec_list: List[ExecutionContext] = []

        # the current child pointer
        self._child_ptr = 0

        self._contingency_handler_list = []

        self.set_status(NodeStatus.IDLE)

    # PROTECTED

    def _internal_on_tick(self) -> None:
        if(self.get_status() != NodeStatus.RUNNING):
            self.set_status(NodeStatus.RUNNING)

        # if child list is empty, there is nothing to do
        if(len(self._child_ec_list) == 0):
            return

        # create child nodes
        self._internal_create_child_nodes()

        # _throttle_ms -> tick
        tick: bool = False
        current_ts = datetime.now()
        if(self._throttle_ms is None
           or int((current_ts - self._last_ts).total_seconds() * 1000) >= self._throttle_ms):
            self.bt_runner.get_logger().trace(f'ticking {self.__class__.__name__} '
                                              + f'- {self.get_status()}')
            tick = True
            self._last_ts = current_ts

        # tick child nodes and apply contingency-handler
        self._internal_tick_child_nodes(tick)

        if(tick is True):
            self.on_tick()

        self._internal_prepare_next_tick()

    # @abstractmethod
    def _internal_create_child_nodes(self) -> None:
        raise NotImplementedError

    # @abstractmethod
    def _internal_tick_child_nodes(self, tick: bool) -> None:
        raise NotImplementedError

    # @abstractmethod
    def _internal_prepare_next_tick(self) -> None:
        raise NotImplementedError

    def _internal_bind_in_params(self, child_ec: ExecutionContext) -> None:
        if(len(child_ec.call_in_params) != len(child_ec.instance._internal_get_in_params())):
            self.get_logger().warn(f'{child_ec.node.__name__} takes '
                                   + f'{len(child_ec.instance._internal_get_in_params())} '
                                   + f'argument(s), but {len(child_ec.call_in_params)} '
                                   + f'was/were provided')
        for i, var in enumerate(child_ec.call_in_params):
            if(isinstance(var, str) and len(var) > 0 and var[0] == '?'):
                var = var.replace('?', '_', 1)
                var = getattr(self, var)
            if(i < len(child_ec.instance._internal_get_in_params())):
                setattr(child_ec.instance,
                        child_ec.instance._internal_get_in_params()[i].replace('?', '_', 1), var)

    def _internal_bind_out_params(self, child_ec: ExecutionContext) -> None:
        for i, var in enumerate(child_ec.instance._internal_get_out_params()):
            var = var.replace('?', '_', 1)
            if(len(child_ec.call_out_params) > i):
                if(getattr(child_ec.instance, var) is None):
                    if(getattr(self,
                               child_ec.call_out_params[i].replace('?', '_', 1), None) is None):
                        setattr(self, child_ec.call_out_params[i].replace('?', '_', 1), None)
                else:
                    setattr(self, child_ec.call_out_params[i].replace('?', '_', 1),
                            getattr(child_ec.instance, var))

    @final
    def _internal_tick_child(self, child_ec: ExecutionContext):

        # if child status is IDLE or RUNNING -> tick it
        if(child_ec.instance.get_status() == NodeStatus.IDLE or
           child_ec.instance.get_status() == NodeStatus.RUNNING):
            # tick child
            child_ec.instance._internal_on_tick()

    @final
    def _internal_apply_contingencies(self, child_ec: ExecutionContext):
        self.get_logger().debug('searching contingency-handler for: '
                                + f'{child_ec.instance.__class__.__name__} - '
                                + f'{child_ec.instance.get_status()} - '
                                + f'{child_ec.instance.get_contingency_message()}')

        # iterate over contingency_handler_list
        for contingency_handler in self._contingency_handler_list:

            # handle regex
            if(isinstance(contingency_handler[0], str)):
                regexClassName = re.compile(contingency_handler[0])
            else:
                regexClassName = re.compile(contingency_handler[0].__name__)
            regexMessage = re.compile(contingency_handler[2])

            self.get_logger().debug(f'checking contingency_handler: {regexClassName.pattern} - '
                                    + f'{contingency_handler[1]} - {regexMessage.pattern}')

            # check if contingency-handler matches
            if(bool(re.match(regexClassName,
                             child_ec.instance.__class__.__name__))
                    and child_ec.instance.get_status() in contingency_handler[1]
                    and bool(re.match(regexMessage,
                                      child_ec.instance.get_contingency_message()))):
                self.get_logger().debug(f'{child_ec.instance.__class__.__name__} -> '
                                        + f'run contingency_handler {contingency_handler[3]}')
                # append ContingencyHistoryEntry to history
                self._internal_append_to_contingency_history(
                    ContingencyHistoryEntry(child_ec.instance.__class__.__name__,
                                            child_ec.instance.get_status(),
                                            child_ec.instance.get_contingency_message(),
                                            contingency_handler[3]))
                # execute function attached to the contingency-handler
                exec(f'self.{contingency_handler[3]}()')
                break

    # PUBLIC

    @final
    def register_contingency_handler(self,
                                     node,
                                     node_status_list: List[NodeStatus],
                                     contingency_message: str,
                                     contingency_function: Callable) -> None:
        """Register a contingency-handler.

        Registers a function which is called in case the provided contingency information
        are met. The registered contingency-handlers are tried to match to the current
        status and contingency message in the order they are registered.

        For the parameters `node` and `contingency_message` a regular expression (regex)
        can be used.

        Parameters
        ----------
        node: TreeNode, str
            The node the contingency-handler triggers on. In case of using regex
            the name has to be provided as string.
        node_status_list:  [NodeStatus]
            A list of NodeStatuses the contingency-handler triggers on.
        contingency_message: str
            A regex the contingency-message has to match.
        contingency_function: Callable
            The function which is called to handle the contingency.

        """
        # for the function only store the name, thus there is no 'bound method' to self
        # which increases the ref count and prevents the gc to delete the object
        self._contingency_handler_list.append((node,
                                               node_status_list,
                                               contingency_message,
                                               contingency_function.__name__))

    @final
    def fix_current_child(self) -> None:
        """Fix the current child.

        Mark the current child node as `FIXED`. This function should typiclly be
        called inside of a contingency-handler in case the handler fixes the situation
        and the control flow of the current `ControlNode` can be continued. `FIXED`
        is handled in the same way as `SUCCESS`, but provides the additional information
        that the node was 'fixed'.

        """
        self.get_logger().trace(f'{self.__class__.__name__} -> fix_current_child called')
        self.set_current_child_status(NodeStatus.FIXED)

    @final
    def abort_current_child(self) -> None:
        """Abort the currently executing child."""
        self.get_logger().trace(f'{self.__class__.__name__} -> abort_current_child called')
        if(self._child_ptr < len(self._child_ec_list)
           and self._child_ec_list[self._child_ptr].instance is not None):
            self._child_ec_list[self._child_ptr].instance.abort()

    @final
    def set_current_child_status(self, node_status: NodeStatus) -> None:
        """Set the status of the currently executing child node.

        Parameters
        ----------
        node_status: `NodeStatus`
            Status of the node

        """
        self.get_logger().trace(f'{self.__class__.__name__} -> set_current_child_status '
                                + f'to {node_status}')
        self._child_ec_list[self._child_ptr].instance.set_status(node_status)
