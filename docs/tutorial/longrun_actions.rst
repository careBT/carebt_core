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
with a Python timer.

Create a multi-tick ActionNode
------------------------------

Create a file named ``longrun_actions.py`` with following content.
Or use the provided file: :download:`longrun_actions.py <../../carebt/examples/longrun_actions.py>`


.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 15-60
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``AddTwoNumbersMultiTickAction`` node is implemented as a Python class which inherits from ``ActionNode``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 21

The constructor (``__init__``) of the ``AddTwoNumbersMultiTickAction`` defines the signature that
the node has three input parameters (*?ticks ?x ?y*) and one output parameter (*?z*). The
input parameter *?ticks* is used to specify how many ticks the calculation should take. The remaining
parameters are the same as for the ``AddTwoNumbersAction``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 45-46

In the ``on_init`` function the internal *_tick_count* variable is initialized to one.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 48-49

In the ``on_tick`` function it is checked whether the internal *_tick_count* has reached the provided
*?tick* limit or not. In case the limit is reached the other two input parameters are added,
the result is bound to the output parameter and the node is set so ``SUCCESS``. In case the *_tick_count*
limit is not reached a message is printed on standard output. The node remains in status ``RUNNING`` and thus,
it is ticked again.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 51-60


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
    :lines: 65-116
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
    :lines: 90-96

The ``on_timeout`` function is called is case the specified timeout timer expires. In this example,
it is implemented that the current node is aborted and the contingency-message is set to 'TIMEOUT'.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 110-113

The ``on_abort`` function is called in case that the node is aborted. This function is the place
to do some cleanup which needs to be done in case the 'running' actions (resources) are aborted.
In this example only a message is printed on standard output.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 115-116


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
    :lines: 121-160
    :linenos:


The code explained
^^^^^^^^^^^^^^^^^^

In the ``on_init`` function the node status is set to ``SUSPENDED`` and a Python timer is implemented
to 'simulate' an asynchronous action. This timer is set to *?calctime* and the ``done_callback`` is
registered which is called as soon as the timer has expired.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 149-152

In the ``on_tick`` function a print statement is implemented to demonstrate that the ``on_tick`` function
is never called in this example as the node is directly set to ``SUSPENDED``. The ``on_tick`` function
could also be removed in this case!

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 154-155

In the ``done_callback`` the calculation is performed, the result is bound to the output parameter and
the status of the node is set to ``SUCCESS``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 157-160


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
