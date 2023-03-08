from collections import deque
from Hooks import NonIncrSAT, IncrSAT, SystemSAT
from SolverList import SolverList
from z3 import Solver

import math
import maude



class BreadthFirst():

    def __init__(self, system_name):
        self.solvers = SolverList(1)

        self.nonincr_hook = NonIncrSAT()
        self.incr_hook = NonIncrSAT()
        self.system_hook = NonIncrSAT()

        self.count = 0
        self.queue = deque()
        self.visited = None
        self.found : maude.Term = None
        self.depth_found = -1

        self.system_name = system_name
        self.stop_time = 0

        self.global_depth = 0


    def register_hooks(self):
        maude.connectEqHook("NonIncrSAT", self.nonincr_hook)
        maude.connectEqHook("IncrSAT", self.incr_hook)
        maude.connectEqHook("SystemSAT", self.system_hook)



    def search(self, term : maude.Term, system_pattern : maude.Term, 
               goal_pattern : maude.Term, max_count=math.inf):
        
        self.visited = set()
        self.queue = deque()
        term.reduce()
        self.queue.append((term, 0))

        module : maude.Module = term.symbol().getModule()

        if self.system_name == "ASystem":
            self.stop_time = module.parseTerm(f"getStopTime({term})")
            self.stop_time.reduce()

        
        while self.found is None and self.count < max_count:

            if not self.queue:
                break

            
            current, global_depth = self.queue.popleft()
            

            if str(current) in self.visited:
                continue


            self.visited.add(str(current))
            self.count += 1


            # For soft agents goal check
            if self.system_name == "ASystem":

                time = module.parseTerm(f"getTime({current})")
                time.reduce()
                if self.stop_time == time:

                    goal = module.parseTerm(f"IncrSAT(enforceSP(badSP, {current}))")
                    goal.reduce()


                    if str(goal) == "(true).Bool":
                        self.found = term
                        self.depth_found = global_depth
                        return

                
            # if goal pattern is same sort as system pattern
            # we need to check that current term matches goal pattern
            elif str(system_pattern.getSort()) == str(goal_pattern.getSort()):
                is_match = bool(list(current.match(goal_pattern)))
                

                if is_match:
                    self.found = current
                    self.depth_found = global_depth
                    return

            # otherwise goal pattern is some operator that is used in
            # the "such that" section of maude search
            else:
                goal_str = str(goal_pattern).replace(self.system_name, str(current))
                goal_result = module.parseTerm(goal_str)
                goal_result.reduce()


                if str(goal_result) == "(true).Bool":
                    self.found = current
                    self.depth_found  = global_depth
                    return


            for child_term, *_ in current.search(maude.ONE_STEP, system_pattern):
                self.queue.append((child_term, global_depth+1))

