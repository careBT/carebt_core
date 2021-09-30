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

from time import sleep

from carebt.abstractLogger import AbstractLogger, LogLevel
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode
from carebt.simplePrintLogger import SimplePrintLogger
from carebt.treeNode import TreeNode


class RootNode(SequenceNode):

    def __init__(self, bt_runner: 'BehaviorTreeRunner'):
        super().__init__(bt_runner)


class BehaviorTreeRunner:
    """
    The `BehaviorTreeRunner` is the interface to the careBT execution engine.
    With the `run` method a careBT behavior tree, respectively each careBT
    node can be executed.

    """

    def __init__(self):
        self._tick_rate_ms = 50
        self._tick_count = 0
        self._logger = SimplePrintLogger()
        self.get_logger().set_log_level(LogLevel.WARN)

    # PUBLIC

    def set_tick_rate_ms(self, tick_rate_ms: int) -> None:
        """
        Sets the rate in milliseconds in which the careBT execution engine runs.
        It is the rate at which the nodes are ticked. Default is 50 ms.

        Parameters
        ----------
        tick_rate_ms: int
            The tick rate in milliseconds

        """

        self._tick_rate_ms = tick_rate_ms

    def get_tick_count(self) -> int:
        """
        Returns the current counter of the ticks the careBT execution engine
        has taken for the last execution of the `run` method.

        Returns
        -------
        int
            Ticks taken for the behavior tree execution

        """

        return self._tick_count

    def set_logger(self, logger: AbstractLogger):
        """
        Sets a custom logger which is then used by the careBT execution
        engine.

        Parameters
        ----------
        logger: AbstractLogger
            A logger implementation

        """

        self._logger = logger

    def get_logger(self) -> AbstractLogger:
        """
        Returns the current logger, which is an implementation of
        `AbstractLogger`.

        Returns
        -------
        `AbstractLogger`
            The current logger

        """

        return self._logger

    def run(self, node: TreeNode, params: str = None) -> None:
        """
        Executes the provided node, respectively the provided behavior tree.

        Parameters
        ----------
        node: TreeNode
            The node which should be executed

        params: str, optional
            The parameters for the node which should be executed

        """

        self._instance = RootNode(self)
        self._instance.set_status(NodeStatus.IDLE)
        self._instance.set_contingency_message('')
        self._instance.add_child(node, params)
        self._tick_count = 0

        # run tree
        while(self._instance.get_status() == NodeStatus.IDLE
                or self._instance.get_status() == NodeStatus.RUNNING):
            self._tick_count += 1
            self.get_logger().info('---------------------------------- tick-count: {}'
                                   .format(self._tick_count))
            self._instance._on_tick()
            sleep(self._tick_rate_ms / 1000)

        # after tree execution
        self.get_logger().info('---------------------------------------------------')
        self.get_logger().info('bt execution finished')
        self.get_logger().info('status:  {}'.format(self._instance.get_status()))
        self.get_logger().info('message: {}'.format(self._instance.get_contingency_message()))
        self.get_logger().info('---------------------------------------------------')