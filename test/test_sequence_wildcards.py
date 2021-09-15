from test.global_mock import mock
from test.helloActions import HelloWorldAction, SayHelloAction

from unittest.mock import call

from carebt.behaviorTree import BehaviorTree
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode

########################################################################


class SequenceWildcards_1(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler(SayHelloAction,
                                 [NodeStatus.FAILURE],
                                 'CHUCK_IS_NOT_ALLOWED',
                                 self.handle_name_is_chuck)

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class SequenceWildcards_2(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler(SayHelloAction,
                                 [NodeStatus.FAILURE],
                                 'CHUCK_*',
                                 self.handle_name_is_chuck)

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class SequenceWildcards_3(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler(SayHelloAction,
                                 [NodeStatus.FAILURE],
                                 '*',
                                 self.handle_name_is_chuck)

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class SequenceWildcards_4(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler('SayHelloAction',
                                 [NodeStatus.FAILURE],
                                 'CHUCK_IS_NOT_ALLOWED',
                                 self.handle_name_is_chuck)

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class SequenceWildcards_5(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler('Say*',
                                 [NodeStatus.FAILURE],
                                 'CHUCK_*',
                                 self.handle_name_is_chuck)

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class SequenceWildcards_6(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler('*',
                                 [NodeStatus.FAILURE],
                                 '*',
                                 self.handle_name_is_chuck)

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class SequenceWildcards_7(SequenceNode):

    def __init__(self, bt):
        super().__init__(bt, '?name')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name')
        self.add_child(SayHelloAction, '"Alice"')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_rule_handler('Say?ello?ction',
                                 [NodeStatus.FAILURE],
                                 'CHUCK_*_A??OWED',
                                 self.handle_name_is_chuck)

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class TestSequenceNodeWildcard:

    # SequenceWildcards_1; name = Chuck
    def test_sequence_chuck_1(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_verbosity(1)
        bt.run(SequenceWildcards_1, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWildcards_1'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWildcards_1'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # SequenceWildcards_2; name = Chuck
    def test_sequence_chuck_2(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_verbosity(1)
        bt.run(SequenceWildcards_2, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWildcards_2'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWildcards_2'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # SequenceWildcards_3; name = Chuck
    def test_sequence_chuck_3(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_verbosity(1)
        bt.run(SequenceWildcards_3, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWildcards_3'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWildcards_3'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # SequenceWildcards_4; name = Chuck
    def test_sequence_chuck_4(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_verbosity(1)
        bt.run(SequenceWildcards_4, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWildcards_4'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWildcards_4'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # SequenceWildcards_5; name = Chuck
    def test_sequence_chuck_5(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_verbosity(1)
        bt.run(SequenceWildcards_5, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWildcards_5'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWildcards_5'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # SequenceWildcards_6; name = Chuck
    def test_sequence_chuck_6(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_verbosity(1)
        bt.run(SequenceWildcards_6, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWildcards_6'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWildcards_6'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'

    # SequenceWildcards_7; name = Chuck
    def test_sequence_chuck_7(self):
        mock.reset_mock()
        bt = BehaviorTree()
        bt.set_verbosity(1)
        bt.run(SequenceWildcards_7, '"Chuck"')
        mock('bt finished')
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ SequenceWildcards_7'),
                                       call('__init__ HelloWorldAction'),
                                       call('on_tick - Hello World'),
                                       call('__del__ HelloWorldAction'),
                                       call('__init__ SayHelloAction'),
                                       call('on_tick - Chuck'),
                                       call('handle_name_is_chuck'),
                                       call('__del__ SayHelloAction'),
                                       call('__del__ SequenceWildcards_7'),
                                       call('bt finished')]
        assert bt._instance.get_status() == NodeStatus.ABORTED
        assert bt._instance.get_message() == 'CHUCK_IS_NOT_ALLOWED'
