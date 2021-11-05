![build workflow](https://github.com/CareBT/carebt_core/actions/workflows/python-app.yml/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# careBT - contingency aware Behavior Trees

[About](#about) | [Installation](#installation) | [Getting Started](#getting-started) | [Contacts](#contacts)

-----

## About
A Python library offering a Behavior Tree implementation which focuses on 
contingency handling - the key to master highly dynamic applications in
complex worlds. Although, careBT can be used in many different application, the
main use cases are inspired by mobile robots such as service robots, for example.


careBT is:
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

## Contacts

Andreas Steck - <steck.andi@gmail.com>
