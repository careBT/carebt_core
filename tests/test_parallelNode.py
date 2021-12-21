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
from unittest.mock import call

from carebt.abstractLogger import LogLevel
from carebt.behaviorTreeRunner import BehaviorTreeRunner
from carebt.nodeStatus import NodeStatus
from tests.global_mock import mock
from tests.parallelNodes import AddTwoNumbersParallel
from tests.parallelNodes import AsyncAddChildParallel
from tests.parallelNodes import CountAbortParallel
from tests.parallelNodes import CountAbortParallelWithTick
from tests.parallelNodes import ParallelRemoveSuccess
from tests.parallelNodes import TickCountingParallel
from tests.parallelNodes import TickCountingParallelDel
from tests.parallelNodes import TickCountingParallelDelAdd1
from tests.parallelNodes import TickCountingParallelDelAdd2
from tests.parallelNodes import TickCountingParallelDelAllAdd
from tests.parallelNodes import TickCountingParallelWithAbort

########################################################################


class TestParallelNode:
    """Test the `ParallelNode`."""

    ########################################################################

    def test_AddTwoNumbersParallel(self):
        """Test the `AddTwoNumbersParallel` node."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AddTwoNumbersParallel)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AddTwoNumbersParallel'),
                                       call('on_init AddTwoNumbersParallel'),
                                       call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('__init__ AddTwoNumbersAction'),
                                       call('on_init AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 1 + 2 = 3'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 2 + 3 = 5'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('AddTwoNumbersAction: calculating: 3 + 4 = 7'),
                                       call('on_delete AddTwoNumbersAction'),
                                       call('__del__ AddTwoNumbersAction'),
                                       call('on_delete AddTwoNumbersParallel'),
                                       call('__del__ AddTwoNumbersParallel')]

    ########################################################################

    def test_TickCountingParallel_threshold_3_success_3(self):
        """Test the `TickCountingParallel` node.

        Test the `TickCountingParallel`. The success_threshold is set to 3. All three
        children count up to 4 and complete then with `SUCCESS`. Thus the whole `ParallelNode'
        completes with `SUCCESS`
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(TickCountingParallel, '3 4 True 4 True 4 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ TickCountingParallel'),
                                       call('on_init TickCountingParallel success_threshold = 3'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/4'),
                                       call('TickCountingAction id = 2 tick: 1/4'),
                                       call('TickCountingAction id = 3 tick: 1/4'),
                                       call('TickCountingAction id = 1 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 2/4'),
                                       call('TickCountingAction id = 3 tick: 2/4'),
                                       call('TickCountingAction id = 1 tick: 3/4'),
                                       call('TickCountingAction id = 2 tick: 3/4'),
                                       call('TickCountingAction id = 3 tick: 3/4'),
                                       call('TickCountingAction id = 1 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('TickCountingAction id = 2 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('TickCountingAction id = 3 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('on_delete TickCountingParallel'),
                                       call('__del__ TickCountingParallel')]

    def test_TickCountingParallel_threshold_3_fail_1(self):
        """Test the `TickCountingParallel` node.

        Test the `TickCountingParallel`. The success_threshold is set to 3. One of the children
        fails after 3 ticks. Thus the whole `ParallelNode' completes with `FAILURE`.
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(TickCountingParallel, '3 4 True 3 False 5 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'COUNTING_ERROR'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ TickCountingParallel'),
                                       call('on_init TickCountingParallel success_threshold = 3'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/4'),
                                       call('TickCountingAction id = 2 tick: 1/3'),
                                       call('TickCountingAction id = 3 tick: 1/5'),
                                       call('TickCountingAction id = 1 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 2/3'),
                                       call('TickCountingAction id = 3 tick: 2/5'),
                                       call('TickCountingAction id = 1 tick: 3/4'),
                                       call('TickCountingAction id = 2 DONE with FAILURE'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('TickCountingAction id = 3 tick: 3/5'),
                                       call('on_abort TickCountingAction id = 1'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('on_abort TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('on_delete TickCountingParallel'),
                                       call('__del__ TickCountingParallel')]

    def test_TickCountingParallel_threshold_2_success_all(self):
        """Test the `TickCountingParallel` node.

        Test the `TickCountingParallel`. The success_threshold is set to 3. All children
        succeed, but in different ticks.
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(TickCountingParallel, '2 2 True 9 True 4 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ TickCountingParallel'),
                                       call('on_init TickCountingParallel success_threshold = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/2'),
                                       call('TickCountingAction id = 2 tick: 1/9'),
                                       call('TickCountingAction id = 3 tick: 1/4'),
                                       call('TickCountingAction id = 1 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('TickCountingAction id = 2 tick: 2/9'),
                                       call('TickCountingAction id = 3 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 3/9'),
                                       call('TickCountingAction id = 3 tick: 3/4'),
                                       call('TickCountingAction id = 2 tick: 4/9'),
                                       call('TickCountingAction id = 3 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('on_abort TickCountingAction id = 2'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('on_delete TickCountingParallel'),
                                       call('__del__ TickCountingParallel')]

    ########################################################################

    def test_TickCountingParallelWithAbort_threshold_3_fail_1(self):
        """Test the `TickCountingParallelWithAbort` node.

        Test the `TickCountingParallelWithAbort`. The success_threshold is set to 3. One of
        the children fails after 3 ticks. The contingengy-handler aborts the whole `ParralelNode`.
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(TickCountingParallelWithAbort, '3 4 True 3 False 5 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.ABORTED
        assert bt_runner._instance.get_contingency_message() == 'ANOTHER_COUNTING_ERROR'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ TickCountingParallelWithAbort'),
                                       call('on_init TickCountingParallelWithAbort success_threshold = 3'),  # noqa: E501
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/4'),
                                       call('TickCountingAction id = 2 tick: 1/3'),
                                       call('TickCountingAction id = 3 tick: 1/5'),
                                       call('TickCountingAction id = 1 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 2/3'),
                                       call('TickCountingAction id = 3 tick: 2/5'),
                                       call('TickCountingAction id = 1 tick: 3/4'),
                                       call('TickCountingAction id = 2 DONE with FAILURE'),
                                       call('on_abort TickCountingAction id = 1'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('on_abort TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('on_delete TickCountingParallelWithAbort'),
                                       call('__del__ TickCountingParallelWithAbort')]

    ########################################################################

    def test_TickCountingParallelDelAdd1_threshold_3_fail_1(self):
        """Test the `TickCountingParallelDelAdd1` node.

        Test the `TickCountingParallelDelAdd1`. The success_threshold is set to 2. One of the
        children fails after 3 ticks. The contingengy-handler removed child #2 (id=3), adds
        new new children and sets the success_threshold to 3.
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(TickCountingParallelDelAdd1, '2 4 True 3 False 5 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        call('__init__ TickCountingParallelDelAdd1'),
        assert mock.call_args_list == [call('__init__ TickCountingParallelDelAdd1'),
                                       call('on_init TickCountingParallelDelAdd1 success_threshold = 2'),  # noqa: E501
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/4'),
                                       call('TickCountingAction id = 2 tick: 1/3'),
                                       call('TickCountingAction id = 3 tick: 1/5'),
                                       call('TickCountingAction id = 1 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 2/3'),
                                       call('TickCountingAction id = 3 tick: 2/5'),
                                       call('TickCountingAction id = 1 tick: 3/4'),
                                       call('TickCountingAction id = 2 DONE with FAILURE'),
                                       call('on_abort TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 4'),
                                       call('TickCountingAction id = 1 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('TickCountingAction id = 4 tick: 1/3'),
                                       call('TickCountingAction id = 4 tick: 2/3'),
                                       call('TickCountingAction id = 4 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 4'),
                                       call('__del__ TickCountingAction id = 4'),
                                       call('on_delete TickCountingParallelDelAdd1'),
                                       call('__del__ TickCountingParallelDelAdd1')]

    ########################################################################

    def test_TickCountingParallelDelAdd2_threshold_3_fail_1(self):
        """Test the `TickCountingParallelDelAdd2` node.

        Test the `TickCountingParallelDelAdd2`. The success_threshold is set to 2. One of the
        children fails after 3 ticks. The contingengy-handler removed child #2 (id=3), adds
        new new children and sets the success_threshold to 3.
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(TickCountingParallelDelAdd2, '2 4 True 3 False 5 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ TickCountingParallelDelAdd2'),
                                       call('on_init TickCountingParallelDelAdd2 success_threshold = 2'),  # noqa: E501
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/4'),
                                       call('TickCountingAction id = 2 tick: 1/3'),
                                       call('TickCountingAction id = 3 tick: 1/5'),
                                       call('TickCountingAction id = 1 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 2/3'),
                                       call('TickCountingAction id = 3 tick: 2/5'),
                                       call('TickCountingAction id = 1 tick: 3/4'),
                                       call('TickCountingAction id = 2 DONE with FAILURE'),
                                       call('on_abort TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 4'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 5'),
                                       call('TickCountingAction id = 1 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('TickCountingAction id = 4 tick: 1/3'),
                                       call('TickCountingAction id = 5 tick: 1/5'),
                                       call('TickCountingAction id = 4 tick: 2/3'),
                                       call('TickCountingAction id = 5 tick: 2/5'),
                                       call('TickCountingAction id = 4 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 4'),
                                       call('__del__ TickCountingAction id = 4'),
                                       call('TickCountingAction id = 5 tick: 3/5'),
                                       call('TickCountingAction id = 5 tick: 4/5'),
                                       call('TickCountingAction id = 5 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 5'),
                                       call('__del__ TickCountingAction id = 5'),
                                       call('on_delete TickCountingParallelDelAdd2'),
                                       call('__del__ TickCountingParallelDelAdd2')]

    ########################################################################

    def test_TickCountingParallelDel_threshold_3_fail_1(self):
        """Test the `TickCountingParallelDel` node.

        Test the `TickCountingParallelDel`. The success_threshold is set to 2. One of the
        children fails after 3 ticks. The contingengy-handler removed child #2 (id=3) and
        sets the success_threshold to 1.
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.DEBUG)
        bt_runner.run(TickCountingParallelDel, '2 4 True 3 False 5 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ TickCountingParallelDel'),
                                       call('on_init TickCountingParallelDel success_threshold = 2'),  # noqa: E501
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/4'),
                                       call('TickCountingAction id = 2 tick: 1/3'),
                                       call('TickCountingAction id = 3 tick: 1/5'),
                                       call('TickCountingAction id = 1 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 2/3'),
                                       call('TickCountingAction id = 3 tick: 2/5'),
                                       call('TickCountingAction id = 1 tick: 3/4'),
                                       call('TickCountingAction id = 2 DONE with FAILURE'),
                                       call('on_abort TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('TickCountingAction id = 1 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('on_delete TickCountingParallelDel'),
                                       call('__del__ TickCountingParallelDel')]

    ########################################################################

    def test_TickCountingParallelDelAllAdd_threshold_3_fail_1(self):
        """Test the `TickCountingParallelDelAllAdd` node.

        Test the `TickCountingParallelDelAllAdd`. The success_threshold is set to 2. One of the
        children fails after 3 ticks. The contingengy-handler removed child #2 (id=3), adds
        new new children and sets the success_threshold to 3.
        """
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(TickCountingParallelDelAllAdd, '2 4 True 3 False 5 True')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ TickCountingParallelDelAllAdd'),
                                       call('on_init TickCountingParallelDelAllAdd success_threshold = 2'),  # noqa: E501
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('TickCountingAction id = 1 tick: 1/4'),
                                       call('TickCountingAction id = 2 tick: 1/3'),
                                       call('TickCountingAction id = 3 tick: 1/5'),
                                       call('TickCountingAction id = 1 tick: 2/4'),
                                       call('TickCountingAction id = 2 tick: 2/3'),
                                       call('TickCountingAction id = 3 tick: 2/5'),
                                       call('TickCountingAction id = 1 tick: 3/4'),
                                       call('TickCountingAction id = 2 DONE with FAILURE'),
                                       call('on_abort TickCountingAction id = 1'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('on_abort TickCountingAction id = 2'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('on_abort TickCountingAction id = 3'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 4'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 5'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 6'),
                                       call('TickCountingAction id = 4 tick: 1/3'),
                                       call('TickCountingAction id = 5 tick: 1/5'),
                                       call('TickCountingAction id = 6 tick: 1/6'),
                                       call('TickCountingAction id = 4 tick: 2/3'),
                                       call('TickCountingAction id = 5 tick: 2/5'),
                                       call('TickCountingAction id = 6 tick: 2/6'),
                                       call('TickCountingAction id = 4 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 4'),
                                       call('__del__ TickCountingAction id = 4'),
                                       call('TickCountingAction id = 5 tick: 3/5'),
                                       call('TickCountingAction id = 6 tick: 3/6'),
                                       call('TickCountingAction id = 5 tick: 4/5'),
                                       call('TickCountingAction id = 6 tick: 4/6'),
                                       call('TickCountingAction id = 5 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 5'),
                                       call('__del__ TickCountingAction id = 5'),
                                       call('TickCountingAction id = 6 tick: 5/6'),
                                       call('TickCountingAction id = 6 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 6'),
                                       call('__del__ TickCountingAction id = 6'),
                                       call('on_delete TickCountingParallelDelAllAdd'),
                                       call('__del__ TickCountingParallelDelAllAdd')]

    ########################################################################

    def test_CountAbortParallel(self):
        """Test the CountAbortParallel."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.TRACE)
        bt_runner.run(CountAbortParallel)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'COUNTING_ERROR'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ CountAbortParallel'),
                                       call('on_init CountAbortParallel'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ FailOnCountAction'),
                                       call('on_init FailOnCountAction'),
                                       call('TickCountingAction id = 1 tick: 1/99'),
                                       call('FailOnCountAction tick: 2/5'),
                                       call('TickCountingAction id = 1 tick: 2/99'),
                                       call('FailOnCountAction tick: 3/5'),
                                       call('TickCountingAction id = 1 tick: 3/99'),
                                       call('FailOnCountAction tick: 4/5'),
                                       call('TickCountingAction id = 1 tick: 4/99'),
                                       call('FailOnCountAction DONE with FAILURE'),
                                       call('on_delete FailOnCountAction'),
                                       call('__del__ FailOnCountAction'),
                                       call('on_abort TickCountingAction id = 1'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('on_delete CountAbortParallel'),
                                       call('__del__ CountAbortParallel')]

    ########################################################################

    def test_CountAbortParallelWithTick(self):
        """Test the CountAbortParallelWithTick."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.TRACE)
        start = datetime.now()
        bt_runner.run(CountAbortParallelWithTick)
        end = datetime.now()
        delta = end - start
        assert int(delta.total_seconds() * 1000) > 600
        assert int(delta.total_seconds() * 1000) < 700
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.FAILURE
        assert bt_runner._instance.get_contingency_message() == 'COUNTING_ERROR'
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ CountAbortParallelWithTick'),
                                       call('on_init CountAbortParallelWithTick'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ FailOnCountAction'),
                                       call('on_init FailOnCountAction'),
                                       call('TickCountingAction id = 1 tick: 1/99'),
                                       call('FailOnCountAction tick: 2/5'),
                                       call('on_tick CountAbortParallelWithTick'),
                                       call('TickCountingAction id = 1 tick: 2/99'),
                                       call('FailOnCountAction tick: 3/5'),
                                       call('on_tick CountAbortParallelWithTick'),
                                       call('TickCountingAction id = 1 tick: 3/99'),
                                       call('FailOnCountAction tick: 4/5'),
                                       call('on_tick CountAbortParallelWithTick'),
                                       call('TickCountingAction id = 1 tick: 4/99'),
                                       call('FailOnCountAction DONE with FAILURE'),
                                       call('on_delete FailOnCountAction'),
                                       call('__del__ FailOnCountAction'),
                                       call('on_tick CountAbortParallelWithTick'),
                                       call('on_abort TickCountingAction id = 1'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('on_delete CountAbortParallelWithTick'),
                                       call('__del__ CountAbortParallelWithTick')]

    ########################################################################

    def test_ParallelRemoveSuccess(self):
        """Test the ParallelRemoveSuccess."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.get_logger().set_log_level(LogLevel.TRACE)
        bt_runner.run(ParallelRemoveSuccess)
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ ParallelRemoveSuccess'),
                                       call('on_init ParallelRemoveSuccess'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 1'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 2'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 3'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 4'),
                                       call('__init__ TickCountingAction'),
                                       call('on_init TickCountingAction id = 5'),
                                       call('TickCountingAction id = 1 tick: 1/2'),
                                       call('TickCountingAction id = 2 tick: 1/4'),
                                       call('TickCountingAction id = 3 tick: 1/6'),
                                       call('TickCountingAction id = 4 tick: 1/8'),
                                       call('TickCountingAction id = 5 tick: 1/99'),
                                       call('TickCountingAction id = 1 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 1'),
                                       call('__del__ TickCountingAction id = 1'),
                                       call('TickCountingAction id = 2 tick: 2/4'),
                                       call('TickCountingAction id = 3 tick: 2/6'),
                                       call('TickCountingAction id = 4 tick: 2/8'),
                                       call('TickCountingAction id = 5 tick: 2/99'),
                                       call('TickCountingAction id = 2 tick: 3/4'),
                                       call('TickCountingAction id = 3 tick: 3/6'),
                                       call('TickCountingAction id = 4 tick: 3/8'),
                                       call('TickCountingAction id = 5 tick: 3/99'),
                                       call('TickCountingAction id = 2 DONE with FAILURE'),
                                       call('on_delete TickCountingAction id = 2'),
                                       call('__del__ TickCountingAction id = 2'),
                                       call('TickCountingAction id = 3 tick: 4/6'),
                                       call('TickCountingAction id = 4 tick: 4/8'),
                                       call('TickCountingAction id = 5 tick: 4/99'),
                                       call('TickCountingAction id = 3 tick: 5/6'),
                                       call('TickCountingAction id = 4 tick: 5/8'),
                                       call('TickCountingAction id = 5 tick: 5/99'),
                                       call('TickCountingAction id = 3 DONE with SUCCESS'),
                                       call('on_delete TickCountingAction id = 3'),
                                       call('__del__ TickCountingAction id = 3'),
                                       call('TickCountingAction id = 4 tick: 6/8'),
                                       call('TickCountingAction id = 5 tick: 6/99'),
                                       call('on_abort TickCountingAction id = 4'),
                                       call('on_delete TickCountingAction id = 4'),
                                       call('__del__ TickCountingAction id = 4'),
                                       call('on_abort TickCountingAction id = 5'),
                                       call('on_delete TickCountingAction id = 5'),
                                       call('__del__ TickCountingAction id = 5'),
                                       call('on_delete ParallelRemoveSuccess'),
                                       call('__del__ ParallelRemoveSuccess')]

    ########################################################################

    def test_AsyncAddChildSequence(self):
        """Tests the AsyncAddChildSequence."""
        mock.reset_mock()
        bt_runner = BehaviorTreeRunner()
        bt_runner.run(AsyncAddChildParallel, '')
        assert mock.called
        assert bt_runner._instance.get_status() == NodeStatus.SUCCESS
        assert bt_runner._instance.get_contingency_message() == ''
        print(mock.call_args_list)
        assert mock.call_args_list == [call('__init__ AsyncAddChildParallel'),
                                       call('on_init AsyncAddChildParallel'),
                                       call('AsyncAddChildParallel: DONE'),
                                       call('__init__ HelloWorldAction'),
                                       call('__init__ HelloWorldAction'),
                                       call('HelloWorldAction: Hello World !!!'),
                                       call('__del__ HelloWorldAction'),
                                       call('HelloWorldAction: Hello World !!!'),
                                       call('__del__ HelloWorldAction')]
