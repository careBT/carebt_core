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
from typing import TYPE_CHECKING

from carebt.nodeStatus import NodeStatus
from carebt.treeNode import TreeNode

if TYPE_CHECKING:
    from carebt.behaviorTreeRunner import BehaviorTreeRunner  # pragma: no cover


class ActionNode(TreeNode, ABC):
    """The careBT `ActionNode` class.

    `ActionNodes` are the leafs in a careBT behavior tree. They execute
    the actions in the 'world' the behavior tree is running in. This includes
    manipulating the environment or actively perceiving it.

    Parameters
    ----------
    bt_runner: 'BehaviorTreeRunner'
        The behavior tree runner which started the tree.
    params: str
        The input/Output parameters of the node
        e.g. '?x ?y => ?z'

    """

    def __init__(self, bt_runner: 'BehaviorTreeRunner', params: str = None):
        """Init the `ActionNode` with bt_runner and params."""
        super().__init__(bt_runner, params)
        self.get_logger().info(f'creating {self.__class__.__name__}')

    # PROTECTED

    def _internal_on_tick(self) -> None:
        current_ts = datetime.now()
        if(self._throttle_ms is None or
                int((current_ts - self._last_ts).total_seconds() * 1000) >= self._throttle_ms):
            if(self.get_status() == NodeStatus.IDLE or
                    self.get_status() == NodeStatus.RUNNING):
                self.bt_runner.get_logger().trace(f'ticking {self.__class__.__name__} - '
                                                  + f'{self.get_status()}')
                self.on_tick()
                self._last_ts = current_ts

    def _internal_on_abort(self) -> None:
        super()._internal_on_abort()
        self.bt_runner.get_logger().info(f'aborting {self.__class__.__name__}')
        self.on_abort()
        self.set_status(NodeStatus.ABORTED)
