This is an experimental prototype for the verification of whether 
services, such as HTTP web-servers, are subject to DDoS attacks, 
such as Slowloris. 

The accompanying paper

Abraão Aires Urquiza, Musab A. AlTurki, Max I. Kanovich, 
Tajana Ban Kirigin, Vivek Nigam, Andre Scedrov, and Carolyn L. Talcott.
Resource-Bounded Intruders in Denial of Service Attacks. 
In 32nd IEEE Computer Security Foundations Symposium, 
CSF 2019, Hoboken, NJ, USA, June 25-28, 2019, pp. 382–396, 2019.

and the submitted journal paper describe the foundations of the problem as 
well as the design choices for the construction of the tool

This Readme explains how to execute the tool.

This machinery does not come with any type of warranty. 
For any questions please contact the paper authors.

---------------------------
Tool Required: 
  * Maude 3.0 integrated with the CVC4 SMT-solver.
    (Notice that the oficial version with Maude is integrated with the 
     Yices SMT solver and it will not work, as we need to solve non-linear 
     constraints.)
    This Maude version can be obtained from 
      https://github.com/maude-se/maude-se.github.io

---------------------------
File Descriptions:

  * symbolic.maude contains the sorts and operators for specifying 
    symbols and constraints.
  * config.maude contains the sorts and operators for specifying verification problems
  * exe.maude contains the rewrite rules specifying the operational semantics of configurations
  * load contains the basic files that need to be loaded to carry out verification
  * the directory examples contains some examples of verification problems.
     - Each file contains a verification scenario that is parametric in two values, for example, initSlow1(pxsB, msgs1B). 
     The parameters, pxsB, msgs1B, specify respectively the bound on the number of parallel protocol sessions and the bound on the number of messages in the network.
     The value 0 denotes no bounds.

-----------------------------
Sample Execution:
 * execute in the console:

> maude load

This will load the basic machinery.
 
 * Load your verification problem, e.g., the ones in the directory example:

Maude> load examples/slowloris.maude

 * execute search commands. 

For example:

search [1] in SLOWLORIS : initSlow1(0, 0) =>* conf:Config such that goal(conf:Config, Threshold) = (true).Bool .

The end of each file in the example directory contains several experiments of search commands and their results. 
These experiments were carried out on Mac 2.2 GHz Intel Core i7 with 16GB of memory. 

