from tests.global_mock import mock

from threading import Timer

from carebt.actionNode import ActionNode
from carebt.nodeStatus import NodeStatus

########################################################################


class HelloWorldAction(ActionNode):

    def __init__(self, bt):
        super().__init__(bt)
        mock('__init__ {}'.format(self.__class__.__name__))

    def on_tick(self) -> None:
        mock('on_tick - Hello World')
        print('Hello World !!!')
        self.set_status(NodeStatus.SUCCESS)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class LongRunningHelloWorldAction(ActionNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self._name = 'Default Name'
        mock('__init__ {}'.format(self.__class__.__name__))

    def on_tick(self) -> None:
        mock('LongRunningHelloWorldAction: Hello World ... takes very long ...')
        self.set_status(NodeStatus.SUSPENDED)
        Timer(2, self.hello_done_callback).start()

    def on_abort(self) -> None:
        mock('on_abort LongRunningHelloWorldAction')

    def hello_done_callback(self) -> None:
        mock('LongRunningHelloWorldAction: Hello World DONE !!!')
        if(self._name == 'Bob'):
            self.set_status(NodeStatus.FAILURE)
            self.set_message('BOB_IS_NOT_ALLOWED')
            mock('LongRunningHelloWorldAction: NodeStatus.FAILURE')
        elif(self._name == 'Chuck'):
            self.set_status(NodeStatus.FAILURE)
            self.set_message('CHUCK_IS_NOT_ALLOWED')
            mock('LongRunningHelloWorldAction: NodeStatus.FAILURE')
        elif(self._name == 'Dave'):
            mock('LongRunningHelloWorldAction: abort')
            self.abort()
        else:
            self.set_status(NodeStatus.SUCCESS)
            mock('LongRunningHelloWorldAction: NodeStatus.SUCCESS')

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class MultiTickHelloWorldAction(ActionNode):

    def __init__(self, bt):
        super().__init__(bt)
        self.attempts = 1
        mock('__init__ {}'.format(self.__class__.__name__))

    def on_tick(self) -> None:
        if(self.attempts <= 3):
            mock('MultiTickHelloWorldAction: Hello World ... '
                 'takes several ticks ... (attempts = {})'
                 .format(self.attempts))
            self.attempts += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            mock('MultiTickHelloWorldAction: Hello World DONE !!!')
            self.set_status(NodeStatus.SUCCESS)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class MultiTickThrottledHelloWorldAction(ActionNode):

    def __init__(self, bt):
        super().__init__(bt)
        self.attempts = 1
        self.set_throttle_ms(500)
        mock('__init__ {}'.format(self.__class__.__name__))

    def on_tick(self) -> None:
        if(self.attempts <= 3):
            mock('MultiTickThrottledHelloWorldAction: Hello World ... '
                 'takes several ticks ... (attempts = {})'
                 .format(self.attempts))
            self.attempts += 1
            self.set_status(NodeStatus.RUNNING)
        else:
            mock('MultiTickThrottledHelloWorldAction: Hello World DONE !!!')
            self.set_status(NodeStatus.SUCCESS)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class SayHelloAction(ActionNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self._name = 'Default Name'
        mock('__init__ {}'.format(self.__class__.__name__))

    def on_tick(self) -> None:
        mock('on_tick - {}'.format(self._name))
        if(self._name == 'Chuck'):
            self.set_status(NodeStatus.FAILURE)
            self.set_message('CHUCK_IS_NOT_ALLOWED')
        elif(self._name == 'Judy'):
            self.set_status(NodeStatus.FAILURE)
            self.set_message('JUDY_IS_NOT_ALLOWED')
        elif(self._name == 'Bob'):
            self.set_status(NodeStatus.FAILURE)
            self.set_message('BOB_IS_NOT_ALLOWED')
        elif(self._name == 'Eve'):
            self.set_status(NodeStatus.FAILURE)
            self.set_message('EVE_IS_NOT_ALLOWED')
        elif(self._name == 'Ivan'):
            self.set_status(NodeStatus.FAILURE)
            self.set_message('IVAN_IS_NOT_ALLOWED')
        else:
            print('Hello {}!'.format(self._name))
            self.set_status(NodeStatus.SUCCESS)

    def on_abort(self) -> None:
        mock('on_abort - {}'.format(self._name))

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))
