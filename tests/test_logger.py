from tests.global_mock import mock
from tests.helloActions import HelloWorldAction

from carebt.logger import AbstractLogger
from carebt.behaviorTree import BehaviorTree
from carebt.logger import Logger
from carebt.nodeStatus import NodeStatus

from io import StringIO

import re

from unittest.mock import call
from unittest.mock import patch


class CustomLogger(AbstractLogger):

    def __init__(self):
        super().__init__()

    # PUBLIC

    def debug(self, msg: str):
        if(self._verbosity):
            mock('DEBUG {}'.format(msg))

    def info(self, msg: str):
        if(self._verbosity):
            mock('INFO {}'.format(msg))

    def warn(self, msg: str):
        if(self._verbosity):
            mock('WARN {}'.format(msg))

    def error(self, msg: str):
        if(self._verbosity):
            mock('ERROR {}'.format(msg))


class TestLogger:

    @patch('sys.stdout', new_callable=StringIO)
    def test_logger(self, mock_print):
        self.logger = Logger()
        self.logger.set_verbosity(True)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. DEBUG debug test\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO info test\n'  # noqa: E501
                           '....-..-.. ..:..:.. WARN warn test\n'  # noqa: E501
                           '....-..-.. ..:..:.. ERROR error test\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_logger_verbosity_false(self, mock_print):
        bt = BehaviorTree()
        bt.run(HelloWorldAction)
        regex = re.compile('Hello World !!!\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_logger_verbosity_true(self, mock_print):
        bt = BehaviorTree()
        bt.set_verbosity(True)
        bt.run(HelloWorldAction)
        regex = re.compile('....-..-.. ..:..:.. INFO ---------------------------------- tick-count: 1\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ticking RootSequence\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO creating HelloWorldAction\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ticking HelloWorldAction - NodeStatus.IDLE\n'  # noqa: E501
                           'Hello World !!!\n'  # noqa: E501
                           '....-..-.. ..:..:.. DEBUG searching rule-handler for: HelloWorldAction - NodeStatus.SUCCESS - \n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO finished RootSequence\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ---------------------------------------------------\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO bt execution finished\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO status:  NodeStatus.SUCCESS\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO message: \n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ---------------------------------------------------\n')  # noqa: E501
        print(mock_print.getvalue())
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_custom_logger_verbosity_false(self, mock_print):
        bt = BehaviorTree()
        cl = CustomLogger()
        bt.set_logger(cl)
        bt.run(HelloWorldAction)
        regex = re.compile('Hello World !!!\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_custom_logger_verbosity_true(self, mock_print):
        mock.reset_mock()
        bt = BehaviorTree()
        cl = CustomLogger()
        bt.set_logger(cl)
        bt.set_verbosity(True)
        bt.run(HelloWorldAction)
        regex = re.compile('Hello World !!!\n')
        mock('bt finished')
        print(mock_print.getvalue())
        print(mock.call_args_list)
        assert mock.call_args_list == [call('INFO ---------------------------------- tick-count: 1'),  # noqa: E501
                                       call('INFO ticking RootSequence'),  # noqa: E501
                                       call('INFO creating HelloWorldAction'),  # noqa: E501
                                       call('__init__ HelloWorldAction'),  # noqa: E501
                                       call('INFO ticking HelloWorldAction - NodeStatus.IDLE'),  # noqa: E501
                                       call('on_tick - Hello World'),  # noqa: E501
                                       call('DEBUG searching rule-handler for: HelloWorldAction - NodeStatus.SUCCESS - '),  # noqa: E501
                                       call('__del__ HelloWorldAction'),  # noqa: E501
                                       call('INFO finished RootSequence'),  # noqa: E501
                                       call('INFO ---------------------------------------------------'),  # noqa: E501
                                       call('INFO bt execution finished'),  # noqa: E501
                                       call('INFO status:  NodeStatus.SUCCESS'),  # noqa: E501
                                       call('INFO message: '),  # noqa: E501
                                       call('INFO ---------------------------------------------------'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt._instance.get_status() == NodeStatus.SUCCESS
        assert bt._instance.get_message() == ''
