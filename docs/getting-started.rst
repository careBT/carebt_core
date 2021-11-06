Getting Started
===============

Hello World example
-------------------

Create a file named :download:`helloworld.py <https://raw.githubusercontent.com/careBT/carebt_core/main/carebt/examples/helloworld.py>` with following content:

.. literalinclude:: ../carebt/examples/helloworld.py
    :language: python
    :lines: 15-
    :linenos:

Start the Python3 interpreter with :file:`helloworld.py` loaded:

.. code-block:: bash

    python3 -i helloworld.py

Run the **careBT** Behavior Tree with the HelloWorldAction:

.. code-block:: python

    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(HelloWorldAction)
    HelloWorldAction: Hello World !!!

Or, alternatively with log-level set to INFO

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