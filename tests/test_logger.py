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

from io import StringIO
import re
from unittest.mock import call
from unittest.mock import patch

from carebt.abstractLogger import AbstractLogger
from carebt.abstractLogger import LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from carebt.simplePrintLogger import SimplePrintLogger
from tests.actionNodes import HelloWorldAction
from tests.global_mock import mock


class CustomLogger(AbstractLogger):

    def __init__(self):
        super().__init__()

    # PUBLIC

    def trace(self, msg: str):
        if(self._log_level == LogLevel.TRACE):
            mock(f'TRACE {msg}')

    def debug(self, msg: str):
        if(self._log_level == LogLevel.DEBUG):
            mock(f'DEBUG {msg}')

    def info(self, msg: str):
        if(self._log_level <= LogLevel.INFO):
            mock(f'INFO {msg}')

    def warn(self, msg: str):
        if(self._log_level <= LogLevel.WARN):
            mock(f'WARN {msg}')

    def error(self, msg: str):
        if(self._log_level <= LogLevel.ERROR):
            mock(f'ERROR {msg}')


class TestLogger:

    @patch('sys.stdout', new_callable=StringIO)
    def test_simpleprintlogger_trace(self, mock_print):
        self.logger = SimplePrintLogger()
        self.logger.set_log_level(LogLevel.TRACE)
        self.logger.trace('trace test')
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. TRACE trace test\n'  # noqa: E501
                           '....-..-.. ..:..:.. DEBUG debug test\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO info test\n'  # noqa: E501
                           '.............-..-.. ..:..:.. WARN warn test....\n'  # noqa: E501
                           '.............-..-.. ..:..:.. ERROR error test....\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_simpleprintlogger_debug(self, mock_print):
        self.logger = SimplePrintLogger()
        self.logger.set_log_level(LogLevel.DEBUG)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. DEBUG debug test\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO info test\n'  # noqa: E501
                           '.............-..-.. ..:..:.. WARN warn test....\n'  # noqa: E501
                           '.............-..-.. ..:..:.. ERROR error test....\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_simpleprintlogger_info(self, mock_print):
        self.logger = SimplePrintLogger()
        self.logger.set_log_level(LogLevel.INFO)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('....-..-.. ..:..:.. INFO info test\n'  # noqa: E501
                           '.............-..-.. ..:..:.. WARN warn test....\n'  # noqa: E501
                           '.............-..-.. ..:..:.. ERROR error test....\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_simpleprintlogger_warn(self, mock_print):
        self.logger = SimplePrintLogger()
        self.logger.set_log_level(LogLevel.WARN)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('.............-..-.. ..:..:.. WARN warn test....\n'  # noqa: E501
                           '.............-..-.. ..:..:.. ERROR error test....\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_simpleprintlogger_error(self, mock_print):
        self.logger = SimplePrintLogger()
        self.logger.set_log_level(LogLevel.ERROR)
        self.logger.debug('debug test')
        self.logger.info('info test')
        self.logger.warn('warn test')
        self.logger.error('error test')
        regex = re.compile('.............-..-.. ..:..:.. ERROR error test....\n')  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))

    @patch('sys.stdout', new_callable=StringIO)
    def test_simpleprintlogger_off(self, mock_print):
        self.logger = SimplePrintLogger()
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
        regex = re.compile('HelloWorldAction: Hello World !!!\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_logger_level_debug(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.DEBUG)
        bt_runner.run(HelloWorldAction, '"Alice"')
        regex = re.compile('....-..-.. ..:..:.. INFO creating HelloWorldAction\n'  # noqa: E501
                           'HelloWorldAction: Hello Alice !!!\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ---------------------------------------------------\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO bt execution finished\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO status:  NodeStatus.SUCCESS\n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO contingency-message: \n'  # noqa: E501
                           '....-..-.. ..:..:.. INFO ---------------------------------------------------\n')  # noqa: E501
        print(mock_print.getvalue())
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_custom_logger_level_off(self, mock_print):
        bt_runner = BehaviorTreeRunner()
        cl = CustomLogger()
        cl.set_log_level(LogLevel.OFF)
        bt_runner.set_logger(cl)
        bt_runner.run(HelloWorldAction)
        regex = re.compile('HelloWorldAction: Hello World !!!\n')
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''

    @patch('sys.stdout', new_callable=StringIO)
    def test_action_custom_logger_level_debug(self, mock_print):
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        cl = CustomLogger()
        cl.set_log_level(LogLevel.DEBUG)
        bt_runner.set_logger(cl)
        bt_runner.run(HelloWorldAction)
        regex = re.compile('HelloWorldAction: Hello World !!!\n')
        print(mock_print.getvalue())
        print(mock.call_args_list)
        assert mock.call_args_list == [call('INFO creating HelloWorldAction'),  # noqa: E501
                                       call('__init__ HelloWorldAction'),  # noqa: E501
                                       call('WARN HelloWorldAction takes 1 argument(s), but 0 was/were provided'),  # noqa: E501
                                       call('HelloWorldAction: Hello World !!!'),  # noqa: E501
                                       call('__del__ HelloWorldAction'),  # noqa: E501
                                       call('INFO ---------------------------------------------------'),  # noqa: E501
                                       call('INFO bt execution finished'),  # noqa: E501
                                       call('INFO status:  NodeStatus.SUCCESS'),  # noqa: E501
                                       call('INFO contingency-message: '),  # noqa: E501
                                       call('INFO ---------------------------------------------------')]  # noqa: E501
        assert bool(re.match(regex, mock_print.getvalue()))
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
