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
from tests.helloActions import HelloWorldAction

from carebt.logger import AbstractLogger, LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
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

    def trace(self, msg: str):
        if(self._log_level == LogLevel.TRACE):
            mock('TRACE {}'.format(msg))

    def debug(self, msg: str):
        if(self._log_level == LogLevel.DEBUG):
            mock('DEBUG {}'.format(msg))

    def info(self, msg: str):
        if(self._log_level <= LogLevel.INFO):
            mock('INFO {}'.format(msg))

    def warn(self, msg: str):
        if(self._log_level <= LogLevel.WARN):
            mock('WARN {}'.format(msg))

    def error(self, msg: str):
        if(self._log_level <= LogLevel.ERROR):
            mock('ERROR {}'.format(msg))


class TestLogger:

    @patch('sys.stdout', new_callable=StringIO)
    def test_logger_trace(self, mock_print):
        self.logger = Logger()
        self.logger.set_log_level(LogLevel.TRACE)
        self.logger.trace('trace test')
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. TRACE trace test\n'  # noqa: E501
                           '....-..-.. ..:..:.. DEBUG debug test\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO info test\n'  # noqa: E501
                           '....-..-.. ..:..:.. WARN warn test\n'  # noqa: E501
                           '....-..-.. ..:..:.. ERROR error test\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_logger_debug(self, mock_print):
        self.logger = Logger()
        self.logger.set_log_level(LogLevel.DEBUG)
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
    def test_logger_info(self, mock_print):
        self.logger = Logger()
        self.logger.set_log_level(LogLevel.INFO)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. INFO info test\n'  # noqa: E501
                           '....-..-.. ..:..:.. WARN warn test\n'  # noqa: E501
                           '....-..-.. ..:..:.. ERROR error test\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_logger_warn(self, mock_print):
        self.logger = Logger()
        self.logger.set_log_level(LogLevel.WARN)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. WARN warn test\n'  # noqa: E501
                           '....-..-.. ..:..:.. ERROR error test\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_logger_error(self, mock_print):
        self.logger = Logger()
        self.logger.set_log_level(LogLevel.ERROR)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. ERROR error test\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_logger_off(self, mock_print):
        self.logger = Logger()
        self.logger.set_log_level(LogLevel.OFF)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('')
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_logger_level_off(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.OFF)
        bt_runner.run(HelloWorldAction)
        regex = re.compile('Hello World !!!\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_logger_level_debug(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.DEBUG)
        bt_runner.run(HelloWorldAction)
        regex = re.compile('....-..-.. ..:..:.. INFO ---------------------------------- tick-count: 1\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ticking RootSequence\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO creating HelloWorldAction\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ticking HelloWorldAction - NodeStatus.IDLE\n'  # noqa: E501
                           'Hello World !!!\n'  # noqa: E501
                           '....-..-.. ..:..:.. DEBUG searching contingency-handler for: HelloWorldAction - NodeStatus.SUCCESS - \n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO finished RootSequence\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ---------------------------------------------------\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO bt execution finished\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO status:  NodeStatus.SUCCESS\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO message: \n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ---------------------------------------------------\n')  # noqa: E501
        print(mock_print.getvalue())
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_custom_logger_level_off(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        cl = CustomLogger()
        cl.set_log_level(LogLevel.OFF)
        bt_runner.set_logger(cl)
        bt_runner.run(HelloWorldAction)
        regex = re.compile('Hello World !!!\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_custom_logger_level_debug(self, mock_print):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        cl = CustomLogger()
        cl.set_log_level(LogLevel.DEBUG)
        bt_runner.set_logger(cl)
        bt_runner.run(HelloWorldAction)
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
                                       call('DEBUG searching contingency-handler for: HelloWorldAction - NodeStatus.SUCCESS - '),  # noqa: E501
                                       call('__del__ HelloWorldAction'),  # noqa: E501
                                       call('INFO finished RootSequence'),  # noqa: E501
                                       call('INFO ---------------------------------------------------'),  # noqa: E501
                                       call('INFO bt execution finished'),  # noqa: E501
                                       call('INFO status:  NodeStatus.SUCCESS'),  # noqa: E501
                                       call('INFO message: '),  # noqa: E501
                                       call('INFO ---------------------------------------------------'),  # noqa: E501
                                       call('bt finished')]  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_message() == ''
