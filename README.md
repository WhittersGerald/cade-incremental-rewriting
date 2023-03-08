# cade-incremental-rewriting

### Requirements

Python 3.9 or newer


### Setup

Clone the repository using 

`git clone https://github.com/WhittersGerald/cade-incremental-rewriting.git`

Change directory:

`cd cade-incremental-rewriting`

Create a virtual environment using 

`python3 -m venv .venv`

If on Windows/Powershell activate virtual environment using:

`.venv\Scripts\Activate.ps1`

If on Windows/CMD activate virtual environment using:

`.venv\Scripts\activate.bat`

If on Posix/bash activate virtual environment using:

`source .venv/bin/activate`

Install packages using:

`python3 -m pip install -r requirements.txt`



### Replications

Scripts for running the experiments are located in ./experiments and named beginning with "exp_". The scripts
take a required argument for the type of search. The options are, "bfs" for breadth-first search, "dfs" for depth-first search, 
or some nonnegative integer for hybrid search with that integer as the depth parameter.

Running Slowloris experiments with bfs would be:

`python3 experiments/exp_slowloris.py bfs`

Running the CASH-OK System experiments with hybrid search for depth parameter 4 would be:

`python3 experiments/exp_cashok.py 4`

Running the Cyber-Physical System experiments with dfs would be:

`python3 experiments/exp_cps.py dfs`


Results are found in experiments/results

### Notes

Cyber-Physical System experiments are bounded, so the depth parameter used is a multiplier of the
argument given to replicate the results in the paper. Only 1, 2, and 3 are depth multipliers that make sense and will
choose depth parameters that are 1/3, 2/3, and 3/3 of the search tree respectively.

Some DFS experiments for Slowloris and CASH-OK/CASH-BAD will run indefinitely. Changing the experiments that will be run
can be done by modifying the script file and commenting out entries in the list `start_terms`

An older version of Z3 is used and listed in requirements.txt. Newer versions modified the call to `Solver.from_string` which
changed the format of allowed smtlib2 strings. A fix is being worked on for this project to allow newer versions of Z3.