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

from enum import IntEnum


class LogLevel(IntEnum):
    """An Enum representing the logging levels."""

    TRACE = 0
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    OFF = 5


class AbstractLogger(ABC):
    """The `AbstractLogger` interface.

    The `AbstractLogger` interface has to be implemented for
    a custom logger.
    """

    def __init__(self):
        self._log_level: LogLevel = LogLevel.INFO

    def set_log_level(self, log_level: LogLevel):
        self._log_level = log_level

    @abstractmethod
    def trace(self, msg: str):
        raise NotImplementedError

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
