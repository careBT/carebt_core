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

from datetime import datetime

from carebt.abstractLogger import AbstractLogger
from carebt.abstractLogger import LogLevel


class _PrintColors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = '\033[0m'


class SimplePrintLogger(AbstractLogger):
    """The careBT `SimplePrintLogger` class.

    A simple logger implementaion which prints the statements on standard
    output.
    """

    def __init__(self):
        super().__init__()

    # PROTECTED

    def _get_time(self):
        date_time = datetime.now()
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    # PUBLIC

    def trace(self, msg: str):
        if(self._log_level <= LogLevel.TRACE):
            print(f'{self._get_time()} TRACE {msg}')

    def debug(self, msg: str):
        if(self._log_level <= LogLevel.DEBUG):
            print(f'{self._get_time()} DEBUG {msg}')

    def info(self, msg: str):
        if(self._log_level <= LogLevel.INFO):
            print(f'{self._get_time()} INFO {msg}')

    def warn(self, msg: str):
        if(self._log_level <= LogLevel.WARN):
            print(_PrintColors.BOLD + _PrintColors.ORANGE
                  + f'{self._get_time()} WARN {msg}'
                  + _PrintColors.DEFAULT)

    def error(self, msg: str):
        if(self._log_level <= LogLevel.ERROR):
            print(_PrintColors.BOLD + _PrintColors.RED
                  + f'{self._get_time()} ERROR {msg}'
                  + _PrintColors.DEFAULT)
