![build workflow](https://github.com/CareBT/carebt_core/actions/workflows/python-app.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# careBT - contingency aware Behavior Trees

[About](#about) | [Installation](#installation) | [Getting Started](#getting-started) | [Documentation](#documentation) | [Background](#background) | [Contacts](#contacts) | [Bibliography](#bibliography)

-----

## About
A Python library offering a Behavior Tree implementation which focuses on contingency handling - the key to master complex applications in highly dynamic worlds. Although, careBT can be used in many different application, the main use cases are inspired by mobile robots such as service robots, for example.

**careBT** is:
- easy to use
- lightweight
- well tested (test-coverage > 95%)

## Installation

From [pypi](https://pypi.python.org/pypi/carebt):
```
TODO pip install carebt
```

From source:
```
# git clone https://github.com/careBT/carebt_core.git
# cd carebt_core
# ./build_and_install.sh
```

## Getting Started

After installing careBT, run the Hello World example.

Create a file named `helloworld.py` with following content:
``` python
from carebt.actionNode import ActionNode
from carebt.nodeStatus import NodeStatus


class HelloWorldAction(ActionNode):

    def __init__(self, bt_runner):
        super().__init__(bt_runner)

    def on_tick(self) -> None:
        print('HelloWorldAction: Hello World !!!')
        self.set_status(NodeStatus.SUCCESS)

```

Start the Python interpreter with the file helloworld.py:
```
python -i helloworld.py
```

Start the careBT Behavior Tree:
```
>>> from carebt.behaviorTreeRunner import BehaviorTreeRunner
>>> bt_runner = BehaviorTreeRunner()
>>> bt_runner.run(HelloWorldAction)
HelloWorldAction: Hello World !!!
```
Or alternatively with log level set to INFO:
```
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
```

## Documentation

Documentation can be found at [https://carebt.readthedocs.io/](https://carebt.readthedocs.io/)

## Background

The work on **careBT** is strongly influenced by my previous work I have done at the [University of Applied
Sciences in Ulm](https://www.servicerobotik-ulm.de/). Especially the design and development of *SmartTCL* [1] [2] [3] itself and the huge amount of different
behaviors and scenarios we were working on.

An excerpt of these scenarios can be seen here:
* [Mobile Manipulation - Robot "Kate" cleans up the table. This video shows how the robot is disturbed in different situations and thus, hindered to fulfill its job. But due to the contingency handling mechanisms in SmartTCL it finds and executes alternative solutions.](https://www.youtube.com/watch?v=xtLK-655v7k)

* [Mobile Manipulation - Robot "Kate" Prepares and Delivers Coffee.](https://www.youtube.com/watch?v=B4E1uC3Cbps)

* [The Robot Butler Scenario shows another huge scenario.](https://www.youtube.com/watch?v=nUM3BUCUnpY)

## Contacts

Andreas Steck - <steck.andi@gmail.com>

## Bibliography

[1] [Andreas Steck, Christian Schlegel. SmartTCL: An Execution Language for Conditional Reactive Task Execution in a Three Layer Architecture for Service Robots. In Proc. of SIMPAR 2010 Workshops (International Workshop on Dynamic languages for RObotic and Sensors systems (DYROS)), 2nd Intl. Conf. on Simulation, Modeling, and Programming for Autonomous Robots, Pages 274-277, Darmstadt, ISBN 978-3-00-032863-3, 2010.](https://www.researchgate.net/publication/259389996_SmartTCL_An_Execution_Language_for_Conditional_Reactive_Task_Execution_in_a_Three_Layer_Architecture_for_Service_Robots)

[2] [Andreas Steck. Conditional Reactive Task Execution in a Three Layer Architecture for Service Robots. Master Thesis, November 2010.](http://www.servicerobotik-ulm.de/drupal/sites/default/files/masterthesis-steck.pdf)

[3] [Andreas Steck, Christian Schlegel. Managing execution variants in task coordination by exploiting design-time models at run-time. In Proc. IEEE Int. Conf. on Robotics and Intelligent Systems (IROS), San Francisco, USA, September, 2011.](https://ras.papercept.net/conferences/conferences/IROS11/program/IROS11_ContentListWeb_3.html)
