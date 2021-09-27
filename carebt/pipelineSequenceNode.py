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
from carebt.sequenceNode import SequenceNode

if TYPE_CHECKING:
    from carebt.behaviorTreeRunner import BehaviorTreeRunner  # pragma: no cover


class PipelineSequenceNode(SequenceNode):  # abstract

    def __init__(self, bt_runner: 'BehaviorTreeRunner', params: str = None):
        super().__init__(bt_runner, params)
        self.__period_ms = None
        self.__current_cycle = 1
        self.__max_cycles = None
        self.__last_ts = datetime.min

    def set_period_ms(self, period_ms: int) -> None:
        self.__period_ms = period_ms

    def set_max_cycles(self, max_cycles: int) -> None:
        self.__max_cycles = max_cycles

    def _on_tick(self) -> None:
        self.get_logger().info('ticking PipelineSequenceNode {}'
                               .format(self.__class__.__name__))
        self.set_status(NodeStatus.RUNNING)

        current_ts = datetime.now()
        if(self.__period_ms is None or
           int((current_ts - self.__last_ts).total_seconds() * 1000) >= self.__period_ms):

            ################################################
            # If there is no current child to be ticked, create one

            if(self._child_ec_list[self._child_ptr].instance is None):
                # create node instance
                self._child_ec_list[self._child_ptr].instance = \
                    self._child_ec_list[self._child_ptr].node_as_class(self.get_bt_runner())

            # tick child
            self._tick_child(self._child_ec_list[self._child_ptr])
            self._apply_rules(self._child_ec_list[self._child_ptr])

            ################################################
            # finally, check how to proceed

            # if the status of the pipeline sequence is IDLE or RUNNING
            if(self.get_status() == NodeStatus.IDLE or
               self.get_status() == NodeStatus.RUNNING):
                self.__last_ts = datetime.min
                cur_child_state = self._child_ec_list[self._child_ptr].instance.get_status()

                # if the current child tick returned with ABORTED
                if(cur_child_state == NodeStatus.ABORTED):
                    # the whole pipeline sequence gets state ABORTED
                    self.set_status(NodeStatus.ABORTED)

                # if the current child tick returned with SUCCESS
                elif(cur_child_state == NodeStatus.SUCCESS):
                    # check if there is at least one more node to run
                    if(self._child_ptr + 1 < len(self._child_ec_list)):
                        self._child_ptr += 1
                    else:
                        # no more nodes to run -> pipeline sequence = SUCCESS
                        self.set_status(NodeStatus.SUCCESS)

                # if the current child tick returned with FAILURE
                elif(cur_child_state == NodeStatus.FAILURE):
                    self.__last_ts = current_ts

                    if(self.__current_cycle < self.__max_cycles):
                        self.__current_cycle += 1
                        self.set_status(NodeStatus.RUNNING)
                        self._child_ptr = 0
                        for child_ec in self._child_ec_list:
                            if(child_ec.instance is not None):
                                child_ec.instance.set_status(NodeStatus.IDLE)
                                child_ec.instance.set_message('')

                    else:
                        self.set_status(NodeStatus.FAILURE)
                        self.set_message(self._child_ec_list[self._child_ptr]
                                         .instance.get_message())

            if(self.get_status() == NodeStatus.SUCCESS or
               self.get_status() == NodeStatus.FAILURE or
               self.get_status() == NodeStatus.ABORTED):
                self.get_logger().info('finished {}'.format(self.__class__.__name__))
                for child_ec in self._child_ec_list:
                    child_ec.instance = None
