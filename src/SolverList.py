import statistics
from timeit import default_timer as timer

from z3 import Solver

from smtlib import SMTLIB

class SolverList:

    def __init__(self, num_solvers):
        self.num_solvers = num_solvers
        self.solvers : list[Solver] = None
        self.stats = []
        self.smtlib = SMTLIB()

        self.reset()

    def reset(self):
        self.solvers = [Solver() for _ in range(self.num_solvers)]
        for solver in self.solvers:
            solver.set("solver2_timeout", 1)

    def push(self):  
        for solver in self.solvers:
            solver.push()

    def pop(self):
        for solver in self.solvers:
            solver.pop()


    def from_string(self, s, index):
        self.solvers[index].from_string(s)


    def check(self, index):
        start = timer()
        rsat = self.solvers[index].check()
        end = timer()

        self.stats.append(end - start)

        return rsat

        
    def __getitem__(self, index: int):
        return self.solvers[index]
    
    def print_stats(self, file=None):
        if self.stats:
            print("AVERAGE", sum(self.stats) / len(self.stats), file=file)
            print("MEDIAN", statistics.median(self.stats), file=file)
            print("MAX", max(self.stats), file=file)
            print("MIN", min(self.stats), file=file)
            print("TOTAL", sum(self.stats), file=file)
            print("LENGTH", len(self.stats), file=file)
