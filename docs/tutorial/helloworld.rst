Writing a Hello World ActionNode
=================================

Overview
--------

This tutorial shows the classical HelloWorld example. It is the simplest possible starting point to learn **careBT**.


Steps
-----

1 Create the Hello World ActionNode
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a file named ``helloworld.py`` with following content.
Or copy it from ::download:`helloworld.py <https://raw.githubusercontent.com/careBT/carebt_core/main/carebt/examples/helloworld.py>`


.. literalinclude:: ../../carebt/examples/helloworld.py
    :language: python
    :lines: 15-
    :linenos:

1.1 The code explained
~~~~~~~~~~~~~~~~~~~~~~

The first two statements are the includes for the ``ActionNode`` and the ``NodeStatus``.

The ``HelloWorldAction`` node is implemented as a Python class which inherits from ``ActionNode``.

The constructor (``__init__``) of the ``HelloWorldAction`` needs to call the constructor (``super().__init__``)
of the ``ActionNode`` and pass the bt_runner as an argument. This is required by the **careBT** execution engine to work
properly. The constructor is also the place to register the input/output parameters of the node and will be explained
in further tutorials.

In the ``on_tick`` function the code has to be placed which is executed every time the node is ticked. In this example
this is a simple print statemant which shows the text "HelloWorldAction: Hello World !!!" on the standard output. The
following line puts the node into the status ``SUCCESS``, which indicates that the execution of the node has completed
and the execution was succesful. Thus, the ``HelloWorldAction`` node is not ticked again.

2 Run the example
^^^^^^^^^^^^^^^^^

Start the Python3 interpreter with :file:`helloworld.py` loaded:

.. code-block:: bash

    python3 -i helloworld.py

Run the **HelloWorldAction** node:

.. code-block:: python

    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(HelloWorldAction)
    HelloWorldAction: Hello World !!!

Or, alternatively run it with log-level set to INFO:

.. code-block:: python

    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> from carebt.abstractLogger import LogLevel
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.get_logger().set_log_level(LogLevel.INFO)
    >>> bt_runner.run(HelloWorldAction)
    2021-11-05 20:48:06 INFO ---------------------------------- tick-count: 1
    2021-11-05 20:48:06 INFO ticking RootNode
    2021-11-05 20:48:06 INFO creating HelloWorldAction
    2021-11-05 20:48:06 INFO ticking HelloWorldAction - NodeStatus.IDLE
    HelloWorldAction: Hello World !!!
    2021-11-05 20:48:06 INFO finished RootNode
    2021-11-05 20:48:06 INFO ---------------------------------------------------
    2021-11-05 20:48:06 INFO bt execution finished
    2021-11-05 20:48:06 INFO status:  NodeStatus.SUCCESS
    2021-11-05 20:48:06 INFO message: 
    2021-11-05 20:48:06 INFO ---------------------------------------------------
