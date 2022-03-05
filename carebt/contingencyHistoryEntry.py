# Copyright 2022 Andreas Steck (steck.andi@gmail.com)
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

from carebt.nodeStatus import NodeStatus


class ContingencyHistoryEntry():
    """The careBT `ContingencyHistoryEntry` class.

    `ContingencyHistoryEntry` represents a contingency history entry of the contingency
    history list.

    Parameters
    ----------
    node_name: str
        The name of the node which raised the contingency.
    status: NodeStatus
        The NodeStatus which lead to the contingency.
    contingency_message: str
        The contingency-message which lead to the contingency.
    function: str
        The contingency handler function which was called.

    """

    def __init__(self, node_name: str, status: NodeStatus,
                 contingency_message: str, function: str):
        self.node_name = node_name
        self.status = status
        self.contingency_message = contingency_message
        self.function = function
