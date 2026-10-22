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

import sched
from typing import Callable


class CareBTTimer:
    """The careBT `CareBTTimer` class.

    A one-shot timer which is executed by the careBT execution engine. The
    callback is not executed in a separate thread, but in the thread which
    ticks the behavior tree, right before the next tick after the timer has
    expired. Thus, the callback can safely change the state of a node.

    A `CareBTTimer` should not be created directly. Use
    `TreeNode.create_timer` or `BehaviorTreeRunner.create_timer` instead.

    Parameters
    ----------
    scheduler: sched.scheduler
        The scheduler of the `BehaviorTreeRunner`
    delay_ms: int
        The delay in milliseconds after which the callback is executed
    callback: Callable
        The function which is called when the timer expires

    """

    def __init__(self, scheduler: sched.scheduler, delay_ms: int, callback: Callable):
        self.__scheduler = scheduler
        self.__callback = callback
        self.__event = scheduler.enter(delay_ms / 1000, 0, self.__fire)

    # PRIVATE

    def __fire(self) -> None:
        callback = self.__callback
        self.__callback = None
        self.__event = None
        # callback can only be None if cancel raced with the scheduler
        if(callback is not None):  # pragma: no branch
            callback()

    # PUBLIC

    def cancel(self) -> None:
        """Cancel the timer.

        Can safely be called multiple times or after the timer has expired.
        """
        if(self.__event is not None):
            try:
                self.__scheduler.cancel(self.__event)
            except ValueError:
                # the event was already removed from the scheduler
                pass
        self.__event = None
        # release the callback (bound method) to make sure that the
        # object it is bound to can be destroyed by the gc
        self.__callback = None

    def is_active(self) -> bool:
        """Return whether the timer is still pending.

        Returns
        -------
        bool
            `True` if the timer has neither expired nor been canceled

        """
        return self.__event is not None
