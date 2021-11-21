Writing SequenceNodes
=====================

Overview
--------

This tutorial demonstrates a couple of simple **careBT** ``SequenceNodes``. For the demos
the ``ActionNode`` implemented in the previous tutorial is reused and two additional
``ActionNodes`` are implemented.


Create the ActionNodes and the SimpleSequence
---------------------------------------------

Create a file named ``simple_sequence.py`` with following content.
Or use the provided file: :download:`simple_sequence.py <../../carebt/examples/simple_sequence.py>`


.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 15-93
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The first statements are the includes for the Python random library, the **careBT** classes (``ActionNode``, 
``NodeStatus``, ``SequenceNode``) and the ``AddTwoNumbersAction``.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 15-21

The ``CreateRandomNumberAction`` is a custom ``ActionNode`` which generates a random number which is bound to
the output parameter *?number*.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 26-44

The ``PrintNumberAction`` is a custom ``ActionNode`` which prints the provided *?numer* on standard output.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 49-66

The ``SimpleSequence`` node is implemented as a Python class which inherits from ``SequenceNode``.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 71

The class definition is followed by the `Docstring <https://www.python.org/dev/peps/pep-0257/>`__
documentation of the node, which also documents the interface (output parameters).

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 72-84

The constructor (``__init__``) of the ``SimpleSequence`` needs to call the constructor (``super().__init__``)
of the ``SequenceNode`` and pass the bt_runner and the signature as arguments. The signature defines one
output parameter called *?c*.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 86-87

The ``on_init`` function is called rigth after the node was created. It is the place to put the code which should
be executed once, after the node was created. For a ``SequenceNode`` the child nodes are typically added here.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 89-93


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter with :file:`simple_sequence.py` loaded:

.. code-block:: bash

    python -i simple_sequence.py

Run the ``SimpleSequence`` node:

.. code-block:: python

    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(SimpleSequence, '=> ?x')
    CreateRandomNumberAction: number = 6
    CreateRandomNumberAction: number = 5
    AddTwoNumbersAction: calculating: 6 + 5 = 11
    PrintNumberAction: number = 11

    >>> bt_runner.run(SimpleSequence, '=> ?x')
    CreateRandomNumberAction: number = 7
    CreateRandomNumberAction: number = 9
    AddTwoNumbersAction: calculating: 7 + 9 = 16
    PrintNumberAction: number = 16


Create the SimpleSequence2
--------------------------

Add the following content to ``simple_sequence.py``.
Or use the provided file: :download:`simple_sequence.py <../../carebt/examples/simple_sequence.py>`

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 98-127

The code explained
^^^^^^^^^^^^^^^^^^

The ``SimpleSequence2`` is a modified version of the ``SimpleSequence``. It shows how simple a different
sequence of children can be created and how the parameters can be bound across the different children.

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter with :file:`simple_sequence.py` loaded:

.. code-block:: bash

    python -i simple_sequence.py

Run the ``SimpleSequence`` node:

.. code-block:: python

    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(SimpleSequence2, '5 => ?x')
    CreateRandomNumberAction: number = 2
    AddTwoNumbersAction: calculating: 5 + 2 = 7
    PrintNumberAction: number = 7
    CreateRandomNumberAction: number = 2
    AddTwoNumbersAction: calculating: 7 + 2 = 9
    PrintNumberAction: number = 9

    >>> bt_runner.run(SimpleSequence2, '7 => ?x')
    CreateRandomNumberAction: number = 1
    AddTwoNumbersAction: calculating: 7 + 1 = 8
    PrintNumberAction: number = 8
    CreateRandomNumberAction: number = 2
    AddTwoNumbersAction: calculating: 8 + 2 = 10
    PrintNumberAction: number = 10


Create the SimpleSequence3
--------------------------

Add the following content to ``simple_sequence.py``.
Or use the provided file: :download:`simple_sequence.py <../../carebt/examples/simple_sequence.py>`

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 132-146

The code explained
^^^^^^^^^^^^^^^^^^

The ``SimpleSequence3`` shows anoher example how custom ``ActionNodes`` and custom ``SequenceNodes`` can be reused
and how the parameters can be bound.

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter with :file:`simple_sequence.py` loaded:

.. code-block:: bash

    python -i simple_sequence.py

Run the ``SimpleSequence`` node:

.. code-block:: python

    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(SimpleSequence3)
    CreateRandomNumberAction: number = 5
    CreateRandomNumberAction: number = 8
    AddTwoNumbersAction: calculating: 5 + 8 = 13
    PrintNumberAction: number = 13
    PrintNumberAction: number = 13
    CreateRandomNumberAction: number = 2
    AddTwoNumbersAction: calculating: 13 + 2 = 15
    PrintNumberAction: number = 15
    CreateRandomNumberAction: number = 1
    AddTwoNumbersAction: calculating: 15 + 1 = 16
    PrintNumberAction: number = 16
    PrintNumberAction: number = 16

    >>> bt_runner.run(SimpleSequence3)
    CreateRandomNumberAction: number = 1
    CreateRandomNumberAction: number = 2
    AddTwoNumbersAction: calculating: 1 + 2 = 3
    PrintNumberAction: number = 3
    PrintNumberAction: number = 3
    CreateRandomNumberAction: number = 6
    AddTwoNumbersAction: calculating: 3 + 6 = 9
    PrintNumberAction: number = 9
    CreateRandomNumberAction: number = 3
    AddTwoNumbersAction: calculating: 9 + 3 = 12
    PrintNumberAction: number = 12
    PrintNumberAction: number = 12
