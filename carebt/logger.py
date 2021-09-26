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

from abc import ABC
from abc import abstractmethod

from datetime import datetime


class AbstractLogger(ABC):

    def __init__(self):
        self._verbosity: bool = False

    def set_verbosity(self, verbosity: bool):
        self._verbosity = verbosity

    @abstractmethod
    def debug(self, msg: str):
        raise NotImplementedError

    @abstractmethod
    def info(self, msg: str):
        raise NotImplementedError

    @abstractmethod
    def warn(self, msg: str):
        raise NotImplementedError

    @abstractmethod
    def error(self, msg: str):
        raise NotImplementedError


class Logger(AbstractLogger):

    def __init__(self):
        super().__init__()

    # PROTECTED

    def _get_time(self):
        date_time = datetime.now()
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    # PUBLIC

    def debug(self, msg: str):
        if(self._verbosity):
            print('{} DEBUG {}'.format(self._get_time(), msg))

    def info(self, msg: str):
        if(self._verbosity):
            print('{} INFO {}'.format(self._get_time(), msg))

    def warn(self, msg: str):
        if(self._verbosity):
            print('{} WARN {}'.format(self._get_time(), msg))

    def error(self, msg: str):
        if(self._verbosity):
            print('{} ERROR {}'.format(self._get_time(), msg))
