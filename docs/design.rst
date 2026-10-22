Design/Concepts
===============

Overview
--------

**CareBT** was developed to support the implementation of complex robotics applications which operate
in the real world. Such a robot will be faced with a huge amount of different situations which can not be
foreseen in advance. Several decisions how the task-tree should further be expanded are not known during
design-time of the behavior, and have thus to be taken at runtime. To achieve that, the task coordination
mechanism of the robot has (i) to be able to cope with these situations and provide alternative "plans" how
the robot should continue its execution, (ii) to be able to modify the currently executing task-tree at
runtime and (iii) to be able to generate a sub-tree during runtime depending on the current state of the world.
That involves being able to remove nodes from the tree and add new nodes to the tree while "executing"
the tree.

.. note::

    Thus, the main difference between **careBT** and typical behavior tree implementations is the built in mechanism
    to modify the task-tree at runtime depending on situation and context.


Architecture
------------

.. figure:: /_static/carebt_overview.svg
   :alt: careBT as the sequencing layer between an advisory layer (planners, AI agents, domain experts)
         and a skill layer (navigation, localization, perception, manipulation, robot base)
   :align: center
   :width: 100%

   **careBT** in the sequencing layer between the advisory layer and the skill layer.

**CareBT** is located in the sequencing layer, between the advisory layer and the skill layer:

* **Advisory layer**: "expert algorithms" like symbolic planners (e.g. PDDL), AI agents (e.g. LLMs or VLAs) or
  other domain experts. **CareBT** asks them for advice by providing the goal and the current context, like the task,
  the world model or camera images. They answer with a plan, like an action sequence or parameter advice, which
  **careBT** transforms into a sub-tree (see `Dynamic sub-tree generation at runtime`_). The advisors have no direct
  control over the robot. Their advice is always executed and supervised by **careBT**.
* **Sequencing layer**: **careBT** executes the behavior tree and maintains a knowledge base with the robot state,
  the current task and the state of the world (see `Maintaining a model of the world`_). While executing, the tree
  is adapted to the current situation by inserting, replacing and removing nodes. If something goes wrong, a
  contingency-handler replaces the failed part of the tree by an alternative solution (see `Contingency handling`_
  and `Runtime modification of the behavior tree`_).
* **Skill layer**: the capabilities of the robot like navigation, localization, perception, manipulation or the
  robot base. **CareBT** orchestrates and parameterizes the skills and receives their progress and feedback.
  A failure reported by a skill is raised as a contingency in the corresponding node of the tree.

The **careBT-core** is independent of the framework which is used to connect to the skills. This connection is
provided by a framework integration, like `careBT ROS2 <https://github.com/careBT/carebt_ros2>`__.

In the following several concepts and mechanisms of **careBT** are discussed:


Principle of subsidiarity
-------------------------

**CareBT** follows the principle of subsidiarity. In the context of task coordination that means, that a parent node "asks"
a child node to fulfill a dedicated task within a defined decision space. The child node is allowed to try to reach the goal
within that space. If something goes wrong the child node can try to fix the issue within the provided decision space. In case
that this is not possible the child node announces that back to the parent and the parent node can try to fix the issue in its
decision space (which is typically a bit wider).

Each node is responsible to do its best trying to achieve the specified goal and, if it fails, state the reason for the failure.
Thus, the parent which has a wider context can then try to find an alternative solution taking the reason for the failure into
account.


Black-box reusability of (sub-)behaviors
----------------------------------------

To create a custom node, respectively a sub-tree in **careBT** a Python class has to be implemented which inherits
from one of the **careBT** TreeNode classes. These classes are: ActionNode, SequenceNode, FallbackNode, ParallelNode and RateControlNode.
Thus, a custom node, respectively a sub-tree always has a name (the name of the class). Using this name they can directly
be executed, as well as being used in a sub-tree. This allows a black-box reusability of each node - without caring about
how the node is implemented, from which class it is inherited and how the node further expands (or not). To create, for example,
a sequence of nodes a new node has to be implemented which inherits from SequenceNode. Then, the nodes which should be executed inside
this sequence are added as child nodes. As this new node has a name it can be executed and tested, as well as being reused inside
another node to build more complex behaviors.

This strict black-box reusability of nodes accelerates and facilitates the development of complex behaviors. Each node
(respectively sub-tree) of a complex behavior can be implemented, executed and tested individually. This allows to simply compose
complex behaviors out of well tested, reusable sub-behaviors. For example, when developing the behavior of a robot which should
perform a manipulation task like fetching objects from a table the different behaviors like navigation, object recognition and
grasping an object are developed and tested individually and then composed to the more complex behavior.


