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

from threading import Timer

from tests.global_mock import mock

from carebt.actionNode import ActionNode
from carebt.nodeStatus import NodeStatus

########################################################################


class HelloWorldAction(ActionNode):
    """
    The `HelloWorldAction` provides a classical Hello World example.
    It demonstrates a simple implementation of a careBT `ActionNode`.

    When running the `HelloWorldAction`, 'Hello World !!!' is printed on
    standard output.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ HelloWorldAction')

    def on_init(self):
        mock('on_init HelloWorldAction')

    def on_tick(self) -> None:
        mock('HelloWorldAction: Hello World !!!')
        print('HelloWorldAction: Hello World !!!')
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete HelloWorldAction')

    def __del__(self):
        mock('__del__ HelloWorldAction')

########################################################################


class AddTwoNumbersAction(ActionNode):
    """
    The `AddTwoNumbersAction` demonstrates a careBT `ActionNode` with two
    input parameters and one output parameter. It takes the two inputs,
    adds them and returns the result.

    Parameters
    ----------
    ?x : int, default = 0
        The first value
    ?y : int, default = 0
        The second value

    Returns
    -------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?x ?y => ?z')
        mock('__init__ AddTwoNumbersAction')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersAction')
        if(self._x is None):
            self._x = 1234
        if(self._y is None):
            self._y = 5678

    def on_tick(self) -> None:
        self._z = self._x + self._y
        mock('AddTwoNumbersAction: calculating: {} + {} = {}'
             .format(self._x, self._y, self._z))
        print('AddTwoNumbersAction: calculating: {} + {} = {}'
              .format(self._x, self._y, self._z))
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersAction')

########################################################################


class AddTwoNumbersActionWithFailure(ActionNode):
    """
    The `AddTwoNumbersActionWithFailure` is an extension of the
    `AddTwoNumbersAction`. It does not have default values for the two input
    parameters `?x` and `?y`. But in case that at least one of the two input
    parameters is missing the `AddTwoNumbersActionWithFailure` Node switches
    to state `FAILURE` with the message `NOT_TWO_NUMBERS_PROVIDED`.

    Parameters
    ----------
    ?x : int
        The first value
    ?y : int
        The second value

    Returns
    -------
    ?z : int
        The sum of ?x and ?y

    Contingencies:
    --------------
    FAILURE:
        NOT_TWO_NUMBERS_PROVIDED
            At least one of the two input parameters is missing.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?x ?y => ?z')
        mock('__init__ AddTwoNumbersActionWithFailure')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersActionWithFailure')

    def on_tick(self) -> None:
        if(self._x is None or self._y is None):
            mock('AddTwoNumbersActionWithFailure: You did not provide two numbers!')
            print('AddTwoNumbersActionWithFailure: You did not provide two numbers!')
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('NOT_TWO_NUMBERS_PROVIDED')
        else:
            self._z = self._x + self._y
            mock('AddTwoNumbersActionWithFailure: calculating: {} + {} = {}'
                 .format(self._x, self._y, self._z))
            print('AddTwoNumbersActionWithFailure: calculating: {} + {} = {}'
                  .format(self._x, self._y, self._z))
            self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersActionWithFailure')

    def __del__(self):
        mock('__del__ AddTwoNumbersActionWithFailure')

########################################################################


class AddTwoNumbersMultiTickAction(ActionNode):
    """
    The `AddTwoNumbersMultiTickAction` is a variation of the
    `AddTwoNumbersAction` which demonstrates how it looks like when a
    `ActionNode` requires more ticks to complete. To make things simple
    the amount of ticks required to complete the action is provided as
    input parameter.

    Parameters
    ----------
    ?ticks : int
        Number of ticks requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Returns
    -------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?ticks ?x ?y => ?z')
        mock('__init__ AddTwoNumbersMultiTickAction')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersMultiTickAction')
        self.tick_count = 1

    def on_tick(self) -> None:
        if(self.tick_count <= self._ticks):
            mock('AddTwoNumbersMultiTickAction: (tick_count = {}/{})'
                 .format(self.tick_count, self._ticks))
            print('AddTwoNumbersMultiTickAction: (tick_count = {}/{})'
                  .format(self.tick_count, self._ticks))
            self.tick_count += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            self._z = self._x + self._y
            mock('AddTwoNumbersMultiTickAction: DONE {} + {} = {}'
                 .format(self._x, self._y, self._z))
            print('AddTwoNumbersMultiTickAction: DONE {} + {} = {}'
                  .format(self._x, self._y, self._z))
            self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersMultiTickAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersMultiTickAction')

########################################################################


