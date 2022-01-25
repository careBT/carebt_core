.. role:: python(code)
   :language: python

Introduction
============

Overview
--------

The following tutorials are a collection of step-by-step instructions meant to learn the
usage of **careBT**. The best way to approach the tutorials is to walk through them in order
as they build off from each other.


Get Started
-----------

The easiest way to run the examples is to install ``carebt`` with pip.

.. code-block:: bash

    pip install carebt

Then run your python interpreter:

.. code-block:: bash

    $ python

And then run the examples from the tutorials, as for example, the ``HelloWorldAction``:

.. code-block:: python

    >>> import carebt
    >>> from carebt.examples.helloworld import HelloWorldAction
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(HelloWorldAction)
    HelloWorldAction: Hello World !!!

Or import all examples and run the ``HelloWorldAction``:

.. code-block:: python

    >>> import carebt
    >>> import carebt.examples
    >>> bt_runner = carebt.BehaviorTreeRunner()
    >>> bt_runner.run(carebt.examples.HelloWorldAction)
    HelloWorldAction: Hello World !!!

.. hint::
    If creating a own Python package for the tutorial, the import statements for
    the examples need to be adjusted. E.g. :python:`from helloworld import HelloWorldAction`
    in case of starting the Python interpreter directly from the source folder. But that depends
    on the used package structure.