Contingency handling
--------------------

One important feature of **careBT** is the contingency handling mechanism. This mechanism allows to react to the different
situations and failures which occur during execution of a behavior. Almost every action performed in a real world
scenario can possibly go wrong. Thus, a task coordination language should provide mechanisms which allow to react to these
situations by performing an alternative sequence of actions. Therefore, in **careBT**, contingency-handlers can be attached
to the parent node with the attributes when they should be triggered. This trigger takes the name of the child node,
the status of the child node and the contingency-message into account. 

In **careBT** each node does not just complete with `SUCCESS` or `FAILURE`, but also with an additional contingency message.
Especially in case that something goes wrong it is important to also provide the reason for the failure and not only the
information that the task failed. Only that allows to perform an adequate reaction to the failure. For example, when a path planner
fails to plan the path to a desired goal, several failures can occur. The start position might be blocked by an obstacle, the goal
position might be blocked by an obstacle, the goal position might be outside of the map or no path could be found (although start
and goal position are valid). In case that the start position is blocked by an obstacle this position could be cleared in the map
with some clearance and then the path planner can be triggered again. Otherwise, in case that the goal position is blocked by an
obstacle the alternative could be to navigate the robot in the region of the desired goal and check the surroundings there if the
desired goal region is still blocked or can be reached now.

Furthermore, in **careBT** a control node has - in addition to the status and the contingency message - a contingency history.
This contingency history documents which contingency handlers were triggered in which situations. This can be used, for example,
in the `on_delete` callback to finally set the contingency message taking the executed contingency handlers into account.
For example, in case the contingency handler fixes the situation, the node finishes with `SUCCESS` and typically an empty
contingency message. But in such a case the parent might want 'to know' that it was necessary to run a contingency handler to
complete the task. And thus, setting the contingency message in the `on_delete` callback depending on the contingency history
allows to provide this additional information. Additionally, this contingency history can be accessed by the parent node to
check on its own how the task was completed.


Dynamic sub-tree generation at runtime
--------------------------------------

This is another powerful feature of **careBT**. It allows to implement a node for which the exact sequence of its child nodes is
not "programmed" beforehand (as it is not known). But an "expert algorithm" like a symbolic planner, for example, can be called which 
provides a sequence of actions that perfectly suits the current situation and desired goal. Each of these actions can then be transformed
into a corresponding **careBT** node (which typically is not only a single node, but a whole sub-tree) and be executed. This allows to take
the decision on the expansion of the whole tree at runtime at different levels of the tree and by different "expert algorithms".

An example of that mechanism is shown in the mobile manipulation scenario where the
`robot "Kate" cleans up a table <https://www.youtube.com/watch?v=xtLK-655v7k>`__.
(The mentioned scenario was developed with *SmartSoft* and *SmartTCL*, but demonstrates the feature of dynamic sub-tree generation very
well. The implementation of this mechanism in **careBT** is very similar to the one in *SmartTCL*.)

.. important::
    ``Contingency-handlers`` can be registered in the node which dynamically added the children to be able to react to failures which
    might occur at this level. Thus, the contingency handling at the level of the dynamically created sequence works independent from
    the exact execution sequence.


Runtime modification of the behavior tree
-----------------------------------------

In **careBT** the task-tree can simply be modified by removing nodes from the tree or by adding nodes to the tree. These
modifications are typically done by the contingency-handlers which are triggered to react to any circumstances in the
behavior execution.


Dataflow between nodes
----------------------

A **careBT** node can have any number of input or output parameters. Input parameters are used to pass information into a
node, while the output parameters are used to pass information out of a node. The outputs of a node can be used as inputs for
another node. These input/output parameters are directly attached to the interface of a node and thus explicitly visible. As
Python is not typed these parameters are also not typed. Hence, a parameter can be a primitive variable (e.g. bool, int, string)
as well as a complex type (e.g. class, dict, list).


Maintaining a model of the world
--------------------------------

To reflect and maintain a model of the world, a knowledge base should be used. For example, such a knowledge base holds
the information about the different locations the robot
can drive to, the different objects the robot can manipulate, the persons the robot can recognize and so on. Furthermore,
information gathered at runtime is also reflected and updated there. For example, the status of current tasks the robot
should perform or the orders it should deliver.