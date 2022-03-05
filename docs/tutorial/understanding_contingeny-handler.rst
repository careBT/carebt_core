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
    :lines: 15-79
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
    :lines: 61-67

In the ``on_tick`` function the result of the calculation is checked whether it is greater than ten. This is,
of course, just for demo purposes. In case **_z** is greater than ten the node fails and provides the
contingency-message 'RESULT_TOO_LARGE'.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 69-79

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``AddTwoNumbersActionWithFailures`` node.
The log-level is set to `INFO` to see some more details on the execution:

.. code-block:: python

    >>> import carebt
    >>> from carebt import LogLevel
    >>> from carebt.examples.sequence_with_contingencies import AddTwoNumbersActionWithFailures
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.get_logger().set_log_level(LogLevel.INFO)
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '3 5 => ?x')
    2022-03-05 17:09:01 INFO creating AddTwoNumbersActionWithFailures
    AddTwoNumbersActionWithFailures: calculating: 3 + 5 = 8
    2022-03-05 17:09:01 INFO ---------------------------------------------------
    2022-03-05 17:09:01 INFO bt execution finished
    2022-03-05 17:09:01 INFO status:  NodeStatus.SUCCESS
    2022-03-05 17:09:01 INFO contingency-message: 
    2022-03-05 17:09:01 INFO ---------------------------------------------------
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '3 => ?x')
    2022-03-05 17:11:53 INFO creating AddTwoNumbersActionWithFailures
    2022-03-05 17:11:53 WARN AddTwoNumbersActionWithFailures takes 2 argument(s), but 1 was/were provided
    2022-03-05 17:11:53 WARN ---------------------------------------------------
    2022-03-05 17:11:53 WARN bt execution finished
    2022-03-05 17:11:53 WARN status:  NodeStatus.FAILURE
    2022-03-05 17:11:53 WARN contingency-message: ONE_PARAM_MISSING
    2022-03-05 17:11:53 WARN ---------------------------------------------------
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '=> ?x')
    2022-03-05 17:12:35 INFO creating AddTwoNumbersActionWithFailures
    2022-03-05 17:12:35 WARN AddTwoNumbersActionWithFailures takes 2 argument(s), but 0 was/were provided
    2022-03-05 17:12:35 WARN ---------------------------------------------------
    2022-03-05 17:12:35 WARN bt execution finished
    2022-03-05 17:12:35 WARN status:  NodeStatus.FAILURE
    2022-03-05 17:12:35 WARN contingency-message: BOTH_PARAMS_MISSING
    2022-03-05 17:12:35 WARN ---------------------------------------------------
    >>> bt_runner.run(AddTwoNumbersActionWithFailures, '7 5 => ?x')
    2022-03-05 17:12:59 INFO creating AddTwoNumbersActionWithFailures
    AddTwoNumbersActionWithFailures: calculating: 7 + 5 = 12 -> RESULT_TOO_LARGE
    2022-03-05 17:12:59 WARN ---------------------------------------------------
    2022-03-05 17:12:59 WARN bt execution finished
    2022-03-05 17:12:59 WARN status:  NodeStatus.FAILURE
    2022-03-05 17:12:59 WARN contingency-message: RESULT_TOO_LARGE
    2022-03-05 17:12:59 WARN ---------------------------------------------------

Create a sequence without contingency-handling
----------------------------------------------

In this example the ``SimpleSequence`` node is implemented which has the two children ``AddTwoNumbersActionWithFailures``
and ``PrintNumberAction``. The ``AddTwoNumbersActionWithFailures`` is the one from above which can complete with failures.