class AddTwoNumbersThrottledMultiTickAction(ActionNode):
    """
    The `AddTwoNumbersThrottledMultiTickAction` is a variation of the
    `AddTwoNumbersMultiTickAction` which demonstrates how ticking an
    `ActionNode` can be throttled to provided value. In this example
    this value is set to 500ms.

    Parameters
    ----------
    ?ticks : int
        Number of ticks requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Returns
    -------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?ticks ?x ?y => ?z')
        mock('__init__ AddTwoNumbersThrottledMultiTickAction')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersThrottledMultiTickAction')
        self.set_throttle_ms(500)
        self.tick_count = 1

    def on_tick(self) -> None:
        if(self.tick_count <= self._ticks):
            mock('AddTwoNumbersThrottledMultiTickAction: (tick_count = {}/{})'
                 .format(self.tick_count, self._ticks))
            print('AddTwoNumbersThrottledMultiTickAction: (tick_count = {}/{})'
                  .format(self.tick_count, self._ticks))
            self.tick_count += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            self._z = self._x + self._y
            mock('AddTwoNumbersThrottledMultiTickAction: DONE {} + {} = {}'
                 .format(self._x, self._y, self._z))
            print('AddTwoNumbersThrottledMultiTickAction: DONE {} + {} = {}'
                  .format(self._x, self._y, self._z))
            self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersThrottledMultiTickAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersThrottledMultiTickAction')

########################################################################


class AddTwoNumbersLongRunnungAction(ActionNode):
    """
    The `AddTwoNumbersLongRunnungAction` is a variation of the
    `AddTwoNumbersAction` which demonstrates how it looks like when a
    `ActionNode` executes an asynchronous function. To make things simple the
    asynchronous function is implemented with a simple Python timer and
    the amount of milliseconds the asynchronous function requires to complete
    is provided as input parameter.

    Parameters
    ----------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Returns
    -------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?x ?y => ?z')
        mock('__init__ AddTwoNumbersLongRunnungAction')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersLongRunnungAction')
        self.tick_count = 0

    def on_tick(self) -> None:
        mock('AddTwoNumbersLongRunnungAction: calculating {} ms ...'
             .format(self._calctime))
        print('AddTwoNumbersLongRunnungAction: calculating {} ms ...'
              .format(self._calctime))
        self.set_status(NodeStatus.SUSPENDED)
        Timer(self._calctime / 1000, self.done_callback).start()

    def done_callback(self) -> None:
        self._z = self._x + self._y
        mock('AddTwoNumbersLongRunnungAction: done: {} + {} = {}'
             .format(self._x, self._y, self._z))
        print('AddTwoNumbersLongRunnungAction: done: {} + {} = {}'
              .format(self._x, self._y, self._z))
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersLongRunnungAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersLongRunnungAction')

########################################################################


class AddTwoNumbersLongRunnungActionWithAbort(ActionNode):
    """
    The `AddTwoNumbersLongRunnungActionWithAbort` is a variation of the
    `AddTwoNumbersLongRunnungAction`. It uses the timeout callback to abort
    the `ActionNode` in case that the execution (asynchronous function) takes
    to long.

    Parameters
    ----------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Returns
    -------
    ?z : int
        The sum of ?x and ?y

    Contingencies:
    --------------
    FAILURE:
        NOT_TWO_NUMBERS_PROVIDED
            At least one of the two input parameters is missing.
    ABORT:
        TIMEOUT
            The execution time exceeded the timeout

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?x ?y => ?z')
        mock('__init__ AddTwoNumbersLongRunnungActionWithAbort')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersLongRunnungActionWithAbort')
        self.__TIMEOUT: int = 1000
        self.tick_count = 0
        self.set_timeout(self.__TIMEOUT)

    def on_tick(self) -> None:
        if(self._x is None or self._y is None):
            mock('AddTwoNumbersLongRunnungActionWithAbort: '
                 'You did not provide two numbers!')
            print('AddTwoNumbersLongRunnungActionWithAbort: '
                  'You did not provide two numbers!')
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('NOT_TWO_NUMBERS_PROVIDED')
        else:
            mock('AddTwoNumbersLongRunnungActionWithAbort: calculating {} ms ... '
                 '(timeout = {} ms)'
                 .format(self._calctime, self.__TIMEOUT))
            print('AddTwoNumbersLongRunnungActionWithAbort: calculating {} ms ... '
                  '(timeout = {} ms)'
                  .format(self._calctime, self.__TIMEOUT))
            self.set_status(NodeStatus.SUSPENDED)
            self.__done_timer = Timer(self._calctime / 1000, self.done_callback)
            self.__done_timer.start()

    def done_callback(self) -> None:
        # make sure that the node is still suspended, this is especially
        # important if also a timeout is used. If both occure in the same
        # careBT tick
        if(self.get_status() == NodeStatus.SUSPENDED):
            self._z = self._x + self._y
            mock('AddTwoNumbersLongRunnungActionWithAbort: done_callback: {} + {} = {}'
                 .format(self._x, self._y, self._z))
            print('AddTwoNumbersLongRunnungActionWithAbort: done_callback: {} + {} = {}'
                  .format(self._x, self._y, self._z))
            self.set_status(NodeStatus.SUCCESS)
            self.__done_timer.cancel()
            self.__done_timer = None

    def on_timeout(self) -> None:
        mock('on_timeout AddTwoNumbersLongRunnungActionWithAbort')
        print('on_timeout AddTwoNumbersLongRunnungActionWithAbort')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def on_abort(self) -> None:
        mock('on_abort AddTwoNumbersLongRunnungActionWithAbort')
        print('on_abort AddTwoNumbersLongRunnungActionWithAbort')
        self.__done_timer.cancel()
        # set the timer to None to make sure that all references (bound method)
        # are released and the object gets destroyed by gc
        self.__done_timer = None

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersLongRunnungActionWithAbort')

    def __del__(self):
        mock('__del__ AddTwoNumbersLongRunnungActionWithAbort')
