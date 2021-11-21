Writing a node with parameters
==============================

Overview
--------

This tutorial shows how to implement nodes in **careBT** which use input and/or output parameters. In this example an ``ActionNode``,
called ``AddTwoNumbersAction``, is implemented which receives two numbers (*?x*, *?y*) as input parameters, adds these two numbers and binds the
result to an output parameter (*?z*). This is, of course, a simplified example, as adding two numbers is typically not done by an custom
action node. But it demonstrates how parameters are working in **careBT**, without caring about the scenario and how "realistic" it is.

The signature (input/output parameters) of the node is defined by a string provided to the constructor of the
**careBT** node the custom node inherits from and works for all **careBT** nodes in the same way. The syntax is
*<list of input parameters> => <list of output parameters>* with parameter names starting with *?*. 
Each parameter is then available in the custom node class with the name *_<variable-name>*.


Create the AddTwoNumbersAction ActionNode
-----------------------------------------

Create a file named ``action_with_params.py`` with following content.
Or use the provided file: :download:`action_with_params.py <../../carebt/examples/action_with_params.py>`


.. literalinclude:: ../../carebt/examples/action_with_params.py
    :language: python
    :lines: 15-
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The first two statements are the includes for the ``ActionNode`` and the ``NodeStatus``.

.. literalinclude:: ../../carebt/examples/action_with_params.py
    :language: python
    :lines: 15-16

The ``AddTwoNumbersAction`` node is implemented as a Python class which inherits from ``ActionNode``.

.. literalinclude:: ../../carebt/examples/action_with_params.py
    :language: python
    :lines: 19

The class definition is followed by the `Docstring <https://www.python.org/dev/peps/pep-0257/>`__
documentation of the node, which also documents the interface (input/output parameters).

.. literalinclude:: ../../carebt/examples/action_with_params.py
    :language: python
    :lines: 20-37

The constructor (``__init__``) of the ``AddTwoNumbersAction`` needs to call the constructor (``super().__init__``)
of the ``ActionNode`` and passes the bt_runner and the signature as arguments. The input parameters are *?x* and *?y*,
and the output parameter is *?z*. These parameters are then available inside the node as member variables, called:
*_x*, *_y* and *_z*.

.. literalinclude:: ../../carebt/examples/action_with_params.py
    :language: python
    :lines: 39-40

The ``on_init`` function is called rigth after the node was created. It is the place to put the code which should
be executed once, after the node was created. In this example it is implemented that the two input parameters are
checked if values are bound to them during creation. If the variables are not bound (``... is None``), the default value 0
is set.

.. literalinclude:: ../../carebt/examples/action_with_params.py
    :language: python
    :lines: 42-46

In the ``on_tick`` function the two inputs are added and assiged to the output. Furthermore, this calculation is
printed on standard output and the node status is set to ``SUCCESS``. Thus, the ``AddTwoNumbersAction``
node is not ticked again.

.. literalinclude:: ../../carebt/examples/action_with_params.py
    :language: python
    :lines: 48-52

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter with :file:`action_with_params.py` loaded:

.. code-block:: bash

    python -i action_with_params.py

Run the ``AddTwoNumbersAction`` node:

.. code-block:: python

    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(AddTwoNumbersAction, '2 3 => ?sum')
    AddTwoNumbersAction: calculating: 2 + 3 = 5
    >>> bt_runner.run(AddTwoNumbersAction, '4 => ?sum')
    2021-11-12 22:13:07 WARN AddTwoNumbersAction takes 2 argument(s), but 1 was/were provided
    AddTwoNumbersAction: calculating: 4 + 0 = 4
    >>> bt_runner.run(AddTwoNumbersAction, '=> ?sum')
    2021-11-12 22:13:48 WARN AddTwoNumbersAction takes 2 argument(s), but 0 was/were provided
    AddTwoNumbersAction: calculating: 0 + 0 = 0