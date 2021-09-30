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

from tests.global_mock import mock

from carebt.actionNode import ActionNode
from carebt.nodeStatus import NodeStatus

########################################################################


class AddTwoNumbersAction(ActionNode):

    def __init__(self, bt):
        super().__init__(bt, '?x ?y => ?z')
        self._x = 999
        self._y = 999
        mock('__init__ {}'.format(self.__class__.__name__))

    def _on_tick(self) -> None:
        mock('_on_tick - {} + {}'.format(self._x, self._y))
        if(self._x != 123 and self._y != 123):
            self._z = self._x + self._y
        self.set_status(NodeStatus.SUCCESS)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))
