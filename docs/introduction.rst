Introduction
============

About
-----

A Python library offering a Behavior Tree implementation which focuses on contingency handling
- the key to master complex applications in highly dynamic worlds. Although, careBT can be used
in many different application, the main use cases are inspired by mobile robots such as service
robots, for example.

**careBT** is:

*  easy to use
*  lightweight
*  well tested (test-coverage > 95%)

Background
----------

The work on **careBT** is strongly influenced by my previous work I have done at the
`University of Applied Sciences in Ulm <https://www.servicerobotik-ulm.de/>`__. Especially
the design and development of *SmartTCL* [1] [2] [3] itself and the huge amount of different
behaviors and scenarios we were working on.

An excerpt of these scenarios can be seen here:

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
