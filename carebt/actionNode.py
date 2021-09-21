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

from datetime import datetime

from typing import TYPE_CHECKING

from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode

if TYPE_CHECKING:
    from carebt.behaviorTree import BehaviorTree


class ActionNode(TreeNode):  # abstract

    def __init__(self, bt: 'BehaviorTree', params: str = None):
        super().__init__(bt, params)
        self.get_logger().info(1, 'creating {}'.format(self.__class__.__name__))
        self.__throttle_ms = None
        self.__last_ts = datetime.min
        self.set_status(NodeStatus.IDLE)

    def set_throttle_ms(self, throttle_ms: int) -> None:
        self.__throttle_ms = throttle_ms

    # PROTECTED

    def _on_tick(self) -> None:
        current_ts = datetime.now()
        if(self.__throttle_ms is None or
                int((current_ts - self.__last_ts).total_seconds() * 1000) >= self.__throttle_ms):
            if(self.get_status() == NodeStatus.IDLE or
                    self.get_status() == NodeStatus.RUNNING):
                self.bt.get_logger().info(1, 'ticking {} - {}'
                                          .format(self.__class__.__name__,
                                                  self.get_status()))
                self.on_tick()
                self.__last_ts = current_ts

    def _on_abort(self) -> None:
        self.bt.get_logger().info(1, 'aborting {}'.format(self.__class__.__name__))
        self.on_abort()
        self.set_status(NodeStatus.ABORTED)

    # PUBLIC

    # @abstractmethod
    def on_tick(self) -> None:
        raise NotImplementedError

    def on_abort(self) -> None:
        pass
