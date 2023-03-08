# Description

The code is distributed into three main directories:

- lib contains the main maude files for the Soft-Agents framework. We refer to the VNC 2020 paper below for a detailed explanation of the Maude code.
- lib_py contains the basic python libraries in particular:
  - basic_lib.py contains the machinery to collect and parse information from maude to python, e.g., function printLog collects into arrays important data of agents (speed, acceleration, position) available in the log of the system configuration.
  - maude_z3.py contains the machinery to check the satisfiability of symbolic constraints using the Z3 solver. Whenever a check for satisfiability returns true, the corresponding model is stored in the global variable smt_model.
  - isResilient.py contains the machinery to check whether a scenario is resilient.
- vehicle contains specific libraries, in the sub-directory lib-vehicle, and logical scenarios, in the directory logicalScenarios, related to autonomous vehicles. Examples of logical scenarios are pedestrian crossing and platooning.

# Dependencies

Before using the symbolic soft-agents, be sure to have installed the following tools/software:

- Python version 3.9 or later
- Maude bindings for python: The bindings can be installed by running pip, e.g., pip install maude. For more information, see https://github.com/fadoss/maude-bindings  
- Z3 bindings for python: The bindings can be installed by running pip, e.g., pip install z3-solver. For more information, see https://github.com/z3prover/z3

Soft agents has been tested on Mac using an Intel processor.  
It should work on Windows, but we have not tested it yet.  
Since the Z3 is not available for Mac M1 machines, the symbolic soft-agents does not work natively on it.

# Run Symbolic Soft-Agents by Example

We use as running example the platooning scenario available at the folder vehicle/logicalScenarios/platooning. To run the check for resilience simply:

1. cd vehicle/logicalScenarios/platooning
2. python3 platooning_z3.py

## Specifying a test scenario

Inside the file platooning_z3.py, one specifies which scenario is to be used. For example, consider the following code:

maudeLoad = "scenarios/following/load-platooning-manh.maude"  
maudeModule = 'SCENARIO-PLATOONING'  
asys = "asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)"  
t = 4  
safer = 3  
safe = 2   
bad = 1  

It specifies the maude file to load, namely, "scenarios/following/load-platooning-manh.maude". This load file corresponds to a platooning scenario where the ego vehicle is following a leader vehicle. Moreover, it is using a Manhantan distance measure for specifying safety properties. 
The definition of the configuration ("asys(36,basicCond and testBounds0(3/1,2/1,1/1,1/10),2)") is to be found at the maude Module 'SCENARIO-PLATOONING'.
Moreover, the code (t = 4) above specifies that the system shall return to safety (i.e., safer property) in 4 time units. 
Finally, safer, safe, bad specify the parameters for the time gaps for the safety properties.

## Examples of Existing Scenarios

- Platooning: To run these experiments see the explanation above.
  - following specifies a scenario with two vehicles, a leader and a ego vehicle that is following the leader.

- Pedestrian Crossing: To run these experiments is similar to the platooning example shown above, but instead running python3 pedestrian_crossing_z3.py in the folder vehicle/logicalScenarios/pedestrian-crossing.
  - noSensorErrors (in folder vehicle/logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors) contains a pedestrian crossing scenario with one pedestrian and an ego vehicle. The ego vehicle detects the pedestrian and the measurement of the pedestrian's position, speed and direction has no errors.

  - errorPeds (in folder vehicle/logicalScenarios/pedestrian-crossing/scenarios/errorPedS) contains a pedestrian crossing scenario with one pedestrian and an ego vehicle. The ego vehicle detects the pedestrian, but the measurement of the direction of the pedestrian is erroneous. The amount of error is specified symbolically.

# Some useful publications

* [Safety Proofs using Symbolic Soft Agents] V. Nigam and C. Talcott. Automating Safety Proofs about Cyber-Physical Systems using Rewriting Modulo SMT. In Rewriting Logic and its Applications (WRLA), 2022.

* [Maude Bindings in Python] R. Rubio. Maude as a library: an efficient all-purpose programming interface. In Rewriting Logic and its Applications (WRLA), 2022.

* [Non-Symbolic Soft Agents Specification of Platooning] Yuri Gil Dantas, Vivek Nigam, and Carolyn Talcott. A Formal Security Assessment Framework for Cooperative Adaptive Cruise Control. In IEEE Vehicular Networking Conference (VNC), 2020. http://nigam.info/docs/vnc20.pdf

# Contact information

For inquiries, bug-report, etc, please do not hesitate to contact:
* Vivek Nigam <vivek.nigam@gmail.com>
* Carolyn Talcott <carolyn.talcott@gmail.com>