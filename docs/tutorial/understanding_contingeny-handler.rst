Understanding contingency-handlers
==================================

Overview
--------

This tutorial demonstrates how ``contingency-handlers`` can be used to 'react' to failures
which occur during execution of a sequence node.


Create an ActionNode with failures
----------------------------------

Create a file named ``sequence_with_contingencies.py`` with following content.
Or use the provided file: :download:`sequence_with_contingencies.py <../../carebt/examples/sequence_with_contingencies.py>`

First of all, an ``ActionNode`` which 'can' fail is required. Therefore, the ``AddTwoNumbersAction``
is extended that it can complete with ``FAILURE``. This happend in case that one or both input
parameters are missing or that the result of the sum is greater than ten. These are just some
'artificial' failures to beeing able to demonstrate the technics of contingency-handlers.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 23-78
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``AddTwoNumbersAction`` was introduced in :doc:`Writing a node with parameters <action_with_params>` and is
extended to provide some failures.

In the ``on_init`` function two different contingency situations are implemented. The first one
if both input parameters are missing. In this case the node completes with ``FAILURE`` and provides
the contingency-message 'BOTH_PARAMS_MISSING'. And the second one if one input parameter is missing.
In this case the node completes with ``FAILURE`` and provides the contingency-message 'ONE_PARAM_MISSING'.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 60-66

In the ``on_tick`` function the result of the calculation is checked whether it is greater than ten. This is,
of course, just for demo purposes. In case **_z** is greater than ten the node fails and provides the
contingency-message 'RESULT_TOO_LARGE'.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 68-78

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersAction`` node:

.. code-block:: python

    >>> from carebt.examples.sequence_with_contingencies import *
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersAction, '3 5 => ?x')
    AddTwoNumbersAction: calculating: 3 + 5 = 8
    >>> bt_runner.run(AddTwoNumbersAction, '3 => ?x')
    2021-11-25 17:50:54 WARN AddTwoNumbersAction takes 2 argument(s), but 1 was/were provided
    2021-11-25 17:50:54 WARN ---------------------------------------------------
    2021-11-25 17:50:54 WARN bt execution finished
    2021-11-25 17:50:54 WARN status:  NodeStatus.FAILURE
    2021-11-25 17:50:54 WARN message: ONE_PARAM_MISSING
    2021-11-25 17:50:54 WARN ---------------------------------------------------
    >>> bt_runner.run(AddTwoNumbersAction, '=> ?x')
    2021-11-25 17:51:03 WARN AddTwoNumbersAction takes 2 argument(s), but 0 was/were provided
    2021-11-25 17:51:03 WARN ---------------------------------------------------
    2021-11-25 17:51:03 WARN bt execution finished
    2021-11-25 17:51:03 WARN status:  NodeStatus.FAILURE
    2021-11-25 17:51:03 WARN message: BOTH_PARAMS_MISSING
    2021-11-25 17:51:03 WARN ---------------------------------------------------
    >>> bt_runner.run(AddTwoNumbersAction, '7 5 => ?x')
    AddTwoNumbersAction: calculating: 7 + 5 = 12 -> RESULT_TOO_LARGE
    2021-11-25 17:51:10 WARN ---------------------------------------------------
    2021-11-25 17:51:10 WARN bt execution finished
    2021-11-25 17:51:10 WARN status:  NodeStatus.FAILURE
    2021-11-25 17:51:10 WARN message: RESULT_TOO_LARGE
    2021-11-25 17:51:10 WARN ---------------------------------------------------
