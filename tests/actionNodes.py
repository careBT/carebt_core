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

from carebt.actionNode import ActionNode
from carebt.nodeStatus import NodeStatus
from tests.global_mock import mock

########################################################################


class HelloWorldAction(ActionNode):
    """The `HelloWorldAction` example node.

    The `HelloWorldAction` provides a classical Hello World example.
    It demonstrates a simple implementation of a careBT `ActionNode`.

    When running the `HelloWorldAction`,
    'HelloWorldAction: Hello World !!!' is printed on standard output. In case
    a `?name` is provided 'HelloWorldAction: Hello <name> !!!' is printed.

    Input Parameters
    ----------------
    ?name : str
        The name to print

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?name')
        mock('__init__ HelloWorldAction')
        self._name = None

    def on_tick(self) -> None:
        if self._name is None:
            mock('HelloWorldAction: Hello World !!!')
            print('HelloWorldAction: Hello World !!!')
        else:
            mock(f'HelloWorldAction: Hello {self._name} !!!')
            print(f'HelloWorldAction: Hello {self._name} !!!')
        self.set_status(NodeStatus.SUCCESS)

    def __del__(self):
        mock('__del__ HelloWorldAction')

########################################################################


class HelloWorldActionWithMessage(ActionNode):
    """The `HelloWorldActionWithMessage` example node.

    The `HelloWorldActionWithMessage` is a modfication of the `HelloWorldAction`
    example. The difference is that the node also provides a contingency-message.
    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner)
        mock('__init__ HelloWorldActionWithMessage')

    def on_tick(self) -> None:
        mock('HelloWorldActionWithMessage: Hello World !!!')
        print('HelloWorldActionWithMessage: Hello World !!!')
        self.set_status(NodeStatus.SUCCESS)
        self.set_contingency_message('HELLOWORLD_PRINTED')

    def __del__(self):
        mock('__del__ HelloWorldActionWithMessage')

########################################################################


class AddTwoNumbersAction(ActionNode):
    """The `AddTwoNumbersAction` example node.

    The `AddTwoNumbersAction` demonstrates a careBT `ActionNode` with two
    input parameters and one output parameter. It takes the two inputs,
    adds them and returns the result.

    Input Parameters
    ----------------
    ?x : int, default = 0
        The first value
    ?y : int, default = 0
        The second value

    Output Parameters
    -----------------
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
        mock(f'AddTwoNumbersAction: calculating: {self._x} + {self._y} = {self._z}')
        print(f'AddTwoNumbersAction: calculating: {self._x} + {self._y} = {self._z}')
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersAction')

########################################################################


class AddTwoNumbersActionMissingOutput(ActionNode):
    """The `AddTwoNumbersActionMissingOutput` example node.

    The `AddTwoNumbersActionMissingOutput` misses to set the ouput ?z.

    Input Parameters
    ----------------
    ?x : int, default = 0
        The first value
    ?y : int, default = 0
        The second value

    Output Parameters
    -----------------
    ?z : int
        Is missing

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?x ?y => ?z')
        mock('__init__ AddTwoNumbersActionMissingOutput')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersActionMissingOutput')

    def on_tick(self) -> None:
        mock('on_tick AddTwoNumbersActionMissingOutput')
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersAction')

########################################################################


