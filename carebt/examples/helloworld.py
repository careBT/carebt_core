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

from carebt import ActionNode
from carebt import NodeStatus


class HelloWorldAction(ActionNode):
    """The `HelloWorldAction` example node.

    The `HelloWorldAction` provides a classical Hello World example.
    It demonstrates a simple implementation of a careBT `ActionNode`.

    When running the `HelloWorldAction`,
    'HelloWorldAction: Hello World !!!' is printed on standard output.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_tick(self) -> None:
        print('HelloWorldAction: Hello World !!!')
        self.set_status(NodeStatus.SUCCESS)
