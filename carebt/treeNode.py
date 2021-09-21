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

from typing import Callable
from typing import final
from typing import TYPE_CHECKING

from carebt.nodeStatus import NodeStatus

if TYPE_CHECKING:
    from carebt.behaviorTree import BehaviorTree
    from carebt.behaviorTree import Logger


class TreeNode():  # abstract

    def __init__(self, bt: 'BehaviorTree', params: str = None):
        self.bt = bt
        self.set_status(NodeStatus.IDLE)
        self.__error_message = ''
        self.__params = params
        self.__in_params = []
        self.__out_params = []
        self._abort_handler = None

        # create local variables
        if(self.__params is not None):
            _params = self.__params.split('=>')
            if(len(_params[0]) > 0):
                self.__in_params = _params[0].strip().split(' ')
            if len(_params) == 2:
                self.__out_params = _params[1].strip().split(' ')

            self.get_logger().debug(2, '{} in_params:  {}'
                                    .format(self.__class__.__name__,
                                            self.__in_params))
            self.get_logger().debug(2, '{} out_params: {}'
                                    .format(self.__class__.__name__,
                                            self.__out_params))

            # create in params
            for p in filter(None, self.__in_params):
                p = p.replace('?', '_')
                self.get_logger().debug(2, 'in: {}'.format(p))
                exec('self.{} = None'.format(p))

            # create out params
            for p in filter(None, self.__out_params):
                p = p.replace('?', '_')
                self.get_logger().debug(2, 'out: {}'.format(p))
                exec('self.{} = None'.format(p))

    # PROTECTED

    # @abstractmethod
    def _on_tick(self) -> None:
        raise NotImplementedError

    # @abstractmethod
    def _on_abort(self) -> None:
        raise NotImplementedError

    # PUBLIC

    @final
    def abort(self) -> None:
        self._on_abort()

    @final
    def attach_abort_handler(self, function: Callable) -> None:
        self._abort_handler = function.__name__

    @final
    def get_bt(self) -> 'BehaviorTree':
        return self.bt

    @final
    def get_logger(self) -> 'Logger':
        return self.bt.get_logger()

    @final
    def get_status(self) -> NodeStatus:
        return self.__node_status

    @final
    def set_status(self, node_status: NodeStatus) -> None:
        self.__node_status = node_status

    @final
    def get_message(self) -> str:
        return self.__error_message

    @final
    def set_message(self, error_message: str) -> None:
        self.__error_message = error_message

    @final
    def get_in_params(self) -> list:
        return self.__in_params

    @final
    def get_out_params(self) -> list:
        return self.__out_params
