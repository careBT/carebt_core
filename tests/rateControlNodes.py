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
from tests.actionNodes import AddTwoNumbersMultiTickAction
from tests.actionNodes import AddTwoNumbersMultiTickActionWithTimeout

from carebt.rateControlNode import RateControlNode

########################################################################


class RateControlledAddTwoNumbersMultiTickAction(RateControlNode):

    def __init__(self, bt):
        super().__init__(bt, 250)
        mock('__init__ RateControlledAddTwoNumbersMultiTickAction')

    def on_init(self) -> None:
        mock('__init__ RateControlledAddTwoNumbersMultiTickAction')
        self.set_child(AddTwoNumbersMultiTickAction, '5 1 2 => ?result')

    def on_delete(self) -> None:
        mock('on_delete RateControlledAddTwoNumbersMultiTickAction')

    def __del__(self):
        mock('__del__ RateControlledAddTwoNumbersMultiTickAction')

########################################################################


class RateControlledAddTwoNumbersMultiTickActionWithTimeout(RateControlNode):

    def __init__(self, bt):
        super().__init__(bt, 400)
        mock('__init__ RateControlledAddTwoNumbersMultiTickActionWithTimeout')

    def on_init(self) -> None:
        mock('__init__ RateControlledAddTwoNumbersMultiTickActionWithTimeout')
        self.set_child(AddTwoNumbersMultiTickActionWithTimeout, '5 1 2 => ?result')

    def on_delete(self) -> None:
        mock('on_delete RateControlledAddTwoNumbersMultiTickActionWithTimeout')

    def __del__(self):
        mock('__del__ RateControlledAddTwoNumbersMultiTickActionWithTimeout')

########################################################################


class RateControlledAddTwoNumbersMultiTickActionOwnTimeout(RateControlNode):

    def __init__(self, bt):
        super().__init__(bt, 250)
        mock('__init__ RateControlledAddTwoNumbersMultiTickActionOwnTimeout')

    def on_init(self) -> None:
        mock('__init__ RateControlledAddTwoNumbersMultiTickActionOwnTimeout')
        self.set_child(AddTwoNumbersMultiTickAction, '5 1 2 => ?result')
        self.set_timeout(1000)

    def on_delete(self) -> None:
        mock('on_delete RateControlledAddTwoNumbersMultiTickActionOwnTimeout')

    def on_timeout(self) -> None:
        mock('on_timeout RateControlledAddTwoNumbersMultiTickActionOwnTimeout')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def __del__(self):
        mock('__del__ RateControlledAddTwoNumbersMultiTickActionOwnTimeout')
