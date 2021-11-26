.. role:: python(code)
   :language: python

Writing a HelloWorld ActionNode
=================================

Overview
--------

This tutorial shows the classical HelloWorld example. It is the simplest possible starting point to learn **careBT**.


Create the HelloWorldAction ActionNode
--------------------------------------

Create a file named ``helloworld.py`` with following content.
Or use the provided file: :download:`helloworld.py <../../carebt/examples/helloworld.py>`


.. literalinclude:: ../../carebt/examples/helloworld.py
    :language: python
    :lines: 15-
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The first two statements are the includes for the ``ActionNode`` and the ``NodeStatus``.

.. literalinclude:: ../../carebt/examples/helloworld.py
    :language: python
    :lines: 15-16

The ``HelloWorldAction`` node is implemented as a Python class which inherits from ``ActionNode``.

.. literalinclude:: ../../carebt/examples/helloworld.py
    :language: python
    :lines: 19

The class definition is followed by the `Docstring <https://www.python.org/dev/peps/pep-0257/>`__
documentation of the node.

.. literalinclude:: ../../carebt/examples/helloworld.py
    :language: python
    :lines: 20-27

The constructor (``__init__``) of the ``HelloWorldAction`` needs to call the constructor (``super().__init__``)
of the ``ActionNode`` and pass the bt_runner as an argument. This is required by the **careBT** execution engine to work
properly. The constructor is also the place to register the input/output parameters of the node and will be explained
in further tutorials.

.. literalinclude:: ../../carebt/examples/helloworld.py
    :language: python
    :lines: 29-30

In the ``on_tick`` function the code has to be placed which is executed every time the node is ticked. In this example
this is a simple print statemant which shows the text "HelloWorldAction: Hello World !!!" on the standard output. The
following line puts the node into the status ``SUCCESS``, which indicates that the execution of the node has completed
and the execution was succesful. Thus, the ``HelloWorldAction`` node is not ticked again.

.. literalinclude:: ../../carebt/examples/helloworld.py
    :language: python
    :lines: 32-34

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``HelloWorldAction`` node:

.. code-block:: python

    >>> from carebt.examples.helloworld import *
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(HelloWorldAction)
    HelloWorldAction: Hello World !!!
