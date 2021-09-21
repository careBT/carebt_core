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

import re

from typing import Callable
from typing import final
from typing import TYPE_CHECKING

from carebt.executionContext import ExecutionContext
from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode

if TYPE_CHECKING:
    from carebt.behaviorTree import BehaviorTree  # pragma: no cover


class ControlNode(TreeNode):  # abstract

    def __init__(self, bt: 'BehaviorTree', params: str = None):
        super().__init__(bt, params)

        # list for the child nodes
        self._child_ec_list = []

        # the current child pointer
        self._child_ptr = 0

        self._rule_handler_list = []

        self.set_status(NodeStatus.IDLE)

    # PRIVATE

    """ allowed wildcards:
        ? one character
        * one or many charactres"""
    def __wildcard_to_regex(self, wildcard: str) -> re:
        # replace wildcards
        wildcard = wildcard.replace('?', '.')
        wildcard = wildcard.replace('*', '.*')

        return re.compile(wildcard)

    def _bind_in_params(self, child_ec: ExecutionContext) -> None:
        if(len(child_ec.call_in_params) != len(child_ec.instance.get_in_params())):
            self.get_logger().warn(1, '{} takes {} argument(s), but {} was/were provided'
                                   .format(child_ec.node_as_class.__name__,
                                           len(child_ec.instance.get_in_params()),
                                           len(child_ec.call_in_params)))
        for i, var in enumerate(child_ec.call_in_params):
            if(isinstance(var, str) and var[0] == '?'):
                var = var.replace('?', '_')
                var = getattr(self, var)
            setattr(child_ec.instance,
                    child_ec.instance.get_in_params()[i].replace('?', '_'), var)

    def _bind_out_params(self, child_ec: ExecutionContext) -> None:
        for i, var in enumerate(child_ec.instance.get_out_params()):
            var = var.replace('?', '_')
            if(getattr(child_ec.instance, var) is None):
                self.get_logger().warn(1, '{} output {} is not set'
                                       .format(child_ec.node_as_class.__name__,
                                               var.replace('_', '?')))
            setattr(self, child_ec.call_out_params[i].replace('?', '_'),
                    getattr(child_ec.instance, var))

    # PROTECTED

    @final
    def _tick_child(self, child_ec: ExecutionContext):

        # if child status is IDLE or RUNNING -> tick it
        if(child_ec.instance.get_status() == NodeStatus.IDLE or
           child_ec.instance.get_status() == NodeStatus.RUNNING):
            # bind in params
            self._bind_in_params(child_ec)

            # tick child
            child_ec.instance._on_tick()

        # bind out params
        self._bind_out_params(child_ec)

    @final
    def _apply_rules(self, child_ec: ExecutionContext):
        self.get_logger().debug(1, 'searching rule-handler for: {} - {} - {}'
                                .format(child_ec.instance.__class__.__name__,
                                        child_ec.instance.get_status(),
                                        child_ec.instance.get_message()))

        # iterate over rule_handler_list
        for rule_handler in self._rule_handler_list:

            # handle wildcards
            if(isinstance(rule_handler[0], str)):
                regexClassName = self.__wildcard_to_regex(
                    rule_handler[0])
            else:
                regexClassName = self.__wildcard_to_regex(
                    rule_handler[0].__name__)
            regexMessage = self.__wildcard_to_regex(rule_handler[2])

            self.get_logger().debug(2, 'rule_handler: {} -{} - {}'
                                    .format(regexClassName.pattern,
                                            rule_handler[1],
                                            regexMessage.pattern))
            # check if rule-handler matches
            if(bool(re.match(regexClassName,
                             child_ec.instance.__class__.__name__))
                    and child_ec.instance.get_status() in rule_handler[1]
                    and bool(re.match(regexMessage,
                                      child_ec.instance.get_message()))):
                self.get_logger().debug(1, '{} -> run rule_handler {}'
                                        .format(child_ec.instance.__class__.__name__,
                                                rule_handler[3]))
                # execute function attached to the rule-handler
                exec('self.{}()'.format(rule_handler[3]))
                self.get_logger().info(1, 'after rule_handler {} - {} - {}'
                                       .format(child_ec.instance.__class__.__name__,
                                               child_ec.instance.get_status(),
                                               child_ec.instance.get_message()))
                break

        # if child status is SUCCESS
        if(child_ec.instance.get_status() == NodeStatus.SUCCESS):
            # bind out params
            self._bind_out_params(child_ec)

    # PUBLIC

    @final
    def attach_rule_handler(self, node_as_class: TreeNode, node_status_list: NodeStatus,
                            message: str, function: Callable) -> None:
        # for the function only store the name, thus there is no 'bound method' to self
        # which increases the ref count and prevents the gc to delete the object
        self._rule_handler_list.append((node_as_class,
                                        node_status_list,
                                        message,
                                        function.__name__))

    def set_child_status(self, status: NodeStatus) -> None:
        self._child_ec_list[self._child_ptr].instance.set_status(status)

    def set_child_message(self, msg: str) -> None:
        self._child_ec_list[self._child_ptr].instance.set_message(msg)

    def clear_child_message(self) -> None:
        self._child_ec_list[self._child_ptr].instance.set_message('')
