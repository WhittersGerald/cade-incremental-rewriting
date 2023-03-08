import os
import sys

src_dir = os.path.abspath(__file__ + "/../../src")
sys.path.append(src_dir)


import maude

from BreadthFirstSearch import *
from HybridSearch import *
from DepthFirstSearch import *


from utils import *

basefile = os.path.abspath(__file__ + "/../../maude/soft-agents")


maudeLoad = f"{basefile}/vehicle/logicalScenarios/pedestrian-crossing/scenarios/noSensorErrors/load-pedestrian-resilience.maude"
maudeModule = 'SCENARIO-CROSSING'

maude.init(advise=False)
maude.load(maudeLoad)
maude.input("set print format off .")

module = maude.getModule(str(maudeModule))

num_solvers = 1
system_name = "ASystem"


system_pattern_str = "c:ASystem"
system_pattern = module.parseTerm(system_pattern_str)

goal_pattern = None


start_terms = [
    "asysPedXLine(3,3/1,2/1,1/1,1/10)",
    "asysPedXLine(4,3/1,2/1,1/1,1/10)",
    "asysPedXLine(5,3/1,2/1,1/1,1/10)",

    "asysPedXLine(3,4/1,2/1,1/1,1/10)",
    "asysPedXLine(4,4/1,2/1,1/1,1/10)",
    "asysPedXLine(5,4/1,2/1,1/1,1/10)",

]

depth = None
cycles = False

if len(sys.argv) < 2:
    print("Please enter an argument")
    exit()

arg = sys.argv[1]

if arg.lower() == "bfs":
    search_obj = BreadthFirst
    num_solvers = None

elif arg.lower() == "dfs":
    search_obj = DepthFirst

else:
    try:
        depth = int(arg)

        if depth < 0:
            raise Exception
        
        search_obj = Hybrid

    except:
        print("Invalid argument")
        exit()




run_experiment(module, search_obj, start_terms, "CPS", 
               system_pattern, goal_pattern, system_name, 
               depth=depth, num_solvers=num_solvers, cycles=cycles)