Add the following content to ``sequence_with_contingencies.py``.
Or use the provided file: :download:`sequence_with_contingencies.py <../../carebt/examples/sequence_with_contingencies.py>`

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 84-112
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``SimpleSequence`` has two input parameters which are directly used as inputs for the
``AddTwoNumbersActionWithFailures``.

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleSequence`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt import LogLevel
    >>> from carebt.examples.sequence_with_contingencies import SimpleSequence
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.get_logger().set_log_level(LogLevel.INFO)
    >>> bt_runner.run(SimpleSequence, '2 5')
    2022-03-05 17:14:21 INFO creating AddTwoNumbersActionWithFailures
    AddTwoNumbersActionWithFailures: calculating: 2 + 5 = 7
    2022-03-05 17:14:21 INFO creating PrintNumberAction
    PrintNumberAction: number = 7
    2022-03-05 17:14:21 INFO finished SimpleSequence
    2022-03-05 17:14:21 INFO ---------------------------------------------------
    2022-03-05 17:14:21 INFO bt execution finished
    2022-03-05 17:14:21 INFO status:  NodeStatus.SUCCESS
    2022-03-05 17:14:21 INFO contingency-message: 
    2022-03-05 17:14:21 INFO ---------------------------------------------------
    >>> bt_runner.run(SimpleSequence, '2')
    2022-03-05 17:14:56 WARN SimpleSequence takes 2 argument(s), but 1 was/were provided
    2022-03-05 17:14:56 INFO creating AddTwoNumbersActionWithFailures
    2022-03-05 17:14:56 INFO finished SimpleSequence
    2022-03-05 17:14:56 WARN ---------------------------------------------------
    2022-03-05 17:14:56 WARN bt execution finished
    2022-03-05 17:14:56 WARN status:  NodeStatus.FAILURE
    2022-03-05 17:14:56 WARN contingency-message: ONE_PARAM_MISSING
    2022-03-05 17:14:56 WARN ---------------------------------------------------
    >>> bt_runner.run(SimpleSequence, '')
    2022-03-05 17:15:21 WARN SimpleSequence takes 2 argument(s), but 0 was/were provided
    2022-03-05 17:15:21 INFO creating AddTwoNumbersActionWithFailures
    2022-03-05 17:15:21 INFO finished SimpleSequence
    2022-03-05 17:15:21 WARN ---------------------------------------------------
    2022-03-05 17:15:21 WARN bt execution finished
    2022-03-05 17:15:21 WARN status:  NodeStatus.FAILURE
    2022-03-05 17:15:21 WARN contingency-message: BOTH_PARAMS_MISSING
    2022-03-05 17:15:21 WARN ---------------------------------------------------
    >>> bt_runner.run(SimpleSequence, '6 8')
    2022-03-05 17:15:43 INFO creating AddTwoNumbersActionWithFailures
    AddTwoNumbersActionWithFailures: calculating: 6 + 8 = 14 -> RESULT_TOO_LARGE
    2022-03-05 17:15:43 INFO finished SimpleSequence
    2022-03-05 17:15:43 WARN ---------------------------------------------------
    2022-03-05 17:15:43 WARN bt execution finished
    2022-03-05 17:15:43 WARN status:  NodeStatus.FAILURE
    2022-03-05 17:15:43 WARN contingency-message: RESULT_TOO_LARGE
    2022-03-05 17:15:43 WARN ---------------------------------------------------

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
    :lines: 117-181
    :linenos:


The code explained
^^^^^^^^^^^^^^^^^^

In the ``on_init`` function the two child nodes are added. Afterwards two contingency-handlers are registered. The
first one is attached to the ``AddTwoNumbersActionWithFailures`` child and triggers in case the child node completes
with ``FAILURE`` and with the contingency-message ``RESULT_TOO_LARGE``. In this case the ``fix_large_result``
function is called.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 151-154

The ``fix_large_result`` function removes all children from the sequence and adds the two new child nodes
``CreateRandomNumberAction`` and ``PrintNumberAction``.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 163-167

The second contingency-handler is also attached to the ``AddTwoNumbersActionWithFailures`` child and triggers 
in case the child node completes with ``FAILURE`` and the contingency-message matches the regular expression 
``r'.*_PARAM(S)?_MISSING'``. Thus, the ``fix_missing_input`` function is triggered for both contingency-messages
the ``AddTwoNumbersActionWithFailures`` node can provide. Alternatively the regular expression could be formulated,
for example, as follows: ``r'ONE_PARAM_MISSING|BOTH_PARAMS_MISSING'`` or ``r'.*_MISSING'``.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 156-161

The ``fix_missing_input`` function sets the output parameter ``_c`` resp. ``?c`` to zero and the currently
executing child - which is the ``AddTwoNumbersActionWithFailures`` - to ``FIXED``. As ``FIXED`` is handled
in the same way as ``SUCCESS`` the execution continues with the ``PrintNumberAction`` with input parameter
?c set to zero.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 169-172

The ``on_delete`` callback is called right after all child nodes have finished their execution. In this example,
it is checked whether a contingency-handler was executed. If that was the case the contingency-message is set
accordingly to indicate that to the parent node. Thus, the parent node will be able to analyse the contingency-message,
as well as the contingency-history to figure out how the task was completed with `SUCCESS`.

.. literalinclude:: ../../carebt/examples/sequence_with_contingencies.py
    :language: python
    :lines: 174-181


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``ContingencySequence`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt import LogLevel
    >>> from carebt.examples.sequence_with_contingencies import ContingencySequence
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.get_logger().set_log_level(LogLevel.INFO)
    >>> bt_runner.run(ContingencySequence, '6 4')
    2022-03-05 17:16:26 INFO creating AddTwoNumbersActionWithFailures
    AddTwoNumbersActionWithFailures: calculating: 6 + 4 = 10
    2022-03-05 17:16:26 INFO creating PrintNumberAction
    PrintNumberAction: number = 10
    2022-03-05 17:16:26 INFO finished ContingencySequence
    2022-03-05 17:16:26 INFO ---------------------------------------------------
    2022-03-05 17:16:26 INFO bt execution finished
    2022-03-05 17:16:26 INFO status:  NodeStatus.SUCCESS
    2022-03-05 17:16:26 INFO contingency-message: 
    2022-03-05 17:16:26 INFO ---------------------------------------------------
    >>> bt_runner.run(ContingencySequence, '6')
    2022-03-05 17:42:54 WARN ContingencySequence takes 2 argument(s), but 1 was/were provided
    2022-03-05 17:42:54 INFO creating AddTwoNumbersActionWithFailures
    fix_missing_input: set ?c = 0
    2022-03-05 17:42:54 INFO creating PrintNumberAction
    PrintNumberAction: number = 0
    2022-03-05 17:42:54 INFO finished ContingencySequence
    2022-03-05 17:42:54 INFO ---------------------------------------------------
    2022-03-05 17:42:54 INFO bt execution finished
    2022-03-05 17:42:54 INFO status:  NodeStatus.SUCCESS
    2022-03-05 17:42:54 INFO contingency-message: MISSING_PARAM_FIXED
    2022-03-05 17:42:54 INFO contingency-history: [0] AddTwoNumbersActionWithFailures
    2022-03-05 17:42:54 INFO                          NodeStatus.FAILURE
    2022-03-05 17:42:54 INFO                          ONE_PARAM_MISSING
    2022-03-05 17:42:54 INFO                          fix_missing_input
    2022-03-05 17:42:54 INFO ---------------------------------------------------
    >>> bt_runner.run(ContingencySequence, '')
    2022-03-05 17:43:23 WARN ContingencySequence takes 2 argument(s), but 0 was/were provided
    2022-03-05 17:43:23 INFO creating AddTwoNumbersActionWithFailures
    fix_missing_input: set ?c = 0
    2022-03-05 17:43:23 INFO creating PrintNumberAction
    PrintNumberAction: number = 0
    2022-03-05 17:43:23 INFO finished ContingencySequence
    2022-03-05 17:43:23 INFO ---------------------------------------------------
    2022-03-05 17:43:23 INFO bt execution finished
    2022-03-05 17:43:23 INFO status:  NodeStatus.SUCCESS
    2022-03-05 17:43:23 INFO contingency-message: MISSING_PARAM_FIXED
    2022-03-05 17:43:23 INFO contingency-history: [0] AddTwoNumbersActionWithFailures
    2022-03-05 17:43:23 INFO                          NodeStatus.FAILURE
    2022-03-05 17:43:23 INFO                          BOTH_PARAMS_MISSING
    2022-03-05 17:43:23 INFO                          fix_missing_input
    2022-03-05 17:43:23 INFO ---------------------------------------------------
    >>> bt_runner.run(ContingencySequence, '6 9')
    2022-03-05 17:43:48 INFO creating AddTwoNumbersActionWithFailures
    AddTwoNumbersActionWithFailures: calculating: 6 + 9 = 15 -> RESULT_TOO_LARGE
    fix_large_result
    2022-03-05 17:43:48 INFO creating CreateRandomNumberAction
    CreateRandomNumberAction: number = 5
    2022-03-05 17:43:48 INFO creating PrintNumberAction
    PrintNumberAction: number = 5
    2022-03-05 17:43:48 INFO finished ContingencySequence
    2022-03-05 17:43:48 INFO ---------------------------------------------------
    2022-03-05 17:43:48 INFO bt execution finished
    2022-03-05 17:43:48 INFO status:  NodeStatus.SUCCESS
    2022-03-05 17:43:48 INFO contingency-message: TOO_LARGE_RESULT_FIXED
    2022-03-05 17:43:48 INFO contingency-history: [0] AddTwoNumbersActionWithFailures
    2022-03-05 17:43:48 INFO                          NodeStatus.FAILURE
    2022-03-05 17:43:48 INFO                          RESULT_TOO_LARGE
    2022-03-05 17:43:48 INFO                          fix_large_result
    2022-03-05 17:43:48 INFO ---------------------------------------------------

Again, the first execution demonstrates the 'good' case where two input parameters with a sum smaller
than ten are provided. Thus, the ``AddTwoNumbersActionWithFailures`` completes with ``SUCCESS`` and the
``PrintNumberAction`` is executed. The next two execution show the cases where one or both input parameters
are missing. The ``fix_missing_input`` contingency-handler-function is executed which sets ``?c`` to zero
and fixes the ``AddTwoNumbersActionWithFailures``. Thus, the sequence execution conntinues with
``PrintNumberAction``. The next execution demonstrates the case when the sum of the two input parameters
is greater than ten. In this case the ``fix_large_result`` contingency-handler-function is executed which
removes all child nodes and add two new ones. The last three runs show, how the execution of the contingency
handlers is documented by the contingency-history. 
