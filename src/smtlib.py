
import statistics

from functools import partial 

print = partial(print, flush=True)

# consts

cash_decl = \
"""(declare-const I0 Int)
(declare-const I1 Int)
(declare-const I2 Int)
(declare-const I3 Int)
(declare-const I4 Int)
(declare-const I5 Int)
"""


DEFAULT_OP_DICT = {
    "_and_" :  "and",
    "_or_"  :  "or",
    "_implies_" : "implies",
    "_xor_" : "xor",
    "not_" : "not",
    "_===_" : "=", #eq ?
    "_=/==" : "neq",
    "_<=_" : "<=",
    "_<_" : "<",
    "_>=_" : ">=",
    "_>_" : ">",

    "-_" : "-",
    "_+_" : "+",
    "_-_" : "-",
    "_*_" : "*",
    "_/_" : "/",
    "_div_" : "/",


    "_rem_" : "mod",
    "_?_:_" : "ite",

    
    
    }

DEFAULT_VAR_DICT = {
    "vv" : "Real",
    "tt" : "Int",
    "tw" : "Int",
    "rr" : "Real",

}

DEFAULT_CONST_SET = {
    "<Reals>"
}


class SMTLIB:

    def __init__(self, op_dict : dict = None, var_dict: dict = None):
        if op_dict is None:
            self.op_dict = DEFAULT_OP_DICT
        else:
            self.op_dict = op_dict

        if var_dict is None:
            self.var_dict = DEFAULT_VAR_DICT    
        else:
            self.var_dict = var_dict

        self.decl_dict = dict()
        self.cache = dict()

        self.cash_dict = dict()

        self.stats = []

        # cash decl
        self.cash_dict["I0"] = "Int"
        self.cash_dict["I1"] = "Int"
        self.cash_dict["I2"] = "Int"
        self.cash_dict["I3"] = "Int"
        self.cash_dict["I4"] = "Int"
        self.cash_dict["I5"] = "Int"


        self.new_decl = dict()

        self.new_decl["I0"] = "Int"
        self.new_decl["I1"] = "Int"
        self.new_decl["I2"] = "Int"
        self.new_decl["I3"] = "Int"
        self.new_decl["I4"] = "Int"
        self.new_decl["I5"] = "Int"



    def clean_symbol(self, symbol):
        cleaned = symbol.replace('"', '').replace(" ", "")
        cleaned = f'|"{cleaned}"|'
        return cleaned
        

    #z3 version 4.8.12
    # breaks on some newer versions of z3
    def mk_decl(self):
        result = ""
        for key, value in self.decl_dict.items():
            result += f"(declare-const {self.clean_symbol(key)} {value})\n"

        for key, value in self.cash_dict.items():
            result += f"(declare-const {key} {value})\n"

        return result


    def mk_bool(self, term, save=True):
        op = str(term.symbol())
        term_str = str(term)

        if term_str in self.cache:
            return self.cache[term_str]



        if op in self.op_dict:
            args = term.arguments()
            
            ret = f"({self.op_dict[op]} "
            for arg in args:
                ret += self.mk_bool(arg, save=False) + " "
            ret += ")"

            if save:
                self.cache[term_str] = ret
                
            
            return ret


        elif op in self.var_dict:
            if str(term) not in self.decl_dict:
                self.decl_dict[str(term)] = self.var_dict[op]
            return f"{self.clean_symbol(str(term))}"

        
        elif op == "<Reals>":
            return f"{term.toFloat()}"
            
        elif op == "<Integers>":
            return f"{term.toInt()}"

        elif op == "true" or op == "false":
            return op
        

        # symbolic-guard operators
        elif op in ["s_", "0", "Int"]:
            return f"{term}"


        else:
            print("ERROR")
            raise ValueError(f"unknown maude operator {op}", op)


    def mk_assertion(self, term):
        cond = self.mk_bool(term)
        decl = self.mk_decl()

        self.stats.append(cond.count("(and") + 1)

        smt_string = f"{decl}\n(assert {cond})"
        return smt_string


    
    def print_stats(self, file=None):
        if self.stats:
            print("*** SMT LIB STATS START ***", file=file)
            print("AVERAGE", sum(self.stats) / len(self.stats), file=file)
            print("MEDIAN", statistics.median(self.stats), file=file)
            print("MAX", max(self.stats), file=file)
            print("MIN", min(self.stats), file=file)
            print("TOTAL", sum(self.stats), file=file)
            print("LENGTH", len(self.stats), file=file)
            print("*** SMT LIB STATS END ***", file=file)









    