Writing a ParallelNode
======================

Overview
--------

This tutorial demonstrates the **careBT** ``ParallelNode``. Therefore the ``SimpleParallel`` node
is implemented which has three child nodes of the same type (``AddTwoNumbersMultiTickAction``). With
the input parameters, the amount of ticks can be specified that the children take to complete. As the
``success_threshold`` is set to two, the ``SimpleParallel`` node succeeds in case that two nodes complete
with ``SUCCESS`` or ``FIXED``, or fails in case one child node completes with ``FAILURE`` or
``ABORTED``. By 'playing around' with the input parameters different situation can be provoked.


Create the SimpleParallel node
------------------------------

Create a file named ``parallel.py`` with following content.
Or use the provided file: :download:`parallel.py <../../carebt/examples/parallel.py>`


.. literalinclude:: ../../carebt/examples/parallel.py
    :language: python
    :lines: 15-
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The ``AddTwoNumbersMultiTickAction`` node was already introduced in 
:doc:`Writing long running ActionNodes <longrun_actions>` and is just reused
in this example.

The constructor (``__init__``) of the ``SimpleParallel`` needs to call the constructor (``super().__init__``)
of the ``ParallelNode`` and passes the bt_runner, the success_threshold and the signature as arguments. The
success_threshold is set to two, and the signature defines three input parameter.

.. literalinclude:: ../../carebt/examples/parallel.py
    :language: python
    :lines: 41-42

In the ``on_init`` function the three child nodes are added.

.. literalinclude:: ../../carebt/examples/parallel.py
    :language: python
    :lines: 44-47


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleParallel`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.parallel import SimpleParallel
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(SimpleParallel, '2 4 6')
    AddTwoNumbersMultiTickAction: (tick_count = 1/2)
    AddTwoNumbersMultiTickAction: (tick_count = 1/4)
    AddTwoNumbersMultiTickAction: (tick_count = 1/6)
    AddTwoNumbersMultiTickAction: DONE 1 + 1 = 2
    AddTwoNumbersMultiTickAction: (tick_count = 2/4)
    AddTwoNumbersMultiTickAction: (tick_count = 2/6)
    AddTwoNumbersMultiTickAction: (tick_count = 3/4)
    AddTwoNumbersMultiTickAction: (tick_count = 3/6)
    AddTwoNumbersMultiTickAction: DONE 2 + 2 = 4
    AddTwoNumbersMultiTickAction: (tick_count = 4/6)
    AddTwoNumbersMultiTickAction: on_abort
    >>> bt_runner.run(SimpleParallel, '6 4 2')
    AddTwoNumbersMultiTickAction: (tick_count = 1/6)
    AddTwoNumbersMultiTickAction: (tick_count = 1/4)
    AddTwoNumbersMultiTickAction: (tick_count = 1/2)
    AddTwoNumbersMultiTickAction: (tick_count = 2/6)
    AddTwoNumbersMultiTickAction: (tick_count = 2/4)
    AddTwoNumbersMultiTickAction: DONE 3 + 3 = 6
    AddTwoNumbersMultiTickAction: (tick_count = 3/6)
    AddTwoNumbersMultiTickAction: (tick_count = 3/4)
    AddTwoNumbersMultiTickAction: (tick_count = 4/6)
    AddTwoNumbersMultiTickAction: DONE 2 + 2 = 4
    AddTwoNumbersMultiTickAction: on_abort

In the first execution the first two nodes complete after two resp. four ticks and thus, the
``SimpleParallel`` node also completes. The third node is aborted. In the second execution
the third and second node complete after two resp. four ticks. Again, the ``SimpleParallel``
node completes as two nodes succedded, and as a consequence the first node is aborted. When aborting
a node the ``on_abort`` function of this node is called, this is why the message 'AddTwoNumbersMultiTickAction:
on_abort' is printed on standard output (see implementation of ``AddTwoNumbersMultiTickAction``).