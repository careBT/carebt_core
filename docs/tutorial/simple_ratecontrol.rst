Writing a RateControlNode
=========================

Overview
--------

This tutorial demonstrates the **careBT** ``RateControlNode``. Therefore the ``SimpleRateControl`` node
is implemented which has one child, the ``AddTwoNumbersMultiTickAction``. The ``SimpleRateControl`` node
throttles the tick rate of the ``AddTwoNumbersMultiTickAction`` node to 1000 ms.


Create the SimpleRateControl node
---------------------------------

Create a file named ``ratecontrol.py`` with following content.
Or use the provided file: :download:`ratecontrol.py <../../carebt/examples/ratecontrol.py>`


.. literalinclude:: ../../carebt/examples/ratecontrol.py
    :language: python
    :lines: 15-
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The constructor (``__init__``) of the ``SimpleRateControl`` node needs to call the constructor (``super().__init__``)
of the ``RateControlNode`` and passes the bt_runner, the throttling rate in ms and the signature as arguments.

.. literalinclude:: ../../carebt/examples/ratecontrol.py
    :language: python
    :lines: 39-40

In the ``on_init`` function the child node is added.

.. literalinclude:: ../../carebt/examples/ratecontrol.py
    :language: python
    :lines: 42-43


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleRateControl`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.ratecontrol import SimpleRateControl
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(SimpleRateControl, '5 2 3 => ?result')
    AddTwoNumbersMultiTickAction: (tick_count = 1/5)
    AddTwoNumbersMultiTickAction: (tick_count = 2/5)
    AddTwoNumbersMultiTickAction: (tick_count = 3/5)
    AddTwoNumbersMultiTickAction: (tick_count = 4/5)
    AddTwoNumbersMultiTickAction: DONE 2 + 3 = 5

The ``AddTwoNumbersMultiTickAction`` node is executed until the fifth tick completes
the execution of the node. The time between the ticks is 1000 ms.