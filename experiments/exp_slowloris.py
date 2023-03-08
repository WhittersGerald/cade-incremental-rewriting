import os
import sys

src_dir = os.path.abspath(__file__ + "/../../src")
sys.path.append(src_dir)

import maude

from BreadthFirstSearch import *
from HybridSearch import *
from DepthFirstSearch import *


from utils import *


basefile = os.path.abspath(__file__ + "/../../maude/boundedIntruder")


loadFile = f"{basefile}/load"
maudeLoad = f"{basefile}/examples/slowloris.maude"
maudeModule = 'SLOWLORIS'

maude.init(advise=False)
maude.load(loadFile)
maude.load(maudeLoad)

module = maude.getModule(str(maudeModule))

num_solvers = 2
system_name = "conf:Config"


system_pattern_str = "(pc:PlayerConf)!(tr1:TimeSym)!(ms:MSet)!(b3:Boolean)!(b4:Boolean)!(n5:Nat)!(n6:Nat)"
system_pattern = module.parseTerm(system_pattern_str)

goal_pattern_str = "goal(conf:Config, Threshold)"
goal_pattern = module.parseTerm(goal_pattern_str)



start_terms = [
    "initSlow3(1, 0)",
    "initSlow4(1, 0)",
    "initSlow2(1, 1)",
    "initSlow3(1, 1)",
    "initSlow4(1, 1)"
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




run_experiment(module, search_obj, start_terms, "slowloris", 
               system_pattern, goal_pattern, system_name, 
               depth=depth, num_solvers=num_solvers, cycles=cycles)


