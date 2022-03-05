Writing SequenceNodes
=====================

Overview
--------

This tutorial demonstrates a couple of simple **careBT** ``SequenceNodes``. For the demos
the ``ActionNode`` (``AddTwoNumbersAction``) implemented in the previous tutorial is reused
and two additional ``ActionNodes`` are implemented. The first one (``CreateRandomNumberAction``)
generates a random numer and provides it as output parameter. The second one (``PrintNumberAction``)
prints the, as input parameter, provided number on standard output.


Create the ActionNodes and the SimpleSequence1
----------------------------------------------

This first example called ``SimpleSequence1`` contains four child nodes.

.. graphviz::

    digraph foo {
        s1 [shape=box, margin="0.05,0.1", label="«SequenceNode»\nSimpleSequence1"];

        s1c1 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s1c2 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s1c3 [shape=box, margin="0.05,0.1", label="«ActionNode»\nAddTwoNumbersAction"];
        s1c4 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];

        s1 -> s1c1
        s1 -> s1c2
        s1 -> s1c3
        s1 -> s1c4
   }

The first two nodes generate two random numbers, the third one adds them and the last
one prints the result.

Create a file named ``simple_sequence.py`` with following content.
Or use the provided file: :download:`simple_sequence.py <../../carebt/examples/simple_sequence.py>`


.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 15-96
    :linenos:

The code explained
^^^^^^^^^^^^^^^^^^

The first statements are the includes for the Python random library, the **careBT** classes (``ActionNode``, 
``NodeStatus``, ``SequenceNode``) and the ``AddTwoNumbersAction``.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 15-20

The ``CreateRandomNumberAction`` is a custom ``ActionNode`` which generates a random number which is bound to
the output parameter *?number*.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 26-45

The ``PrintNumberAction`` is a custom ``ActionNode`` which prints the provided *?number* on standard output.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 50-68

The ``SimpleSequence1`` node is implemented as a Python class which inherits from ``SequenceNode``.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 73

The class definition is followed by the `Docstring <https://www.python.org/dev/peps/pep-0257/>`__
documentation of the node, which also documents the interface (output parameters).

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 74-87

The constructor (``__init__``) of the ``SimpleSequence1`` needs to call the constructor (``super().__init__``)
of the ``SequenceNode`` and passes the bt_runner and the signature as arguments. The signature defines one
output parameter called *?c*.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 89-90

The ``on_init`` function is called rigth after the node was created. It is the place to put the code which should
be executed once, after the node was created. For a ``SequenceNode`` the child nodes are typically added here.

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 92-96


Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleSequence1`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.simple_sequence import SimpleSequence1
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(SimpleSequence1, '=> ?x')
    CreateRandomNumberAction: number = 6
    CreateRandomNumberAction: number = 5
    AddTwoNumbersAction: calculating: 6 + 5 = 11
    PrintNumberAction: number = 11

    >>> bt_runner.run(SimpleSequence1, '=> ?x')
    CreateRandomNumberAction: number = 7
    CreateRandomNumberAction: number = 9
    AddTwoNumbersAction: calculating: 7 + 9 = 16
    PrintNumberAction: number = 16


Create the SimpleSequence2
--------------------------

.. graphviz::

    digraph foo {
        s2 [shape=box, margin="0.05,0.1", label="«SequenceNode»\nSimpleSequence2"];

        s2c1 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s2c2 [shape=box, margin="0.05,0.1", label="«ActionNode»\nAddTwoNumbersAction"];
        s2c3 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];
        s2c4 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s2c5 [shape=box, margin="0.05,0.1", label="«ActionNode»\nAddTwoNumbersAction"];
        s2c6 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];

        s2 -> s2c1
        s2 -> s2c2
        s2 -> s2c3
        s2 -> s2c4
        s2 -> s2c5
        s2 -> s2c6
   }

The ``SimpleSequence2`` is a modified version of the ``SimpleSequence1``. It shows how simple a different
sequence of children can be created and how the parameters can be bound across the different children.

Add the following content to ``simple_sequence.py``.
Or use the provided file: :download:`simple_sequence.py <../../carebt/examples/simple_sequence.py>`

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 101-131
    :linenos:

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleSequence2`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.simple_sequence import SimpleSequence2
    >>> bt_runner = carebt.BehaviorTreeRunner()
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

.. graphviz::

    digraph foo {
        
        // make invisible ranks
        rank1 [style=invisible];
        rank2 [style=invisible];
        rank3 [style=invisible];
        rank4 [style=invisible];
        
        // make "invisible" (white) link between them
        rank1 -> rank2 [color=white];
        rank2 -> rank3 [color=white];
        rank3 -> rank4 [color=white];

        s1 [shape=box, margin="0.05,0.1", label="«SequenceNode»\nSimpleSequence1"];

        s1c1 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s1c2 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s1c3 [shape=box, margin="0.05,0.1", label="«ActionNode»\nAddTwoNumbersAction"];
        s1c4 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];

        s1 -> s1c1
        s1 -> s1c2
        s1 -> s1c3
        s1 -> s1c4

        s2 [shape=box, margin="0.05,0.1", label="«SequenceNode»\nSimpleSequence2"];

        s2c1 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s2c2 [shape=box, margin="0.05,0.1", label="«ActionNode»\nAddTwoNumbersAction"];
        s2c3 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];
        s2c4 [shape=box, margin="0.05,0.1", label="«ActionNode»\nCreateRandomNumberAction"];
        s2c5 [shape=box, margin="0.05,0.1", label="«ActionNode»\nAddTwoNumbersAction"];
        s2c6 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];

        s2 -> s2c1
        s2 -> s2c2
        s2 -> s2c3
        s2 -> s2c4
        s2 -> s2c5
        s2 -> s2c6

        s3 [shape=box, margin="0.05,0.1", label="«SequenceNode»\nSimpleSequence3"];

        s3c1 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];
        s3c2 [shape=box, margin="0.05,0.1", label="«ActionNode»\nPrintNumberAction"];

        s3 -> s1
        s3 -> s3c1
        s3 -> s2
        s3 -> s3c2
        
        {
            rank = same;
            // Here you enforce the desired order with "invisible" edges and arrowheads
            rank2 -> s1 -> s3c1 [ style=invis ];
            rankdir = LR;
        }
        {
            rank = same;
            // Here you enforce the desired order with "invisible" edges and arrowheads
            rank4 -> s2 -> s3c2 [ style=invis ];
            rankdir = LR;
        }
   }

The ``SimpleSequence3`` shows another example how custom ``ActionNodes`` and custom ``SequenceNodes`` can be reused
and how the parameters can be bound.

Add the following content to ``simple_sequence.py``.
Or use the provided file: :download:`simple_sequence.py <../../carebt/examples/simple_sequence.py>`

.. literalinclude:: ../../carebt/examples/simple_sequence.py
    :language: python
    :lines: 136-151
    :linenos:

Run the example
^^^^^^^^^^^^^^^

Start the Python interpreter and run the ``SimpleSequence3`` node:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.simple_sequence import SimpleSequence3
    >>> bt_runner = carebt.BehaviorTreeRunner()
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

.. note::
    The ``SimpleSequence3`` example shows how easily a behavior can be composed out of already existing
    sub-behaviors, while the individual sub-behaviors can still be executed and tested separately.
