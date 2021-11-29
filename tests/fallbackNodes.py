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

from tests.actionNodes import AddTwoNumbersAction
from tests.actionNodes import AddTwoNumbersActionWithFailure
from tests.global_mock import mock

from carebt.fallbackNode import FallbackNode

########################################################################


class AddTwoNumbersFallback1(FallbackNode):
    """
    The `AddTwoNumbersFallback1` has two child nodes which both complete with
    `SUCCESS`. The second one should not be executed as the first one already
    succeeds.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback1')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback1')
        self.append_child(AddTwoNumbersAction, '2 4 => ?result')
        self.append_child(AddTwoNumbersAction, '3 6 => ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback1')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback1')

########################################################################


class AddTwoNumbersFallback2(FallbackNode):
    """
    The `AddTwoNumbersFallback2` has two child nodes. The first one fails,
    the second one succeeds. Thus, both should be executed.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback2')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback2')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersAction, '3 6 => ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback2')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback2')

########################################################################


class AddTwoNumbersFallback3(FallbackNode):
    """
    The `AddTwoNumbersFallback3` has four child nodes. The first two fail and the
    following two succeed. Thus, the first three should be executed.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback3')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback3')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '=> ?result')
        self.append_child(AddTwoNumbersAction, '2 4 => ?result')
        self.append_child(AddTwoNumbersAction, '3 6 => ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback3')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback3')

########################################################################


class AddTwoNumbersFallback4(FallbackNode):
    """
    The `AddTwoNumbersFallback4` has two child nodes which both fail. In
    this case the `FallbackSequence` should also fail.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ AddTwoNumbersFallback4')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersFallback4')
        self.append_child(AddTwoNumbersActionWithFailure, '3 => ?result')
        self.append_child(AddTwoNumbersActionWithFailure, '=> ?result')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersFallback4')

    def __del__(self):
        mock('__del__ AddTwoNumbersFallback4')
