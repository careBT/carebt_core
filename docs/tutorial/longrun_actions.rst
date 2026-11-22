Writing long running ActionNodes
================================

Overview
--------

There are two different types of long running ``ActionNodes``. 

First, there are the ``ActionNodes`` that require more ticks to complete. In this case typically in the
``on_tick`` callback a function (action) is triggered and/or a status in the 'world' is checked.
However, the execution time of one tick of the ``on_tick`` function has to be fast. Otherwise this affects the
execution of the **careBT** execution engine. Thus, this programming model should be used if a function
needs to be triggered or a check of a state needs to be executed periodically and the execution
time is fast.

Second, there are the ``ActionNodes`` that need to call long running asynchronous functions (actions). In this case
the node is put into the ``SUSPENDED`` state to suppress further calls of the ``on_tick`` callback. When
initiating the asynchronous action a 'result' callback should be registered that can then take over and
change the state of the node accordingly. In the following example this asynchronous action is 'simulated'
with a careBT timer. A further example shows an asynchronous action which reports its result in another thread.

.. note::

    The **careBT** execution engine is single-threaded. All callbacks (``on_tick``, ``on_timeout``,
    contingency-handlers, timer callbacks, ...) are executed in the thread which ticks the behavior tree.
    Thus, the state of a node must never be changed from another thread. ``set_status`` and
    ``set_contingency_message`` raise a ``RuntimeError`` if they are called from another thread than the
    one which ticks the behavior tree. This can be relaxed with
    ``bt_runner.set_strict_thread_safety(False)``; then only a warning is logged and the state is changed anyway.
    To hand over a result from another thread use ``create_timer(0, ...)``.
    When the behavior tree is integrated into another event loop (e.g. ROS 2) with ``initialize`` and ``tick``,
    all callbacks of that event loop should be executed in the same thread which ticks the behavior tree.

Create a multi-tick ActionNode
------------------------------

Create a file named ``longrun_actions.py`` with following content.
Or use the provided file: :download:`longrun_actions.py <../../carebt/examples/longrun_actions.py>`


.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 18-61
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``AddTwoNumbersMultiTickAction`` node is implemented as a Python class which inherits from ``ActionNode``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 22

The constructor (``__init__``) of the ``AddTwoNumbersMultiTickAction`` defines the signature that
the node has three input parameters (*?ticks ?x ?y*) and one output parameter (*?z*). The
input parameter *?ticks* is used to specify how many ticks the calculation should take. The remaining
parameters are the same as for the ``AddTwoNumbersAction``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 46-47

In the ``on_init`` function the internal *_tick_count* variable is initialized to one.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 49-50

In the ``on_tick`` function it is checked whether the internal *_tick_count* has reached the provided
*?tick* limit or not. In case the limit is reached the other two input parameters are added,
the result is bound to the output parameter and the node is set so ``SUCCESS``. In case the *_tick_count*
limit is not reached a message is printed on standard output. The node remains in status ``RUNNING`` and thus,
it is ticked again.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 52-61


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersMultiTickAction`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.longrun_actions import AddTwoNumbersMultiTickAction
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersMultiTickAction, '1 4 7 => ?result')
    AddTwoNumbersMultiTickAction: DONE 4 + 7 = 11
    >>> bt_runner.run(AddTwoNumbersMultiTickAction, '5 4 7 => ?result')
    AddTwoNumbersMultiTickAction: (tick_count = 1/5)
    AddTwoNumbersMultiTickAction: (tick_count = 2/5)
    AddTwoNumbersMultiTickAction: (tick_count = 3/5)
    AddTwoNumbersMultiTickAction: (tick_count = 4/5)
    AddTwoNumbersMultiTickAction: DONE 4 + 7 = 11
    >>> bt_runner.run(AddTwoNumbersMultiTickAction, '9 4 7 => ?result')
    AddTwoNumbersMultiTickAction: (tick_count = 1/9)
    AddTwoNumbersMultiTickAction: (tick_count = 2/9)
    AddTwoNumbersMultiTickAction: (tick_count = 3/9)
    AddTwoNumbersMultiTickAction: (tick_count = 4/9)
    AddTwoNumbersMultiTickAction: (tick_count = 5/9)
    AddTwoNumbersMultiTickAction: (tick_count = 6/9)
    AddTwoNumbersMultiTickAction: (tick_count = 7/9)
    AddTwoNumbersMultiTickAction: (tick_count = 8/9)
    AddTwoNumbersMultiTickAction: DONE 4 + 7 = 11


Create a multi-tick ActionNode with timeout
-------------------------------------------

Add the following content to ``longrun_actions.py``.
Or use the provided file: :download:`longrun_actions.py <../../carebt/examples/longrun_actions.py>`


.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 66-117
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``AddTwoNumbersMultiTickActionWithTimeout`` introduces a timeout and throttling to
the ``AddTwoNumbersMultiTickAction``.

In the ``on_init`` function the internal *_tick_count* variable is initialized to one and a timeout
is specified for the node which expires after 500 ms. In case the timeout expires the ``on_timeout``
callback is called. In the second variant (which is commented out) throttling is set to 1000 ms.
This ensures that the ticks of the node are omitted and not forwarded until 1000 ms have passed. Thus,
the ``on_tick`` function is called each 1000ms. Furthermore the timeout is set to 5000 ms, that the
timeout is greater than the throttling.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 91-97

The ``on_timeout`` function is called is case the specified timeout timer expires. In this example,
it is implemented that the current node is aborted and the contingency-message is set to 'TIMEOUT'.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 111-114

The ``on_abort`` function is called in case that the node is aborted. This function is the place
to do some cleanup which needs to be done in case the 'running' actions (resources) are aborted.
In this example only a message is printed on standard output.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 116-117


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersMultiTickAction`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.longrun_actions import AddTwoNumbersMultiTickActionWithTimeout
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersMultiTickActionWithTimeout, '1 4 7 => ?result')
    AddTwoNumbersMultiTickActionWithTimeout: DONE 4 + 7 = 11
    >>> bt_runner.run(AddTwoNumbersMultiTickActionWithTimeout, '3 4 7 => ?result')
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 1/3)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 2/3)
    AddTwoNumbersMultiTickActionWithTimeout: DONE 4 + 7 = 11
    >>> bt_runner.run(AddTwoNumbersMultiTickActionWithTimeout, '15 4 7 => ?result')
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 1/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 2/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 3/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 4/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 5/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 6/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 7/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 8/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 9/15)
    AddTwoNumbersMultiTickActionWithTimeout: (tick_count = 10/15)
    AddTwoNumbersMultiTickActionWithTimeout: on_timeout
    AddTwoNumbersMultiTickActionWithTimeout: on_abort
    2021-12-01 20:29:17 WARN ---------------------------------------------------
    2021-12-01 20:29:17 WARN bt execution finished
    2021-12-01 20:29:17 WARN status:  NodeStatus.ABORTED
    2021-12-01 20:29:17 WARN contingency-message: TIMEOUT
    2021-12-01 20:29:17 WARN ---------------------------------------------------

