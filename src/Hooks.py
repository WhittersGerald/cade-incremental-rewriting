
from smtlib import SMTLIB
from SolverList import SolverList
from z3 import Solver, z3

import maude
import traceback

from z3 import *
import sys



def check_arg(arg1 : maude.Term):

    if str(arg1) == "(true).Bool":
        return True
    
    elif str(arg1) == "(false).Bool":
        return False
    

    return None


def check_sat(rsat : z3.CheckSatResult):

    if str(rsat) == "sat":
        return True

    elif str(rsat) == "unsat":
        return False
    
    else:
        raise Exception(f"Checking solver resulted in: {rsat}, exiting.")


class NonIncrSAT(maude.Hook):

    def __init__(self):
        self.smtlib = SMTLIB()
        super().__init__()


    def run(self, term, data):

        try: 
            module = term.symbol().getModule()
            arg = next(term.arguments())

            if check_arg(arg) is not None:
                return arg

            cond = self.smtlib.mk_assertion(arg)

            s = Solver()
            s.from_string(cond)
            rsat = s.check()

            result = check_sat(rsat)

            return module.parseTerm(f"({str(result).lower()}).Bool")

        except:
            traceback.print_exc()
            raise Exception(("ERROR IN EVALUATING SAT IN NonIncrSAT"))



class IncrSAT(maude.Hook):

    def __init__(self, solvers : SolverList):
        
        self.solvers = solvers
        self.smtlib = solvers.smtlib
        super().__init__()

    
    def run(self, term, data):
        try:
            module = term.symbol().getModule()
            args = term.arguments()

            arg1 = next(args)
            index = next(args).toInt()

            if check_arg(arg1) is not None:
                return arg1
            
            cond = self.smtlib.mk_assertion(arg1)
            solver = self.solvers[index]
            
            solver.push()
            solver.from_string(cond)
            rsat = self.solvers.check(index)
            result = check_sat(rsat)
            solver.pop()

            return module.parseTerm(f"({str(result).lower()}).Bool")

        
        except:
            traceback.print_exc()
            raise Exception(("ERROR IN EVALUATING SAT IN IncrSAT"))

   


class SystemSAT(maude.Hook):

    def __init__(self, solvers: SolverList):
        self.solvers = solvers
        self.smtlib = solvers.smtlib

        super().__init__()


    def run(self, term, data):
        try:
            module = term.symbol().getModule()
            args = term.arguments()

            self.solvers.push()

            for i, arg in enumerate(args):
                early_check = check_arg(arg)

                if early_check:
                    continue
                    
                if early_check is False:
                    return arg


                cond = self.smtlib.mk_assertion(arg)
                solver = self.solvers[i]
                solver.from_string(cond)
                rsat = self.solvers.check(i)
                result = check_sat(rsat)



                if not result:
                    self.solvers.pop()
                    return module.parseTerm(f"({str(result).lower()}).Bool")
                               

            return module.parseTerm("(true).Bool")

                    

        except:
            traceback.print_exc()
            raise Exception(("ERROR IN EVALUATING SAT IN SystemSAT"))
        


