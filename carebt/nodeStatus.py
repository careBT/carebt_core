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

from enum import Enum


class NodeStatus(Enum):
    """
    An Enum representing the status of a careBT node

    `IDLE`:      Waiting for first execution
    `RUNNING`:   Currently executing
    `SUSPENDED`: Currently executing, but on_tick() is not called
    `SUCCESS`:   Completed with SUCCESS
    `FAILURE`:   Completed with FAILURE
    `ABORTED`:   Completed with ABORTED
    `FIXED`:     Completed with FIXED (by contingency-handler)

    """

    IDLE = 0
    RUNNING = 1
    SUSPENDED = 2
    SUCCESS = 3
    FAILURE = 4
    ABORTED = 5
    FIXED = 6
