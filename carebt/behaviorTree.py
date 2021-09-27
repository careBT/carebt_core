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

from carebt.logger import AbstractLogger, Logger
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode
from carebt.treeNode import TreeNode


class RootSequence(SequenceNode):

    def __init__(self, bt: 'BehaviorTree'):
        super().__init__(bt)


class BehaviorTree:

    def __init__(self):
        self._instance = RootSequence(self)
        self._tick_rate_ms = 50
        self._tick_count = 0
        self._logger = Logger()

    def set_tick_rate_ms(self, tick_rate_ms: int) -> None:
        self._tick_rate_ms = tick_rate_ms

    def get_tick_count(self) -> int:
        return self._tick_count

    def set_logger(self, logger: AbstractLogger):
        self._logger = logger

    def get_logger(self) -> Logger:
        return self._logger

    def run(self, root_node: TreeNode, params: str = None) -> None:
        self._instance.add_child(root_node, params)
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
        self.get_logger().info('message: {}'.format(self._instance.get_message()))
        self.get_logger().info('---------------------------------------------------')
