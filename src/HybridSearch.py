
from collections import deque
from Hooks import NonIncrSAT, IncrSAT, SystemSAT
from SolverList import SolverList

import math
import maude





class Hybrid():

    def __init__(self, num_solvers, system_name, cycles=False):
        self.solvers = SolverList(num_solvers)

        self.nonincr_hook = NonIncrSAT()
        self.incr_hook = IncrSAT(self.solvers)
        self.system_hook = SystemSAT(self.solvers)


        self.count = 0
        self.queue = deque()
        self.found : maude.Term = None

        self.depth_found = -1

        self.system_name = system_name

        self.cycles = cycles
        self.visited = set()

    # probably requires maude.init to already be called
    def register_hooks(self):
        maude.connectEqHook("NonIncrSAT", self.nonincr_hook)
        maude.connectEqHook("IncrSAT", self.incr_hook)
        maude.connectEqHook("SystemSAT", self.system_hook)


    # change max_count to global_max_depth
    # keep class attribute for current_absolute_depth
    def search(self, term : maude.Term, system_pattern : maude.Term, 
               goal_pattern : maude.Term, depth : int, max_count=math.inf):
        

        self.queue = deque()
        module : maude.Module = term.symbol().getModule()

        if self.system_name == "ASystem":
            self.stop_time = module.parseTerm(f"getStopTime({term})")
            self.stop_time.reduce()


        term.reduce()
        self.queue.append(term.search(maude.ONE_STEP, system_pattern))
        

        while self.found is None and self.count < max_count:


            if not self.queue:
                break
                
            search_result = self.queue.popleft()

            self.solvers.reset()

            while self.found is None and self.count < max_count:
                next_result = next(search_result, None)

                if next_result is None:
                    break

                next_child = next_result[0]

                
                self._dfs_bounded(module, next_child, system_pattern,
                                  goal_pattern, glob_depth=self.depth_found+1,
                                    max_depth=depth, max_count=max_count)
                
                self.solvers.pop()
            

    def _dfs_bounded(self, module, term, system_pattern, goal_pattern,
                     max_depth=math.inf, curr_depth=0, glob_depth=0, max_count=math.inf):
        
        if self.found is not None:
            return
        
        if self.count > max_count:
            return
        
        

        if self.cycles:
            if str(term) in self.visited:
                return

            self.visited.add(str(term))
        
        self.count += 1

        # For soft agents goal check
        if self.system_name == "ASystem":
                
            time = module.parseTerm(f"getTime({term})")
            time.reduce()


            if self.stop_time == time:

                goal = module.parseTerm(f"IncrSAT(enforceSP(badSP, {term}))")
                goal.reduce()

                if str(goal) == "(true).Bool":
                    self.found = term
                    self.depth_found = glob_depth
                    return


        # if goal pattern is same sort as system pattern
        # we need to check that current term matches goal pattern
        elif str(system_pattern.getSort()) == str(goal_pattern.getSort()):
            is_match = bool(list(term.match(goal_pattern)))
            if is_match:
                self.found = term
                self.depth_found = glob_depth
                return

        # otherwise goal pattern is some operator that is used in
        # the "such that" section of maude search
        else:
            goal_str = str(goal_pattern).replace(self.system_name, str(term))
            goal_result = module.parseTerm(goal_str)
            goal_result.reduce()


            if str(goal_result) == "(true).Bool":
                self.found = term
                self.depth_found = glob_depth
                return


        if curr_depth == max_depth:
            self.queue.append(term.search(maude.ONE_STEP, system_pattern))
            self.depth_found = glob_depth

            return
        

        for child_term, *_ in term.search(maude.ONE_STEP, system_pattern):
            self._dfs_bounded(module, child_term, system_pattern, goal_pattern,
                             max_depth=max_depth, curr_depth=curr_depth+1,
                             glob_depth=glob_depth+1, max_count=max_count)
            
            self.solvers.pop()


    def print_stats(self, file=None):
        print("Count:", self.count, file=file)
        self.solvers.print_stats(file=file)

        


