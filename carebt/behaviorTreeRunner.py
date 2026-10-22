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

import sched
from threading import get_ident
from time import monotonic
from time import sleep
from typing import Callable

from carebt.abstractLogger import AbstractLogger, LogLevel
from carebt.careBTTimer import CareBTTimer
from carebt.contingencyHistoryEntry import ContingencyHistoryEntry
from carebt.nodeStatus import NodeStatus
from carebt.rootNode import RootNode
from carebt.simplePrintLogger import SimplePrintLogger
from carebt.treeNode import TreeNode


class _RootNode(RootNode):

    def __init__(self, bt_runner: 'BehaviorTreeRunner'):
        super().__init__(bt_runner)


class BehaviorTreeRunner:
    """The careBT `BehaviorTreeRunner` class.

    The `BehaviorTreeRunner` is the interface to the careBT execution engine.
    With the `run` method a careBT behavior tree, respectively each careBT
    node can be executed. Alternatively, the behavior tree can be initialized
    with `initialize` and ticked externally with `tick`, e.g. to integrate
    careBT into another event loop like the one of ROS 2.

    The careBT execution engine is single-threaded. Nodes, timers and timeouts
    are always executed in the thread which ticks the behavior tree. Thus, the
    state of a node must never be changed from another thread.

    .. hint::

        A warning is logged in case `set_status` or `set_contingency_message`
        of a node is called from another thread than the one which ticks the
        behavior tree, or in case `tick` is called from different threads.
    """

    def __init__(self):
        """Init the `BehaviorTreeRunner`."""
        self._tick_rate_ms = 50
        self._tick_count = 0
        self._instance = None
        self._tick_thread_id = None
        self.__scheduler = sched.scheduler(monotonic, sleep)
        self._logger = SimplePrintLogger()
        self.get_logger().set_log_level(LogLevel.WARN)

    # PUBLIC

    def set_tick_rate_ms(self, tick_rate_ms: int) -> None:
        """Set the tick rate in milliseconds.

        Sets the rate in milliseconds in which the `run` method ticks the
        behavior tree. Default is 50 ms. In case the behavior tree is ticked
        externally with `tick`, the caller is responsible for the tick rate.

        Parameters
        ----------
        tick_rate_ms: int
            The tick rate in milliseconds

        """
        self._tick_rate_ms = tick_rate_ms

    def get_tick_count(self) -> int:
        """Return the current tick count.

        Returns the current counter of the ticks the careBT execution engine
        has taken since the last call of `initialize`, respectively `run`.

        Returns
        -------
        int
            Ticks taken for the behavior tree execution

        """
        return self._tick_count

    def set_logger(self, logger: AbstractLogger):
        """Set a custom logger.

        Sets a custom logger which is then used by the careBT execution
        engine.

        Parameters
        ----------
        logger: AbstractLogger
            A logger implementation

        """
        self._logger = logger

    def get_logger(self) -> AbstractLogger:
        """Return the current logger.

        Returns
        -------
        `AbstractLogger`
            The current logger

        """
        return self._logger

    def get_status(self) -> NodeStatus:
        """Return the status of the last execution.

        Returns
        -------
        `NodeStatus`
            Current status of the node

        """
        return self._instance.get_status()

    def get_contingency_message(self) -> str:
        """Return the contincency message of the last execution.

        Returns
        -------
        str
            The contingency message

        """
        return self._instance.get_contingency_message()

    def create_timer(self, delay_ms: int, callback: Callable) -> CareBTTimer:
        """Create a one-shot timer.

        The callback is executed in the thread which ticks the behavior tree,
        right before the next tick after the timer has expired. Thus, the
        callback can safely change the state of the nodes.

        Parameters
        ----------
        delay_ms: int
            The delay in milliseconds after which the callback is executed
        callback: Callable
            The function which is called when the timer expires

        Returns
        -------
        `CareBTTimer`
            The timer, which can be used to cancel it

        """
        return CareBTTimer(self.__scheduler, delay_ms, callback)

    def initialize(self, node: TreeNode, params: str = None) -> None:
        """Initialize the execution of the provided node, respectively behavior tree.

        After initialization the behavior tree is executed by calling `tick`
        repeatedly. Alternatively, use `run` which initializes and ticks the
        behavior tree until it has completed. Pending timers of a previous
        execution are canceled.

        Parameters
        ----------
        node: TreeNode
            The node which should be executed

        params: str, optional
            The parameters for the node which should be executed

        """
        # drop timers left over from a previous execution
        for event in self.__scheduler.queue:
            try:
                self.__scheduler.cancel(event)
            except ValueError:  # pragma: no cover
                pass
        self._tick_thread_id = None
        self._instance = _RootNode(self)
        self._instance.set_status(NodeStatus.IDLE)
        self._instance.set_contingency_message('')
        self._instance.set_child(node, params)
        self._tick_count = 0

    def tick(self) -> NodeStatus:
        """Execute one tick of the behavior tree.

        First, the callbacks of all expired timers are executed. Afterwards, the
        behavior tree is ticked once. If the behavior tree has already completed,
        calling `tick` has no effect.

        All nodes, timers and timeouts are executed in the thread which calls
        `tick`. Thus, `tick` must always be called from the same thread.

        Returns
        -------
        `NodeStatus`
            The status of the behavior tree after the tick

        """
        if(self._instance is None):
            raise RuntimeError('BehaviorTreeRunner.tick called before initialize')
        thread_id = get_ident()
        if(self._tick_thread_id is None):
            self._tick_thread_id = thread_id
        elif(self._tick_thread_id != thread_id):
            self.get_logger().warn('BehaviorTreeRunner.tick called from another thread '
                                   + 'than the previous ticks')
        if(self._instance.get_status() != NodeStatus.IDLE
                and self._instance.get_status() != NodeStatus.RUNNING):
            return self._instance.get_status()

        self.__scheduler.run(blocking=False)

        self._tick_count += 1
        self.get_logger().trace('---------------------------------- '
                                + f'tick-count: {self._tick_count}')
        self._instance._internal_on_tick()

        if(self._instance.get_status() != NodeStatus.IDLE
                and self._instance.get_status() != NodeStatus.RUNNING):
            self.__log_result()
        return self._instance.get_status()

    def run(self, node: TreeNode, params: str = None) -> None:
        """Execute the provided node, respectively the provided behavior tree.

        Initializes the behavior tree and ticks it with the configured tick rate
        until it has completed.

        Parameters
        ----------
        node: TreeNode
            The node which should be executed

        params: str, optional
            The parameters for the node which should be executed

        """
        self.initialize(node, params)
        while(True):
            status = self.tick()
            sleep(self._tick_rate_ms / 1000)
            if(status != NodeStatus.IDLE and status != NodeStatus.RUNNING):
                break

    # PRIVATE

    def __log_result(self) -> None:
        if(self._instance.get_status() == NodeStatus.SUCCESS):
            self.get_logger().info('---------------------------------------------------')
            self.get_logger().info('bt execution finished')
            self.get_logger().info(f'status:  {self._instance.get_status()}')
            self.get_logger().info('contingency-message: '
                                   + f'{self._instance.get_contingency_message()}')
            entry: ContingencyHistoryEntry
            for idx, entry in enumerate(self._instance.get_contingency_history()):
                if idx == 0:
                    self.get_logger().info(f'contingency-history: [{idx}] {entry.node_name}')
                    self.get_logger().info(f'                         {entry.status}')
                    self.get_logger().info(f'                         {entry.contingency_message}')
                    self.get_logger().info(f'                         {entry.function}')
                else:
                    self.get_logger().info(f'                     [{idx}] {entry.node_name}')
                    self.get_logger().info(f'                         {entry.status}')
                    self.get_logger().info(f'                         {entry.contingency_message}')
                    self.get_logger().info(f'                         {entry.function}')
            self.get_logger().info('---------------------------------------------------')
        else:
            self.get_logger().warn('---------------------------------------------------')
            self.get_logger().warn('bt execution finished')
            self.get_logger().warn(f'status:  {self._instance.get_status()}')
            self.get_logger().warn('contingency-message: '
                                   + f'{self._instance.get_contingency_message()}')
            entry: ContingencyHistoryEntry
            for idx, entry in enumerate(self._instance.get_contingency_history()):
                if idx == 0:
                    self.get_logger().warn(f'contingency-history: [{idx}] {entry.node_name}')
                    self.get_logger().warn(f'                         {entry.status}')
                    self.get_logger().warn(f'                         {entry.contingency_message}')
                    self.get_logger().warn(f'                         {entry.function}')
                else:
                    self.get_logger().warn(f'                     [{idx}] {entry.node_name}')
                    self.get_logger().warn(f'                         {entry.status}')
                    self.get_logger().warn(f'                         {entry.contingency_message}')
                    self.get_logger().warn(f'                         {entry.function}')
            self.get_logger().warn('---------------------------------------------------')
