careBT nodes
============

The class diagram below shows the **careBT** nodes and how they inherit
from each other.

.. graphviz::

   digraph foo {

      TreeNode [shape=box, color="grey", fontcolor="grey", label="TreeNode"];
      ActionNode [shape=box, label="ActionNode"];
      ControlNode [shape=box, color="grey", fontcolor="grey", label="ControlNode"];

      FallbackNode [shape=box, label="FallbackNode"];  
      SequenceNode [shape=box, label="SequenceNode"];
      ParallelNode [shape=box, label="ParallelNode"];
      RateControlNode [shape=box, label="RateControlNode"];
        
      TreeNode -> ActionNode [arrowtail = onormal, dir = back];
      TreeNode -> ControlNode [arrowtail = onormal, dir = back, color="grey"];
      ControlNode -> FallbackNode [arrowtail = onormal, dir = back];
      ControlNode -> SequenceNode [arrowtail = onormal, dir = back];
      ControlNode -> ParallelNode [arrowtail = onormal, dir = back];
      ControlNode -> RateControlNode [arrowtail = onormal, dir = back];
   }

The grey nodes are internal nodes only. The black ones are intended to be used to create
own custom nodes.