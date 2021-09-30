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
from abc import abstractmethod

from typing import Callable
from typing import final
from typing import TYPE_CHECKING

from carebt.nodeStatus import NodeStatus

if TYPE_CHECKING:
    from carebt.behaviorTreeRunner import BehaviorTreeRunner  # pragma: no cover
    from carebt.logger import AbstractLogger  # pragma: no cover


class TreeNode(ABC):
    """
    `TreeNode` is the basic class which provides the common implementation
    for all nodes of careBT.

    """

    def __init__(self, bt_runner: 'BehaviorTreeRunner', params: str = None):
        self.bt_runner = bt_runner
        self.set_status(NodeStatus.IDLE)
        self.__contingency_message = ''
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

            self.get_logger().trace('{} in_params:  {}'
                                    .format(self.__class__.__name__,
                                            self.__in_params))
            self.get_logger().trace('{} out_params: {}'
                                    .format(self.__class__.__name__,
                                            self.__out_params))

            # create in params
            for p in filter(None, self.__in_params):
                p = p.replace('?', '_', 1)
                self.get_logger().trace('in: {}'.format(p))
                exec('self.{} = None'.format(p))

            # create out params
            for p in filter(None, self.__out_params):
                p = p.replace('?', '_', 1)
                self.get_logger().trace('out: {}'.format(p))
                exec('self.{} = None'.format(p))

    # PROTECTED

    @abstractmethod
    def _on_tick(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _on_abort(self) -> None:
        raise NotImplementedError

    @final
    def _get_bt_runner(self) -> 'BehaviorTreeRunner':
        return self.bt_runner

    @final
    def _get_in_params(self) -> list:
        return self.__in_params

    @final
    def _get_out_params(self) -> list:
        return self.__out_params

    # PUBLIC

    @final
    def get_logger(self) -> 'AbstractLogger':
        """
        Returns the current logger, which is an implementation of
        `AbstractLogger`.

        Returns
        -------
        `AbstractLogger`
            The current logger

        """

        return self.bt_runner.get_logger()

    @final
    def get_status(self) -> NodeStatus:
        """
        Returns the current status of the node.

        Returns
        -------
        `NodeStatus`
            Current status of the node

        """

        return self.__node_status

    @final
    def set_status(self, node_status: NodeStatus) -> None:
        """
        Sets the current status of the node.

        Parameters
        ----------
        node_status: `NodeStatus`
            Current status of the node

        """

        self.__node_status = node_status

    @final
    def get_contingency_message(self) -> str:
        """
        Returns the contincency message of the node. Typically this
        message is set in case the node completes with `FAILURE` to
        provide more details what went wrong.

        Returns
        -------
        str
            The contingency message

        """

        return self.__contingency_message

    @final
    def set_contingency_message(self, contingency_message: str) -> None:
        """
        Sets the contincency message of the node. Typically this
        message is set in case the node completes with `FAILURE` to
        provide more details what went wrong.

        Parameters
        ----------
        contingency_message: str
            The contingency message

        """

        self.__contingency_message = contingency_message

    @final
    def attach_abort_handler(self, abort_function: Callable) -> None:
        """
        Sets a function which is called in case the node is aborted. The
        `abort_function` is the place to implement cleanup stuff for the node.

        Parameters
        ----------
        abort_function: Callable
            The abort function

        """

        self._abort_handler = abort_function.__name__

    @final
    def abort(self) -> None:
        """
        Abort the current node execution.

        """

        self._on_abort()