class AddTwoNumbersActionWithFailure(ActionNode):
    """The `AddTwoNumbersActionWithFailure` example node.

    The `AddTwoNumbersActionWithFailure` is an extension of the
    `AddTwoNumbersAction`. It does not have default values for the two input
    parameters `?x` and `?y`. But in case that at least one of the two input
    parameters is missing the `AddTwoNumbersActionWithFailure` Node switches
    to state `FAILURE` with the message `NOT_TWO_NUMBERS_PROVIDED`.

    Input Parameters
    ----------------
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    Contingencies
    -------------
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
            mock('AddTwoNumbersActionWithFailure: calculating: '
                 + f'{self._x} + {self._y} = {self._z}')
            print('AddTwoNumbersActionWithFailure: calculating: '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersActionWithFailure')

    def __del__(self):
        mock('__del__ AddTwoNumbersActionWithFailure')

########################################################################


class AddTwoNumbersMultiTickAction(ActionNode):
    """The `AddTwoNumbersMultiTickAction` example node.

    The `AddTwoNumbersMultiTickAction` is a variation of the
    `AddTwoNumbersAction` which demonstrates how it looks like when a
    `ActionNode` requires more ticks to complete. To make things simple
    the amount of ticks required to complete the action is provided as
    input parameter.

    Input Parameters
    ----------------
    ?ticks : int
        Number of ticks requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
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
            mock(f'AddTwoNumbersMultiTickAction: (tick_count = {self.tick_count}/{self._ticks})')
            print(f'AddTwoNumbersMultiTickAction: (tick_count = {self.tick_count}/{self._ticks})')
            self.tick_count += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            self._z = self._x + self._y
            mock(f'AddTwoNumbersMultiTickAction: DONE '
                 + f'{self._x} + {self._y} = {self._z}')
            print(f'AddTwoNumbersMultiTickAction: DONE '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersMultiTickAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersMultiTickAction')

########################################################################


class AddTwoNumbersMultiTickActionWithTimeout(ActionNode):
    """The `AddTwoNumbersMultiTickActionWithTimeout` example node.

    The `AddTwoNumbersMultiTickActionWithTimeout` is a variation of the
    `AddTwoNumbersAction` which demonstrates how it looks like when a
    `ActionNode` requires more ticks to complete. To make things simple
    the amount of ticks required to complete the action is provided as
    input parameter.

    Input Parameters
    ----------------
    ?ticks : int
        Number of ticks requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?ticks ?x ?y => ?z')
        mock('__init__ AddTwoNumbersMultiTickActionWithTimeout')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersMultiTickActionWithTimeout')
        self.tick_count = 1
        self.set_timeout(1000)

    def on_tick(self) -> None:
        if(self.tick_count <= self._ticks):
            mock('AddTwoNumbersMultiTickActionWithTimeout: (tick_count = '
                 + f'{self.tick_count}/{self._ticks})')
            print('AddTwoNumbersMultiTickActionWithTimeout: (tick_count = '
                  + f'{self.tick_count}/{self._ticks})')
            self.tick_count += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            self._z = self._x + self._y
            mock('AddTwoNumbersMultiTickActionWithTimeout: DONE '
                 + f'{self._x} + {self._y} = {self._z}')
            print('AddTwoNumbersMultiTickActionWithTimeout: DONE '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)

    def on_timeout(self) -> None:
        mock('on_timeout AddTwoNumbersMultiTickActionWithTimeout')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersMultiTickActionWithTimeout')

    def __del__(self):
        mock('__del__ AddTwoNumbersMultiTickActionWithTimeout')

########################################################################


class AddTwoNumbersThrottledMultiTickAction(ActionNode):
    """The `AddTwoNumbersThrottledMultiTickAction` example node.

    The `AddTwoNumbersThrottledMultiTickAction` is a variation of the
    `AddTwoNumbersMultiTickAction` which demonstrates how ticking an
    `ActionNode` can be throttled to the provided value. In this example
    this value is set to 500ms.

    Input Parameters
    ----------------
    ?ticks : int
        Number of ticks requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
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
            mock('AddTwoNumbersThrottledMultiTickAction: (tick_count = '
                 + f'{self.tick_count}/{self._ticks})')
            print('AddTwoNumbersThrottledMultiTickAction: (tick_count = '
                  + f'{self.tick_count}/{self._ticks})')
            self.tick_count += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            self._z = self._x + self._y
            mock('AddTwoNumbersThrottledMultiTickAction: DONE '
                 + f'{self._x} + {self._y} = {self._z}')
            print('AddTwoNumbersThrottledMultiTickAction: DONE '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersThrottledMultiTickAction')

    def __del__(self):
        mock('__del__ AddTwoNumbersThrottledMultiTickAction')

########################################################################


class AddTwoNumbersLongRunningAction(ActionNode):
    """The `AddTwoNumbersLongRunningAction` example node.

    The `AddTwoNumbersLongRunningAction` is a variation of the
    `AddTwoNumbersAction` which demonstrates how it looks like when a
    `ActionNode` executes an asynchronous function. To make things simple the
    asynchronous function is implemented with a simple Python timer and
    the amount of milliseconds the asynchronous function requires to complete
    is provided as input parameter.

    Input Parameters
    ----------------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?x ?y => ?z')
        mock('__init__ AddTwoNumbersLongRunningAction')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersLongRunningAction')

    def on_tick(self) -> None:
        mock(f'AddTwoNumbersLongRunningAction: calculating {self._calctime} ms ...')
        print(f'AddTwoNumbersLongRunningAction: calculating {self._calctime} ms ...')
        self.set_status(NodeStatus.SUSPENDED)
        self.__done_timer = Timer(self._calctime / 1000, self.done_callback)
        self.__done_timer.start()

    def done_callback(self) -> None:
        self._z = self._x + self._y
        mock('AddTwoNumbersLongRunningAction: done: '
             + f'{self._x} + {self._y} = {self._z}')
        print('AddTwoNumbersLongRunningAction: done: '
              + f'{self._x} + {self._y} = {self._z}')
        self.set_status(NodeStatus.SUCCESS)

    def on_abort(self) -> None:
        mock('on_abort AddTwoNumbersLongRunningAction')
        self.__done_timer.cancel()

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersLongRunningAction')
        # set the timer to None to make sure that all references (bound method)
        # are released and the object gets destroyed by gc
        self.__done_timer = None

    def __del__(self):
        mock('__del__ AddTwoNumbersLongRunningAction')

########################################################################


class AddTwoNumbersLongRunningActionWithAbort(ActionNode):
    """The `AddTwoNumbersLongRunningActionWithAbort` example node.

    The `AddTwoNumbersLongRunningActionWithAbort` is a variation of the
    `AddTwoNumbersLongRunningAction`. It uses the timeout callback to abort
    the `ActionNode` in case that the execution (asynchronous function) takes
    to long.

    Input Parameters
    ----------------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    Contingencies
    -------------
    FAILURE:
        NOT_TWO_NUMBERS_PROVIDED
            At least one of the two input parameters is missing.
    ABORT:
        TIMEOUT
            The execution time exceeded the timeout

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?x ?y => ?z')
        mock('__init__ AddTwoNumbersLongRunningActionWithAbort')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersLongRunningActionWithAbort')
        self.__TIMEOUT: int = 1000
        self.set_timeout(self.__TIMEOUT)

    def on_tick(self) -> None:
        if(self._x is None or self._y is None):
            mock('AddTwoNumbersLongRunningActionWithAbort: '
                 'You did not provide two numbers!')
            print('AddTwoNumbersLongRunningActionWithAbort: '
                  'You did not provide two numbers!')
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('NOT_TWO_NUMBERS_PROVIDED')
        else:
            mock(f'AddTwoNumbersLongRunningActionWithAbort: calculating {self._calctime} ms ... '
                 + f'(timeout = {self.__TIMEOUT} ms)')
            print(f'AddTwoNumbersLongRunningActionWithAbort: calculating {self._calctime} ms ... '
                  + f'(timeout = {self.__TIMEOUT} ms)')
            self.set_status(NodeStatus.SUSPENDED)
            self.__done_timer = Timer(self._calctime / 1000, self.done_callback)
            self.__done_timer.start()

    def done_callback(self) -> None:
        # make sure that the node is still suspended, this is especially
        # important if also a timeout is used. If both occure in the same
        # careBT tick
        if(self.get_status() == NodeStatus.SUSPENDED):
            self._z = self._x + self._y
            mock('AddTwoNumbersLongRunningActionWithAbort: done_callback: '
                 + f'{self._x} + {self._y} = {self._z}')
            print('AddTwoNumbersLongRunningActionWithAbort: done_callback: '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)
            self.__done_timer.cancel()

    def on_timeout(self) -> None:
        mock('on_timeout AddTwoNumbersLongRunningActionWithAbort')
        print('on_timeout AddTwoNumbersLongRunningActionWithAbort')
        self.abort()
        self.set_contingency_message('TIMEOUT')

    def on_abort(self) -> None:
        mock('on_abort AddTwoNumbersLongRunningActionWithAbort')
        print('on_abort AddTwoNumbersLongRunningActionWithAbort')
        self.__done_timer.cancel()

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersLongRunningActionWithAbort')
        # set the timer to None to make sure that all references (bound method)
        # are released and the object gets destroyed by gc
        self.__done_timer = None

    def __del__(self):
        mock('__del__ AddTwoNumbersLongRunningActionWithAbort')

########################################################################


class AddTwoNumbersLongRunningActionMissingCallback(ActionNode):
    """The `AddTwoNumbersLongRunningActionMissingCallback` example node.

    The `AddTwoNumbersLongRunningActionMissingCallback` is a variant of the
    `AddTwoNumbersLongRunningActionWithAbort` but does not override on_timeout.

    Input Parameters
    ----------------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?x ?y => ?z')
        mock('__init__ AddTwoNumbersLongRunningActionMissingCallback')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersLongRunningActionMissingCallback')
        self.__TIMEOUT: int = 1000
        self.set_timeout(self.__TIMEOUT)

    def on_tick(self) -> None:
        if(self._x is None or self._y is None):
            mock('AddTwoNumbersLongRunningActionMissingCallback: '
                 'You did not provide two numbers!')
            print('AddTwoNumbersLongRunningActionMissingCallback: '
                  'You did not provide two numbers!')
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('NOT_TWO_NUMBERS_PROVIDED')
        else:
            mock('AddTwoNumbersLongRunningActionMissingCallback: calculating '
                 + f'{self._calctime} ms ... (timeout = {self.__TIMEOUT} ms)')
            print('AddTwoNumbersLongRunningActionMissingCallback: calculating '
                  + f'{self._calctime} ms ... (timeout = {self.__TIMEOUT} ms)')
            self.set_status(NodeStatus.SUSPENDED)
            self.__done_timer = Timer(self._calctime / 1000, self.done_callback)
            self.__done_timer.start()

    def done_callback(self) -> None:
        # make sure that the node is still suspended, this is especially
        # important if also a timeout is used. If both occure in the same
        # careBT tick
        if(self.get_status() == NodeStatus.SUSPENDED):
            self._z = self._x + self._y
            mock('AddTwoNumbersLongRunningActionMissingCallback: done_callback: '
                 + f'{self._x} + {self._y} = {self._z}')
            print('AddTwoNumbersLongRunningActionMissingCallback: done_callback: '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)
            self.__done_timer.cancel()

    def on_abort(self) -> None:
        mock('on_abort AddTwoNumbersLongRunningActionMissingCallback')
        print('on_abort AddTwoNumbersLongRunningActionMissingCallback')
        self.__done_timer.cancel()

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersLongRunningActionMissingCallback')
        # set the timer to None to make sure that all references (bound method)
        # are released and the object gets destroyed by gc
        self.__done_timer = None

    def __del__(self):
        mock('__del__ AddTwoNumbersLongRunningActionMissingCallback')

########################################################################


class AddTwoNumbersLongRunningActionMissingCallback2(ActionNode):
    """The `AddTwoNumbersLongRunningActionMissingCallback2` example node.

    The `AddTwoNumbersLongRunningActionMissingCallback2` is a variant of the
    `AddTwoNumbersLongRunningActionMissingCallback` but does not override on_abort.

    Input Parameters
    ----------------
    ?calctime : int (ms)
        Milliseconds requiered to complete
    ?x : int
        The first value
    ?y : int
        The second value

    Output Parameters
    -----------------
    ?z : int
        The sum of ?x and ?y

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?calctime ?x ?y => ?z')
        mock('__init__ AddTwoNumbersLongRunningActionMissingCallback2')

    def on_init(self) -> None:
        mock('on_init AddTwoNumbersLongRunningActionMissingCallback2')
        self.__TIMEOUT: int = 1000
        self.set_timeout(self.__TIMEOUT)

    def on_tick(self) -> None:
        if(self._x is None or self._y is None):
            mock('AddTwoNumbersLongRunningActionMissingCallback2: '
                 'You did not provide two numbers!')
            print('AddTwoNumbersLongRunningActionMissingCallback2: '
                  'You did not provide two numbers!')
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('NOT_TWO_NUMBERS_PROVIDED')
        else:
            mock('AddTwoNumbersLongRunningActionMissingCallback2: calculating '
                 + f'{self._calctime} ms ... (timeout = {self.__TIMEOUT} ms)')
            print('AddTwoNumbersLongRunningActionMissingCallback2: calculating '
                  + f'{self._calctime} ms ... (timeout = {self.__TIMEOUT} ms)')
            self.set_status(NodeStatus.SUSPENDED)
            self.__done_timer = Timer(self._calctime / 1000, self.done_callback)
            self.__done_timer.start()

    def done_callback(self) -> None:
        # make sure that the node is still suspended, this is especially
        # important if also a timeout is used. If both occure in the same
        # careBT tick
        if(self.get_status() == NodeStatus.SUSPENDED):
            self._z = self._x + self._y
            mock('AddTwoNumbersLongRunningActionMissingCallback: done_callback: '
                 + f'{self._x} + {self._y} = {self._z}')
            print('AddTwoNumbersLongRunningActionMissingCallback: done_callback: '
                  + f'{self._x} + {self._y} = {self._z}')
            self.set_status(NodeStatus.SUCCESS)
            self.__done_timer.cancel()

    def on_delete(self) -> None:
        mock('on_delete AddTwoNumbersLongRunningActionMissingCallback2')
        self.__done_timer.cancel()
        # set the timer to None to make sure that all references (bound method)
        # are released and the object gets destroyed by gc
        self.__done_timer = None

    def __del__(self):
        mock('__del__ AddTwoNumbersLongRunningActionMissingCallback2')

########################################################################


class ShowNumberAction(ActionNode):
    """The `ShowNumberAction` example node.

    The `ShowNumberAction` simply prints the provided numer on the standard
    output. If `?number` the default -1 is used.

    Input Parameters
    ----------------
    ?number : int (default = -1)
        The number that should be printed.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?number')
        mock('__init__ ShowNumberAction')

    def on_init(self) -> None:
        mock('on_init ShowNumberAction')
        if(self._number is None):
            self._number = -1

    def on_tick(self) -> None:
        mock(f'ShowNumberAction: The numer is: {self._number}!')
        print(f'ShowNumberAction: The numer is: {self._number}!')
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete ShowNumberAction')

    def __del__(self):
        mock('__del__ ShowNumberAction')

########################################################################


class ProvideMissingNumbersAction(ActionNode):
    """The `ProvideMissingNumbersAction` example node.

    The `ProvideMissingNumbersAction` is an `ActionNode` with two output parameters.
    The ouput values are hardcoded to 11 respectively 22.

    Output Parameters
    -----------------
    ?a : int
        The first number: 11
    ?b : int
        The second number: 22

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '=> ?a ?b')
        mock('__init__ ProvideMissingNumbersAction')

    def on_init(self) -> None:
        mock('on_init ProvideMissingNumbersAction')

    def on_tick(self) -> None:
        mock('ProvideMissingNumbersAction: provide missing numbers!')
        print('ProvideMissingNumbersAction: provide missing numbers!')
        self._a = 11
        self._b = 22
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete ProvideMissingNumbersAction')

    def __del__(self):
        mock('__del__ ProvideMissingNumbersAction')

########################################################################


class FixMissingNumbersAction(ActionNode):
    """The `FixMissingNumbersAction` example node.

    The `FixMissingNumbersAction` is an `ActionNode` with one output parameters.
    The ouput value is set to 42.

    Output Parameters
    -----------------
    ?out : int
        The number: 42

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '=> ?out')
        mock('__init__ FixMissingNumbersAction')

    def on_init(self) -> None:
        mock('on_init FixMissingNumbersAction')

    def on_tick(self) -> None:
        mock('FixMissingNumbersAction: fix missing numbers!')
        print('FixMissingNumbersAction: fix missing numbers!')
        self._out = 42
        self.set_status(NodeStatus.SUCCESS)

    def on_delete(self) -> None:
        mock('on_delete FixMissingNumbersAction')

    def __del__(self):
        mock('__del__ FixMissingNumbersAction')

########################################################################


class TickCountingAction(ActionNode):
    """The `TickCountingAction` example node.

    The `TickCountingAction` increments the ?count and returns it on each tick. If
    the ?count is equal to the ?goal the nodes completes with `SUCCESS`.

    Input Parameters
    ----------------
    ?id : int
        The id to identify the node.
    ?goal : int (Default = 10)
        The goal tick count.
    ?success : bool (Default = True)
        Wether the node should succeed or fail.

    Output Parameters
    -----------------
    ?count : int
        The current tick count.

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?id ?goal ?success => ?count')
        mock('__init__ TickCountingAction')

    def on_init(self) -> None:
        mock(f'on_init TickCountingAction id = {self._id}')
        print(f'on_init TickCountingAction id = {self._id}')
        self._count = 1
        if(self._goal is None):
            self._goal = 10
        if(self._success is None):
            self._success = True

    def on_tick(self) -> None:
        if(self._count >= self._goal):
            if(self._success is True):
                mock(f'TickCountingAction id = {self._id} DONE with SUCCESS')
                print(f'TickCountingAction id = {self._id} DONE with SUCCESS')
                self.set_status(NodeStatus.SUCCESS)
            else:
                mock(f'TickCountingAction id = {self._id} DONE with FAILURE')
                print(f'TickCountingAction id = {self._id} DONE with FAILURE')
                self.set_status(NodeStatus.FAILURE)
                self.set_contingency_message('COUNTING_ERROR')
        else:
            mock(f'TickCountingAction id = {self._id} tick: {self._count}/{self._goal}')
            print(f'TickCountingAction id = {self._id} tick: {self._count}/{self._goal}')
            self._count += 1
            self.set_status(NodeStatus.RUNNING)

    def on_abort(self) -> None:
        mock(f'on_abort TickCountingAction id = {self._id}')
        print(f'on_abort TickCountingAction id = {self._id}')

    def on_delete(self) -> None:
        mock(f'on_delete TickCountingAction id = {self._id}')
        print(f'on_delete TickCountingAction id = {self._id}')

    def __del__(self):
        mock(f'__del__ TickCountingAction id = {self._id}')

########################################################################


class FailOnCountAction(ActionNode):
    """The `FailOnCountAction` example node.

    The `FailOnCountAction` fails as soon as the ?goal is reached by ?count.

    Input Parameters
    ----------------
    ?goal : int (Default = 10)
        The goal tick count.
    ?count : int
        The tick count

    """

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?goal ?count')
        mock('__init__ FailOnCountAction')

    def on_init(self) -> None:
        mock('on_init FailOnCountAction')
        print('on_init FailOnCountAction')
        if(self._goal is None):
            self._goal = 10

    def on_tick(self) -> None:
        if(self._count >= self._goal):
            mock('FailOnCountAction DONE with FAILURE')
            print('FailOnCountAction DONE with FAILURE')
            self.set_status(NodeStatus.FAILURE)
            self.set_contingency_message('COUNTING_ERROR')
        else:
            mock(f'FailOnCountAction tick: {self._count}/{self._goal}')
            print(f'FailOnCountAction tick: {self._count}/{self._goal}')
            self._count += 1
            self.set_status(NodeStatus.RUNNING)

    def on_abort(self) -> None:
        mock('on_abort FailOnCountAction')
        print('on_abort FailOnCountAction')

    def on_delete(self) -> None:
        mock('on_delete FailOnCountAction')
        print('on_delete FailOnCountAction')

    def __del__(self):
        mock('__del__ FailOnCountAction')
