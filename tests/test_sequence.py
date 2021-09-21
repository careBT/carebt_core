from datetime import datetime

from tests.global_mock import mock
from tests.helloActions import HelloWorldAction
from tests.helloActions import LongRunningHelloWorldAction
from tests.helloActions import SayHelloAction

from unittest.mock import call

from carebt.behaviorTree import BehaviorTree
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode

########################################################################


class SimpleSequence(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class LongRunningSequence(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(LongRunningHelloWorldAction, '?name')
        self.attach_abort_handler(self.abort_handler)
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler(LongRunningHelloWorldAction,
                                 [NodeStatus.SUCCESS],
                                 '*',
                                 self.rule_handler_success)

        self.attach_rule_handler(LongRunningHelloWorldAction,
                                 [NodeStatus.FAILURE],
                                 'BOB_IS_NOT_ALLOWED',
                                 self.rule_handler_failure_bob)

        self.attach_rule_handler(LongRunningHelloWorldAction,
                                 [NodeStatus.FAILURE],
                                 'CHUCK_IS_NOT_ALLOWED',
                                 self.rule_handler_failure_chuck)

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

    def abort_handler(self) -> None:
        mock('abort_handler LongRunningSequence')

    def rule_handler_success(self):
        mock('rule_handler_success')

    def rule_handler_failure_bob(self):
        mock('rule_handler_failure_bob')
        self.abort()

    def rule_handler_failure_chuck(self):
        mock('rule_handler_failure_chuck')

########################################################################


class TestSequenceNode:

    def test_sequence(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SimpleSequence, '"Dave"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SimpleSequence'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Dave'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SimpleSequence'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_sequence_failure(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SimpleSequence, '"Bob"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SimpleSequence'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Bob'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SimpleSequence'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.FAILURE
        assert bt._instance.get_message() == 'BOB_IS_NOT_ALLOWED'

    def test_tick_rate_and_count(self):
        bt = BehaviorTree()
        assert bt.get_tick_count() == 0
        bt.set_tick_rate_ms(1000)
        start = datetime.now()
        bt.run(SimpleSequence, '"Dave"')
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 2950
        assert int(delta.total_seconds() * 1000) < 3050
        assert bt.get_tick_count() == 3

    def test_long_running_sequence_success(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(LongRunningSequence, '"Alice"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningSequence'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.SUCCESS'),  # noqa: E501
                                       call('rule_handler_success'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    def test_long_running_sequence_failure_chuck(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(LongRunningSequence, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningSequence'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.FAILURE'),  # noqa: E501
                                       call('rule_handler_failure_chuck'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.FAILURE
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    def test_long_running_sequence_failure_bob(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(LongRunningSequence, '"Bob"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ LongRunningSequence'),  # noqa: E501
                                       call('__init__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World ... takes very long ...'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: Hello World DONE !!!'),  # noqa: E501
                                       call('LongRunningHelloWorldAction: NodeStatus.FAILURE'),  # noqa: E501
                                       call('rule_handler_failure_bob'),  # noqa: E501
                                       call('abort_handler LongRunningSequence'),  # noqa: E501
                                       call('__del__ LongRunningHelloWorldAction'),  # noqa: E501
                                       call('__del__ LongRunningSequence'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'BOB_IS_NOT_ALLOWED'
