Understanding contingency-handlers
==================================

Overview
--------

This tutorial demonstrates how ``contingency-handlers`` can be used to 'react' to failures
which occur during execution. In the following examples custom ``SequenceNodes`` are used.


Create an ActionNode with failures
----------------------------------

Create a file named ``sequence_with_contingencies.py`` with following content.
Or use the provided file: :download:`sequence_with_contingencies.py <../../carebt/examples/sequence_with_contingencies.py>`

First of all, an ``ActionNode`` which 'can' fail is required. Therefore, the
``AddTwoNumbersAction`` is extended that it can complete with ``FAILURE``. This
extended node is called ``AddTwoNumbersActionWithFailures``. It is implemented that
a failure can be provoked in case that one or both input parameters are missing or
in case the result of the sum of the two parameters is greater than ten. These are,
of course, just some 'artificial' failures to beeing able to demonstrate the technics
of contingency-handlers.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 22-78
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``AddTwoNumbersAction`` was already introduced in :doc:`Writing a node with parameters <action_with_params>` and is
now extended to provide some failures. This extended node is called ``AddTwoNumbersActionWithFailures``.

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

Start the Python interpreter and run the ``AddTwoNumbersActionWithFailures`` node:

.. code-block:: python

    >>> from carebt.examples.sequence_with_contingencies import *
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '3 5 => ?x')
    AddTwoNumbersActionWithFailures: calculating: 3 + 5 = 8
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '3 => ?x')
    2021-11-25 21:50:54 WARN AddTwoNumbersActionWithFailures takes 2 argument(s), but 1 was/were provided
    2021-11-25 21:50:54 WARN ---------------------------------------------------
    2021-11-25 21:50:54 WARN bt execution finished
    2021-11-25 21:50:54 WARN status:  NodeStatus.FAILURE
    2021-11-25 21:50:54 WARN message: ONE_PARAM_MISSING
    2021-11-25 21:50:54 WARN ---------------------------------------------------
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '=> ?x')
    2021-11-25 21:51:03 WARN AddTwoNumbersActionWithFailures takes 2 argument(s), but 0 was/were provided
    2021-11-25 21:51:03 WARN ---------------------------------------------------
    2021-11-25 21:51:03 WARN bt execution finished
    2021-11-25 21:51:03 WARN status:  NodeStatus.FAILURE
    2021-11-25 21:51:03 WARN message: BOTH_PARAMS_MISSING
    2021-11-25 21:51:03 WARN ---------------------------------------------------
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '7 5 => ?x')
    AddTwoNumbersActionWithFailures: calculating: 7 + 5 = 12 -> RESULT_TOO_LARGE
    2021-11-25 21:51:10 WARN ---------------------------------------------------
    2021-11-25 21:51:10 WARN bt execution finished
    2021-11-25 21:51:10 WARN status:  NodeStatus.FAILURE
    2021-11-25 21:51:10 WARN message: RESULT_TOO_LARGE
    2021-11-25 21:51:10 WARN ---------------------------------------------------

Create a sequence without contingency-handling
----------------------------------------------

In this example the ``SimpleSequence`` node is implemented which has the two children ``AddTwoNumbersActionWithFailures``
and ``PrintNumberAction``. The ``AddTwoNumbersActionWithFailures`` is the one from above which can complete with failures.

Add the following content to ``sequence_with_contingencies.py``.
Or use the provided file: :download:`sequence_with_contingencies.py <../../carebt/examples/sequence_with_contingencies.py>`

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 83-111
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``SimpleSequence`` has two input parameters which are directly used as inputs for the
``AddTwoNumbersActionWithFailures``.

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleSequence`` node:

.. code-block:: python

    >>> from carebt.examples.sequence_with_contingencies import *
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(SimpleSequence, '2 5')
    AddTwoNumbersActionWithFailures: calculating: 2 + 5 = 7
    PrintNumberAction: number = 7
    >>> bt_runner.run(SimpleSequence, '2')
    2021-11-26 21:55:03 WARN SimpleSequence takes 2 argument(s), but 1 was/were provided
    2021-11-26 21:55:03 WARN ---------------------------------------------------
    2021-11-26 21:55:03 WARN bt execution finished
    2021-11-26 21:55:03 WARN status:  NodeStatus.FAILURE
    2021-11-26 21:55:03 WARN message: ONE_PARAM_MISSING
    2021-11-26 21:55:03 WARN ---------------------------------------------------
    >>> bt_runner.run(SimpleSequence, '')
    2021-11-26 21:55:11 WARN SimpleSequence takes 2 argument(s), but 0 was/were provided
    2021-11-26 21:55:11 WARN ---------------------------------------------------
    2021-11-26 21:55:11 WARN bt execution finished
    2021-11-26 21:55:11 WARN status:  NodeStatus.FAILURE
    2021-11-26 21:55:11 WARN message: BOTH_PARAMS_MISSING
    2021-11-26 21:55:11 WARN ---------------------------------------------------
    >>> bt_runner.run(SimpleSequence, '6 8')
    AddTwoNumbersActionWithFailures: calculating: 6 + 8 = 14 -> RESULT_TOO_LARGE
    2021-11-26 21:55:17 WARN ---------------------------------------------------
    2021-11-26 21:55:17 WARN bt execution finished
    2021-11-26 21:55:17 WARN status:  NodeStatus.FAILURE
    2021-11-26 21:55:17 WARN message: RESULT_TOO_LARGE
    2021-11-26 21:55:17 WARN ---------------------------------------------------

