import os
import sys

src_dir = os.path.abspath(__file__ + "/../../src")
sys.path.append(src_dir)

import maude

from BreadthFirstSearch import *
from HybridSearch import *
from DepthFirstSearch import *


from utils import *


basefile = os.path.abspath(__file__ + "/../../maude/symbolic-guarded/cash")

maudeLoad = f"{basefile}/case.bad.maude"
maudeModule = 'TEST-STATES-BAD'

maude.init(advise=False)
maude.load(maudeLoad)
maude.input("set print format off .")

module = maude.getModule(str(maudeModule))

num_solvers = 1
system_name = "sys"

system_pattern_str = "sys"
system_pattern = module.parseTerm(system_pattern_str)

goal_pattern_str = "{ B:Bool , < g : global | deadline-miss : true, AtS:AttributeSet > Cnf:Configuration }"
goal_pattern = module.parseTerm(goal_pattern_str)


start_terms = [
    "init(I0, I1, I2, I3, true)",
    "init(I0, I1, I2, I3, I0 + I3 > I1 + I2)",
    "init(I0, I1, I2, I1, I0 + I2 > I1)", 
]

depth = None
cycles = True

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




run_experiment(module, search_obj, start_terms, "cashbad", 
               system_pattern, goal_pattern, system_name, 
               depth=depth, num_solvers=num_solvers, cycles=cycles)


