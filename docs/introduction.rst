Introduction
============

About
-----

**CareBT** is a Python library offering a behavior tree implementation which focuses on contingency
handling - the key to master complex applications which operate in highly dynamic worlds. Although,
**careBT** can be used in many different applications, the main use cases are inspired by mobile
robots such as service robots, for example.

The **careBT-core** (https://github.com/careBT/carebt_core) is kept completely independent from any
frameworks it can be used in. However, such an integration can easily be done. For mobile robotics
applications such a framework could be `ROS <https://www.ros.org/>`__
or `ROS2 <https://www.ros.org/>`__, for example.

**careBT** is:

*  implemented in Python
*  easy to use
*  lightweight
*  well tested (test-coverage > 95%)
*  well documented

Framework integration
---------------------

The following framework integrations of **careBT** are currently available:

* ROS2: https://github.com/careBT/carebt_ros2

Background
----------

The work on **careBT** is strongly influenced by the previous work I have done at the
`Service Robotics Lab in Ulm <https://www.servicerobotik-ulm.de/>`__. Especially the
design and implementation of the task coordination language *SmartTCL* [1] [2] [3],
a Lisp-based implementation of task-nets focusing on handling contingencies which
typically occur in real world scenarios. One important powerful feature of *SmartTCL* is the
ability to dynamically create, expand and modify the task-tree during runtime depening
on the current situation and state of the world. However, *SmartTCL* was developed in the
context of the *SmartSoft* framework and is bound 
to some of the *SmartSoft* concepts, especially to the event-pattern. But the existence of
such an event mechanism should not be taken for granted to beeing able to work together
with other frameworks. Furthermore, *SmartTCL* is implemented in Lisp, which is not widely
used and has a steep learning curve.

On the other hand behavior trees, which can be seen as a variant of task-nets, have emerged
in the past few years. Behavior trees provide basic guidelines and concepts on how to
design and implement a task-tree and its execution engine.
One of these concepts is, for example, that a node is periodically ticked as long as it is in
state RUNNING, and switches to one of the states SUCCESS or FAILURE as soon as it completes.
Behavior trees have already shown their effectivness in developing robotics scenarios.
Nevertheless, the powerfull mechanisms to dynamically create, expand and modify the task-tree
at runtime are not present in classical behavior tree implementations [4] [5] [6]. 

The above led to the idea to develop **careBT** by combining the powerful concepts
of *SmartTCL* with the clean structure of behavior trees. And to use Python as programming
language as it is an interpreted programming language with a relatively fast learning curve.
Furthermore the development of **careBT** is split into the framework independent
**careBT-core** and its framework specific integrations (e.g. ROS2: https://github.com/careBT/carebt_ros2).

An excerpt of some scenarios which demonstrate the powerful mechanisms of *SmartTCL*
can be seen in the following videos on YouTube:

*  `Mobile Manipulation - Robot "Kate" cleans up the table. This video shows how the robot
   is disturbed in different situations and thus, hindered to fulfill its job. But due to 
   the contingency handling mechanisms in SmartTCL it finds and executes alternative 
   solutions. <https://www.youtube.com/watch?v=xtLK-655v7k>`__

* `Mobile Manipulation - Robot "Kate" Prepares and Delivers Coffee.
  <https://www.youtube.com/watch?v=B4E1uC3Cbps>`__

* `The Robot Butler Scenario shows another huge scenario.
  <https://www.youtube.com/watch?v=nUM3BUCUnpY>`__

Bibliography
------------

[1] Andreas Steck, Christian Schlegel. SmartTCL: An Execution Language for Conditional Reactive Task Execution in a Three Layer Architecture for Service Robots. In Proc. of SIMPAR 2010 Workshops (International Workshop on Dynamic languages for RObotic and Sensors systems (DYROS)), 2nd Intl. Conf. on Simulation, Modeling, and Programming for Autonomous Robots, Pages 274-277, Darmstadt, ISBN 978-3-00-032863-3, 2010.

[2] Andreas Steck. Conditional Reactive Task Execution in a Three Layer Architecture for Service Robots. Master Thesis, November 2010.

[3] Andreas Steck, Christian Schlegel. Managing execution variants in task coordination by exploiting design-time models at run-time. In Proc. IEEE Int. Conf. on Robotics and Intelligent Systems (IROS), San Francisco, USA, September, 2011.

[4] BehaviorTree.CPP, https://www.behaviortree.dev/

[5] Py Trees, https://py-trees.readthedocs.io/

[6] Colledanchise Michele, Ogren Petter. (2018). Behavior Trees in Robotics and AI: An Introduction. 10.1201/9780429489105, https://btirai.github.io/