.. hint::

    Change the comments to enable throttling and increase the timeout to 5000 ms to also
    test this feature.


Create an asynchronous ActionNode
---------------------------------

Add the following content to ``longrun_actions.py``.
Or use the provided file: :download:`longrun_actions.py <../../carebt/examples/longrun_actions.py>`

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 122-161
    :linenos:


The code explained
^^^^^^^^^^^^^^^^^^

In the ``on_init`` function the node status is set to ``SUSPENDED`` and a careBT timer is created with
``create_timer`` to 'simulate' an asynchronous action. This timer is set to *?calctime* and the ``done_callback`` is
registered which is called as soon as the timer has expired.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 150-153

In the ``on_tick`` function a print statement is implemented to demonstrate that the ``on_tick`` function
is never called in this example as the node is directly set to ``SUSPENDED``. The ``on_tick`` function
could also be removed in this case!

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 155-156

In the ``done_callback`` the calculation is performed, the result is bound to the output parameter and
the status of the node is set to ``SUCCESS``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 158-161


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersLongRunningAction`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.longrun_actions import AddTwoNumbersLongRunningAction
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersLongRunningAction, '2000 4 7 => ?result')
    AddTwoNumbersLongRunningAction: calculating 2000 ms ...
    AddTwoNumbersLongRunningAction: DONE 4 + 7 = 11


Create an asynchronous ActionNode with a thread
-----------------------------------------------

Real asynchronous functions often report their result in another thread. In the following example such a
function is 'simulated' with a Python thread which sleeps for one second. With the input parameter *?success*
it can be selected whether the function succeeds or fails.

Add the following content to ``longrun_actions.py``.
Or use the provided file: :download:`longrun_actions.py <../../carebt/examples/longrun_actions.py>`

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 15-16

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 166-226
    :linenos:


The code explained
^^^^^^^^^^^^^^^^^^

The constructor (``__init__``) of the ``AddTwoNumbersLongRunningActionWithThread`` defines the signature that
the node has three input parameters (*?success ?x ?y*) and one output parameter (*?z*). If *?success* is ``True``
the asynchronous function succeeds, otherwise it fails.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 200-201

In the ``on_init`` function the node status is set to ``SUSPENDED`` and a Python thread is started which
executes the ``calculate`` function.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 203-206

The ``calculate`` function is executed in the thread. As the state of a node must never be changed from
another thread, it does not set the status of the node. Instead, it creates a careBT timer with a delay
of 0 ms. ``create_timer`` can be called from another thread, and the timer callback is executed in the
thread which ticks the behavior tree, right before the next tick. In case of success, the result is
passed to the ``done_callback``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 208-215

In the ``done_callback`` the result is bound to the output parameter and the status of the node is set
to ``SUCCESS``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 217-221

In the ``failure_callback`` the status of the node is set to ``FAILURE`` and the contingency-message is
set to ``CALCULATION_FAILED``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 223-226

.. note::

    In case the node is aborted or deleted (e.g. due to a timeout of a parent node) before the thread
    reports its result, the timer callback is not executed.


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersLongRunningActionWithThread`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.longrun_actions import AddTwoNumbersLongRunningActionWithThread
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersLongRunningActionWithThread, 'True 4 7 => ?result')
    AddTwoNumbersLongRunningActionWithThread: calculating 1000 ms ...
    AddTwoNumbersLongRunningActionWithThread: DONE 4 + 7 = 11
    >>> bt_runner.run(AddTwoNumbersLongRunningActionWithThread, 'False 4 7 => ?result')
    AddTwoNumbersLongRunningActionWithThread: calculating 1000 ms ...
    AddTwoNumbersLongRunningActionWithThread: FAILED
    2026-10-22 06:57:51 WARN ---------------------------------------------------
    2026-10-22 06:57:51 WARN bt execution finished
    2026-10-22 06:57:51 WARN status:  NodeStatus.FAILURE
    2026-10-22 06:57:51 WARN contingency-message: CALCULATION_FAILED
    2026-10-22 06:57:51 WARN ---------------------------------------------------
