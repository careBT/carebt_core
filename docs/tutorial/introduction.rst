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

The easiest way to run the examples is to clone the ``carebt-core`` repository and run
the python interpreter from there:

.. code-block:: bash

    $ git clone https://github.com/careBT/carebt_core.git
    $ cd carebt_core
    $ python

And then run the examples from the tutorials, as for example, the ``HelloWorldAction``:

.. code-block:: python

    >>> from carebt.examples.helloworld import *
    >>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
    >>> bt_runner = BehaviorTreeRunner()
    >>> bt_runner.run(HelloWorldAction)
    HelloWorldAction: Hello World !!!


.. hint::
    If creating a own Python package for the tutorial, the import statements for
    the examples need to be adjusted. E.g. :python:`from helloworld import *` in case of
    starting the Python interpreter directly from the source folder. But that depends on
    the used package structure.