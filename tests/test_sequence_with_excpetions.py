from tests.global_mock import mock
from tests.helloActions import HelloWorldAction, SayHelloAction

from unittest.mock import call

from carebt.behaviorTree import BehaviorTree
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode

########################################################################


class SequenceWithExceptionHandler(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name1 ?name2')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name1')
        self.add_child(SayHelloAction, '"Alice"')
        self.add_child(SayHelloAction, '"Grace"')
        self.add_child(SayHelloAction, '?name2')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler(SayHelloAction,
                                 [NodeStatus.FAILURE],
                                 'BOB_IS_NOT_ALLOWED',
                                 self.handle_name_is_bob)

        self.attach_rule_handler(SayHelloAction,
                                 [NodeStatus.FAILURE],
                                 'CHUCK_IS_NOT_ALLOWED',
                                 self.handle_name_is_chuck)

        self.attach_rule_handler(SayHelloAction,
                                 [NodeStatus.FAILURE],
                                 'EVE_IS_NOT_ALLOWED',
                                 self.handle_name_is_eve)

    def handle_name_is_bob(self) -> None:
        mock('handle_name_is_bob')
        print('No Problem Bob, keep going!')
        self.set_child_status(NodeStatus.SUCCESS)
        self.set_child_message(None)
        self.clear_child_message()

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def handle_name_is_eve(self) -> None:
        mock('handle_name_is_eve')
        print('Oh Eve, you are Frank')
        self.remove_susequent_children()
        self.add_child(SayHelloAction, '"Frank"')
        self.set_child_status(NodeStatus.SUCCESS)
        self.clear_child_message()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class TestSequenceNodeWithExceptions:

    # sequence runs straight forward
    def test_sequence_dave_heidi(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Dave" "Heidi"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Dave'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Grace'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Heidi'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    # name = Bob creates a FAILURE, but the exceptionHandler fixes
    # the issue and the sequence continues
    def test_sequence_failure_bob_heidi(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Bob" "Heidi"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Bob'),
                                       call('handle_name_is_bob'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Grace'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Heidi'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    # name = Chuck creates a FAILURE and the exceptionHandler
    # aborts the sequence
    def test_sequence_failure_chuck_heidi(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Chuck" "Heidi"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # name = Eve creates a FAILURE and the exceptionHandler
    # removes all subsequent children and adds a SayHelloAction
    # action with name = Frank
    def test_sequence_failure_eve_heidi(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Eve" "Heidi"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Eve'),
                                       call('handle_name_is_eve'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Frank'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    # name = Ivan creates a FAILURE and there is no exceptionHandler
    # thus the whole sequence fails
    def test_sequence_failure_ivan_heidi(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Ivan" "Heidi"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Ivan'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.FAILURE
        assert bt._instance.get_message() == 'IVAN_IS_NOT_ALLOWED'

    # name = Judy creates a FAILURE and there is no exceptionHandler
    # thus the whole sequence fails
    def test_sequence_failure_judy_heidi(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Judy" "Heidi"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Judy'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.FAILURE
        assert bt._instance.get_message() == 'JUDY_IS_NOT_ALLOWED'

    # name = Bob creates a FAILURE in the last child, but the exceptionHandler
    # fixes the issue and the sequence continues and has finally SUCCESS
    def test_sequence_failure_heidi_bob(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Heidi" "Bob"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Heidi'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Grace'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Bob'),
                                       call('handle_name_is_bob'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    # name = Chuck creates a FAILURE in the last child and the exceptionHandler
    # aborts the sequence
    def test_sequence_failure_heidi_chuck(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Heidi" "Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Heidi'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Grace'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # name = Eve creates a FAILURE in the last child and the exceptionHandler
    # removes all subsequent children (which are none) and adds a
    # SayHelloAction action with name = Frank
    def test_sequence_failure_heidi_eve(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Heidi" "Eve"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Heidi'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Grace'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Eve'),
                                       call('handle_name_is_eve'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Frank'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    # name = Ivan creates a FAILURE in the last child and there
    # is no exceptionHandler thus the whole sequence fails
    def test_sequence_failure_heidi_ivan(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Heidi" "Ivan"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Heidi'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Grace'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Ivan'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.FAILURE
        assert bt._instance.get_message() == 'IVAN_IS_NOT_ALLOWED'

    # name = Judy creates a FAILURE and there is no exceptionHandler
    # thus the whole sequence fails
    def test_sequence_failure_heidi_judy(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.run(SequenceWithExceptionHandler, '"Heidi" "Judy"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWithExceptionHandler'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Heidi'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Alice'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Grace'),
                                       call('__del__ SayHelloAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Judy'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWithExceptionHandler'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.FAILURE
        assert bt._instance.get_message() == 'JUDY_IS_NOT_ALLOWED'
