Writing a FallbackNode
======================

Overview
--------

This tutorial demonstrates the **careBT** ``FallbackNode``. Therefore the ``SimpleFallback`` node
is implemented which has three child nodes of the same type (``AddTwoNumbersActionWithFailures``).
By 'playing around' with the input parameters, the 'RESULT_TOO_LARGE' contingency can be provoked
in each of the three children. This allows to observe the functionality of the ``FallbackNode``.


Create the SimpleFallback node
------------------------------

Create a file named ``fallback.py`` with following content.
Or use the provided file: :download:`fallback.py <../../carebt/examples/fallback.py>`


.. literalinclude:: ../../carebt/examples/fallback.py
    :language: python
    :lines: 15-
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``AddTwoNumbersActionWithFailures`` node was already introduced in 
:doc:`Understanding contingency-handlers <understanding_contingeny-handler>` and is just reused
in this example.

The constructor (``__init__``) of the ``SimpleFallback`` needs to call the constructor (``super().__init__``)
of the ``FallbackNode`` and passes the bt_runner and the signature as arguments. The signature defines three
input parameter called *?b1 ?b2 ?b3*.

.. literalinclude:: ../../carebt/examples/fallback.py
    :language: python
    :lines: 41-42

In the ``on_init`` function the three child nodes are added.

.. literalinclude:: ../../carebt/examples/fallback.py
    :language: python
    :lines: 44-47


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleFallback`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.fallback import SimpleFallback
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(SimpleFallback, '1 2 3')
    AddTwoNumbersActionWithFailures: calculating: 1 + 1 = 2
    >>> bt_runner.run(SimpleFallback, '10 2 3')
    AddTwoNumbersActionWithFailures: calculating: 1 + 10 = 11 -> RESULT_TOO_LARGE
    AddTwoNumbersActionWithFailures: calculating: 2 + 2 = 4
    >>> bt_runner.run(SimpleFallback, '10 20 3')
    AddTwoNumbersActionWithFailures: calculating: 1 + 10 = 11 -> RESULT_TOO_LARGE
    AddTwoNumbersActionWithFailures: calculating: 2 + 20 = 22 -> RESULT_TOO_LARGE
    AddTwoNumbersActionWithFailures: calculating: 3 + 3 = 6
    >>> bt_runner.run(SimpleFallback, '10 20 30')
    AddTwoNumbersActionWithFailures: calculating: 1 + 10 = 11 -> RESULT_TOO_LARGE
    AddTwoNumbersActionWithFailures: calculating: 2 + 20 = 22 -> RESULT_TOO_LARGE
    AddTwoNumbersActionWithFailures: calculating: 3 + 30 = 33 -> RESULT_TOO_LARGE
    2021-11-30 20:55:46 WARN ---------------------------------------------------
    2021-11-30 20:55:46 WARN bt execution finished
    2021-11-30 20:55:46 WARN status:  NodeStatus.FAILURE
    2021-11-30 20:55:46 WARN contingency-message: RESULT_TOO_LARGE
    2021-11-30 20:55:46 WARN ---------------------------------------------------

In the first execution of the ``SimpleFallback`` node the first child already completes
with ``SUCCESS`` and thus the whole ``SimpleFallback`` node completes with ``SUCCESS``. In the
second execution the first child fails (with ``RESULT_TOO_LARGE``) and thus the second one
is executed, which succeeds. Thus also the whole ``SimpleFallback`` node completes with ``SUCCESS``.
In the third execution all three children fail and as a consequence the whole ``SimpleFallback``
node fails with the contingency-message ``RESULT_TOO_LARGE``.
