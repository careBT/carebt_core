Writing long running ActionNodes
================================

Overview
--------

There are two different types of long running ``ActionNodes``. 

First, there are the ``ActionNodes`` that require more ticks to complete. In this case typically in the
``on_tick`` callback an action is triggered and/or the result is checked. But the execution time of one
tick of the ``on_tick`` function should be fast. Otherwise this affects the execution of the **careBT**
execution engine. Thus, this programming model should be used if an action needs to be triggered or a
check of a state needs to be executed periodically and the execution time is fast.

Second, there are the ``ActionNodes`` that need to call long running asynchronous actions. In this case
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
    :lines: 21-69
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
    :lines: 44-45

In the ``on_init`` function the internal *_tick_count* variable is initialized to one and a timeout
is specified for the node which expires after 500 ms. In case the timeout expires the ``on_timeout``
callback is called.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 47-49

In the ``on_tick`` function it is checked whether the internal *_tick_count* has reached the provided
*?tick* limit or not. In case the limit is reached the other two input parameters are added together,
the result is bound to the output parameter and the node is set so ``SUCCESS``. In case the *_tick_count*
limit is not reached a message is printed on standard output. The node remains in status ``RUNNING`` and thus,
it is ticked again.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 51-61

The ``on_timeout`` function is called is case the specified timeout timer expires. In this example
it is implemented that the current node is aborted and the contingency-message is set to 'TIMEOUT'.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 63-66

The ``on_abort`` function is called in case that the node is set to ``ABORT``. This is the place
to do some cleanup which needs to be done in case the 'running' action is aborted. In this example
only a message is printed on standard output.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 68-69


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersMultiTickAction`` node:

.. code-block:: python

    >>> from carebt.examples.longrun_actions import AddTwoNumbersMultiTickAction
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersMultiTickAction, '1 4 7 => ?result')
    AddTwoNumbersMultiTickAction: DONE 4 + 7 = 11
    >>> bt_runner.run(AddTwoNumbersMultiTickAction, '3 4 7 => ?result')
    AddTwoNumbersMultiTickAction: (tick_count = 1/3)
    AddTwoNumbersMultiTickAction: (tick_count = 2/3)
    AddTwoNumbersMultiTickAction: DONE 4 + 7 = 11
    >>> bt_runner.run(AddTwoNumbersMultiTickAction, '15 4 7 => ?result')
    AddTwoNumbersMultiTickAction: (tick_count = 1/15)
    AddTwoNumbersMultiTickAction: (tick_count = 2/15)
    AddTwoNumbersMultiTickAction: (tick_count = 3/15)
    AddTwoNumbersMultiTickAction: (tick_count = 4/15)
    AddTwoNumbersMultiTickAction: (tick_count = 5/15)
    AddTwoNumbersMultiTickAction: (tick_count = 6/15)
    AddTwoNumbersMultiTickAction: (tick_count = 7/15)
    AddTwoNumbersMultiTickAction: (tick_count = 8/15)
    AddTwoNumbersMultiTickAction: (tick_count = 9/15)
    AddTwoNumbersMultiTickAction: (tick_count = 10/15)
    AddTwoNumbersMultiTickAction: on_timeout
    AddTwoNumbersMultiTickAction: on_abort
    2021-11-28 21:55:37 WARN ---------------------------------------------------
    2021-11-28 21:55:37 WARN bt execution finished
    2021-11-28 21:55:37 WARN status:  NodeStatus.ABORTED
    2021-11-28 21:55:37 WARN message: TIMEOUT
    2021-11-28 21:55:37 WARN ---------------------------------------------------


Create an asynchronous ActionNode
---------------------------------

Add the following content to ``longrun_actions.py``.
Or use the provided file: :download:`longrun_actions.py <../../carebt/examples/longrun_actions.py>`

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 74-114
    :linenos:


The code explained
^^^^^^^^^^^^^^^^^^

In the ``on_init`` function the node status is set to ``SUSPENDED`` and a Python timer is implemented
to 'simulate' an asynchronous action. This timer is set to *?calctime* and the ``done_callback`` is
registerd which is called as soon as the timer has expired.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 101-105

In the ``on_tick`` function a print statement is implemented to demonstrate that the ``on_tick`` function
is never called in this example as the node is directly set to ``SUSPENDED``. The ``on_tick`` function
could also be removed in this case!

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 107-108

In the ``done_callback`` the calculation is performed, the result is bound to the output parameter and
the status of the node is set to ``SUCCESS``.

.. literalinclude:: ../../carebt/examples/longrun_actions.py
    :language: python
    :lines: 110-114


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersLongRunnungAction`` node:

.. code-block:: python

    >>> from carebt.examples.longrun_actions import AddTwoNumbersLongRunnungAction
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersLongRunnungAction, '2000 4 7 => ?result')
    AddTwoNumbersLongRunnungAction: calculating 2000 ms ...
    AddTwoNumbersLongRunnungAction: DONE 4 + 7 = 11
