from datetime import datetime

from tests.global_mock import mock
from tests.helloActions import MultiTickHelloWorldAction

from unittest.mock import call

from carebt.behaviorTree import BehaviorTree
from carebt.nodeStatus import NodeStatus
from carebt.rateControlNode import RateControlNode

########################################################################


class RateControlledMultiTickHelloWorld(RateControlNode):

    def __init__(self, bt):
        super().__init__(bt, 500)
        self.set_child(MultiTickHelloWorldAction)
        mock('__init__ {}'.format(self.__class__.__name__))

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class TestSequenceNode:

    def test_rate_controlled_multi_tick_hello_world(self):
        mock.reset_mock()
        bt = BehaviorTree()
        start = datetime.now()
        bt.run(RateControlledMultiTickHelloWorld)
        mock('bt finished')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 1500
        assert int(delta.total_seconds() * 1000) < 1600
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ RateControlledMultiTickHelloWorld'),  # noqa: E501
                                       call('__init__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 1)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 2)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 3)'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('__del__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('__del__ RateControlledMultiTickHelloWorld'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''
