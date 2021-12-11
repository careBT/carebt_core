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
    """An Enum representing the status of a careBT node."""

    IDLE = 0
    """Node is waiting for first execution"""

    RUNNING = 1
    """Node is currently executing"""

    SUSPENDED = 2
    """Node is currently executing, but on_tick() is not called"""

    SUCCESS = 3
    """Node has completed with SUCCESS"""

    FAILURE = 4
    """Node has completed with FAILURE"""

    ABORTED = 5
    """Node has completed with ABORTED"""

    FIXED = 6
    """Node has completed with FIXED (by contingency-handler)"""
