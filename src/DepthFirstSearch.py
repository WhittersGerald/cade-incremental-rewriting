from collections import deque
from Hooks import NonIncrSAT, IncrSAT, SystemSAT
from SolverList import SolverList

import math
import maude


class DepthFirst():
    def __init__(self, num_solvers, system_name, cycles=False):
        self.solvers = SolverList(num_solvers)

        self.nonincr_hook = NonIncrSAT()
        self.incr_hook = IncrSAT(self.solvers)
        self.system_hook = SystemSAT(self.solvers)

        # to make results consistent (dont count root state)
        self.count = -1
        self.queue = deque()
        self.found: maude.Term = None

        self.depth_found = -1

        self.system_name = system_name

        self.cycles = cycles
        self.visited = set()

    def register_hooks(self):
        maude.connectEqHook("NonIncrSAT", self.nonincr_hook)
        maude.connectEqHook("IncrSAT", self.incr_hook)
        maude.connectEqHook("SystemSAT", self.system_hook)


    def search(self, term: maude.Term, system_pattern : maude.Term,
               goal_pattern: maude.Term, max_count=math.inf):
        

        module: maude.Module = term.symbol().getModule()

        if self.system_name == "ASystem":
            self.stop_time = module.parseTerm(f"getStopTime({term})")
            self.stop_time.reduce()


        term.reduce()

        self._dfs(module, term, system_pattern,
                          goal_pattern, max_count=max_count)


    def _dfs(self, module, term, system_pattern, goal_pattern, max_count=math.inf):

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
                    return

        # if goal pattern is same sort as system pattern
        # we need to check that current term matches goal pattern
        elif str(system_pattern.getSort()) == str(goal_pattern.getSort()):
            is_match = bool(list(term.match(goal_pattern)))
            if is_match:
                self.found = term
                return

        # otherwise goal pattern is some operator that is used in
        # the "such that" section of maude search
        else:
            goal_str = str(goal_pattern).replace(self.system_name, str(term))
            goal_result = module.parseTerm(goal_str)
            goal_result.reduce()

            if str(goal_result) == "(true).Bool":
                self.found = term
                return


        for child_term, *_ in term.search(maude.ONE_STEP, system_pattern):
            self._dfs(module, child_term, system_pattern, goal_pattern,
                            max_count=max_count)

            self.solvers.pop()
