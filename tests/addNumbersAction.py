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

    def on_tick(self) -> None:
        mock('on_tick - {} + {}'.format(self._x, self._y))
        if(self._x != 123 and self._y != 123):
            self._z = self._x + self._y
        self.set_status(NodeStatus.SUCCESS)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))
