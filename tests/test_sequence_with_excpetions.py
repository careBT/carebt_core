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

from tests.global_mock import mock
from tests.helloActions import HelloWorldAction, SayHelloAction

from unittest.mock import call

from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from carebt.sequenceNode import SequenceNode

########################################################################


class SequenceWithExceptionHandler(SequenceNode):

    def __init__(self, bt_runner):
        super().__init__(bt_runner, '?name1 ?name2')
        self.add_child(HelloWorldAction)
        self.add_child(SayHelloAction, '?name1')
        self.add_child(SayHelloAction, '"Alice"')
        self.add_child(SayHelloAction, '"Grace"')
        self.add_child(SayHelloAction, '?name2')
        mock('__init__ {}'.format(self.__class__.__name__))

        self.attach_contingency_handler(SayHelloAction,
                                        [NodeStatus.FAILURE],
                                        'BOB_IS_NOT_ALLOWED',
                                        self.handle_name_is_bob)

        self.attach_contingency_handler(SayHelloAction,
                                        [NodeStatus.FAILURE],
                                        'CHUCK_IS_NOT_ALLOWED',
                                        self.handle_name_is_chuck)

        self.attach_contingency_handler(SayHelloAction,
                                        [NodeStatus.FAILURE],
                                        'EVE_IS_NOT_ALLOWED',
                                        self.handle_name_is_eve)

    def handle_name_is_bob(self) -> None:
        mock('handle_name_is_bob')
        print('No Problem Bob, keep going!')
        self.fix_current_child()

    def handle_name_is_chuck(self) -> None:
        mock('handle_name_is_chuck')
        print('Oh Chuck, lets stop!')
        self.abort()

    def handle_name_is_eve(self) -> None:
        mock('handle_name_is_eve')
        print('Oh Eve, you are Frank')
        self.remove_susequent_children()
        self.add_child(SayHelloAction, '"Frank"')
        self.fix_current_child()

    def __del__(self):
        mock('__del__ {}'.format(self.__class__.__name__))

########################################################################


class TestSequenceNodeWithExceptions:

    # sequence runs straight forward
    def test_sequence_dave_heidi(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Dave" "Heidi"')
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
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    # name = Bob creates a FAILURE, but the exceptionHandler fixes
    # the issue and the sequence continues
    def test_sequence_failure_bob_heidi(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Bob" "Heidi"')
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
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    # name = Chuck creates a FAILURE and the exceptionHandler
    # aborts the sequence
    def test_sequence_failure_chuck_heidi(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Chuck" "Heidi"')
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
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == 'CHUCK_IS_NOT_ALLOWED'

    # name = Eve creates a FAILURE and the exceptionHandler
    # removes all subsequent children and adds a SayHelloAction
    # action with name = Frank
    def test_sequence_failure_eve_heidi(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Eve" "Heidi"')
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
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    # name = Ivan creates a FAILURE and there is no exceptionHandler
    # thus the whole sequence fails
    def test_sequence_failure_ivan_heidi(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Ivan" "Heidi"')
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
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'IVAN_IS_NOT_ALLOWED'

    # name = Judy creates a FAILURE and there is no exceptionHandler
    # thus the whole sequence fails
    def test_sequence_failure_judy_heidi(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Judy" "Heidi"')
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
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'JUDY_IS_NOT_ALLOWED'

    # name = Bob creates a FAILURE in the last child, but the exceptionHandler
    # fixes the issue and the sequence continues and has finally SUCCESS
    def test_sequence_failure_heidi_bob(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Heidi" "Bob"')
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
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    # name = Chuck creates a FAILURE in the last child and the exceptionHandler
    # aborts the sequence
    def test_sequence_failure_heidi_chuck(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Heidi" "Chuck"')
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
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == 'CHUCK_IS_NOT_ALLOWED'

    # name = Eve creates a FAILURE in the last child and the exceptionHandler
    # removes all subsequent children (which are none) and adds a
    # SayHelloAction action with name = Frank
    def test_sequence_failure_heidi_eve(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Heidi" "Eve"')
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
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    # name = Ivan creates a FAILURE in the last child and there
    # is no exceptionHandler thus the whole sequence fails
    def test_sequence_failure_heidi_ivan(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Heidi" "Ivan"')
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
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'IVAN_IS_NOT_ALLOWED'

    # name = Judy creates a FAILURE and there is no exceptionHandler
    # thus the whole sequence fails
    def test_sequence_failure_heidi_judy(self):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(SequenceWithExceptionHandler, '"Heidi" "Judy"')
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
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'JUDY_IS_NOT_ALLOWED'