The first execution shows the standard case where two input parameters are provided which have a sum
smaller than ten. As in this case the ``AddTwoNumbersActionWithFailures`` node completes with
``SUCCESS`` the ``PrintNumberAction`` is also executed. The subsequent three executions have in common,
that the ``AddTwoNumbersActionWithFailures`` completes with ``FAILURE``, and thus the sequence directly completes
also with ``FAILURE`` - without executing the ``PrintNumberAction`` node. The only difference is that
the contingency-message differs in the three cases.


Create a sequence with contingency-handling
-------------------------------------------

In this example the ``SimpleSequence`` node is extended by two contingency-handlers. The new sequence
is called ``ContingencySequence``.

Add the following content to ``sequence_with_contingencies.py``.
Or use the provided file: :download:`sequence_with_contingencies.py <../../carebt/examples/sequence_with_contingencies.py>`

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 116-171
    :linenos:


The code explained
^^^^^^^^^^^^^^^^^^

In the ``on_init`` function the two child nodes are added. Afterwards two contingency-handlers are registered. The
first one is attached to the ``AddTwoNumbersActionWithFailures`` child and triggers in case the child node completes
with ``FAILURE`` and with the contingency-message ``RESULT_TOO_LARGE``. In this case the ``fix_large_result``
function is called.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 150-153

The ``fix_large_result`` function removes all children from the sequence and adds the two new child nodes
``CreateRandomNumberAction`` and ``PrintNumberAction``.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 162-166

The second contingency-handler is also attached to the ``AddTwoNumbersActionWithFailures`` child and triggers 
in case the child node completes with ``FAILURE`` and the contingency-message matches the regular expression 
``r'.*_PARAM(S)?_MISSING'``. Thus, the ``fix_missing_input`` function is triggered for both contingency-messages
the ``AddTwoNumbersActionWithFailures`` node can provide. Alternatively the regular expression could be formulated,
for example, as follows: ``r'ONE_PARAM_MISSING|BOTH_PARAMS_MISSING'`` or ``r'.*_MISSING'``.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 155-160

The ``fix_missing_input`` function sets the output parameter ``_c`` resp. ``?c`` to zero and the currently
executing child - which is the ``AddTwoNumbersActionWithFailures`` - to ``FIXED``. As ``FIXED`` is handled
in the same way as ``SUCCESS`` the execution continues with the ``PrintNumberAction`` with input parameter
?c set to zero.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 168-171


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``ContingencySequence`` node:

.. code-block:: python

    >>> from carebt.examples.sequence_with_contingencies import *
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(ContingencySequence, '6 4')
    AddTwoNumbersActionWithFailures: calculating: 6 + 4 = 10
    PrintNumberAction: number = 10
    >>> bt_runner.run(ContingencySequence, '6')
    2021-11-26 22:41:59 WARN ContingencySequence takes 2 argument(s), but 1 was/were provided
    fix_missing_input: set ?c = 0
    PrintNumberAction: number = 0
    >>> bt_runner.run(ContingencySequence, '')
    2021-11-26 22:42:07 WARN ContingencySequence takes 2 argument(s), but 0 was/were provided
    fix_missing_input: set ?c = 0
    PrintNumberAction: number = 0
    >>> bt_runner.run(ContingencySequence, '6 9')
    AddTwoNumbersActionWithFailures: calculating: 6 + 9 = 15 -> RESULT_TOO_LARGE
    fix_large_result
    CreateRandomNumberAction: number = 1
    PrintNumberAction: number = 1

Again, the first execution demonstrates the 'good' case where two input parameters with a sum smaller
than ten are provided. Thus, the ``AddTwoNumbersActionWithFailures`` completes with ``SUCCESS`` and the
``PrintNumberAction`` is executed. The next two execution show the cases where one or both input parameters
are missing. The ``fix_missing_input`` contingency-handler-function is executed which sets ``?c`` to zero
and fixes the ``AddTwoNumbersActionWithFailures``. Thus, the sequence execution conntinues with
``PrintNumberAction``. The next execution demonstrates the case when the sum of the two input parameters
is greater than ten. In this case the ``fix_large_result`` contingency-handler-function is executed which
removes all child nodes and add two new ones.
