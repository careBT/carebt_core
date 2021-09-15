from test.global_mock import mock
from test.helloActions import LongRunningHelloWorldAction
from test.helloActions import MultiTickHelloWorldAction

from unittest.mock import call

from carebt.behaviorTree import BehaviorTree
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode

########################################################################


class MultiTickSequence(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(MultiTickHelloWorldAction)
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler(MultiTickHelloWorldAction,
                                 [NodeStatus.SUCCESS],
                                 '*',
                                 self.rule_handler_success)

        self.attach_rule_handler(MultiTickHelloWorldAction,
                                 [NodeStatus.RUNNING],
                                 '*',
                                 self.rule_handler_running)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

    def rule_handler_success(self):
        mock('rule_handler_success')

    def rule_handler_running(self):
        mock('rule_handler_running')

########################################################################


class LongRunningHelloWorldSequence(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(LongRunningHelloWorldAction, '?name')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler(LongRunningHelloWorldAction,
                                 [NodeStatus.SUCCESS],
                                 '*',
                                 self.rule_handler_success)

        self.attach_rule_handler(LongRunningHelloWorldAction,
                                 [NodeStatus.SUSPENDED],
                                 '*',
                                 self.rule_handler_suspended)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

    def rule_handler_success(self):
        mock('rule_handler_success')

    def rule_handler_suspended(self):
        mock('rule_handler_suspended')

########################################################################


class TestActionNode:

    def test_multi_tick_sequence(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(MultiTickSequence)
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ MultiTickSequence'),  # noqa: E501
                                       call('__init__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 1)'),  # noqa: E501
                                       call('rule_handler_running'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 2)'),  # noqa: E501
                                       call('rule_handler_running'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World ... takes several ticks ... (attempts = 3)'),  # noqa: E501
                                       call('rule_handler_running'),  # noqa: E501
                                       call('MultiTickHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('rule_handler_success'),  # noqa: E501
                                       call('__del__ MultiTickHelloWorldAction'),  # noqa: E501
                                       call('__del__ MultiTickSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_long_running_sequence(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_tick_rate_ms(100)
        bt.run(LongRunningHelloWorldSequence, '"Alice"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningHelloWorldSequence'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('rule_handler_suspended'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.SUCCESS'),  # noqa: E501
                                       call('rule_handler_success'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''
