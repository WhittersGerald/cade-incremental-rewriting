import maude
import cvc5
from cvc5 import Kind

class SMT_CHECK(maude.Hook):
  global smt_model
  def run (self,term,data):
    try:
      module = term.symbol().getModule();
      solver = mkSolver();
      arg = next(term.arguments());
      arg.reduce()
      vvs = module.parseTerm("getVVs(" + str(arg) + ",none)")
      vvs.reduce()
      vvsMap = dict();
      # mkVars only if there are variables.
      if(str(vvs) != "(none).Strings"):
        vvsMap = mkVars(vvs,vvsMap,solver)
      form = mkBool(arg,module,vvsMap,solver);
      # print(form)
      solver.assertFormula(form)
      r2 = solver.checkSat()
      print(r2)
      if (str(r2) == "sat"):
        for x in vvsMap:
          smt_model[x] = solver.getValue(vvsMap[x])
        return module.parseTerm("(true).Bool");
      elif (str(r2) == "unsat"): 
        return module.parseTerm("(false).Bool");
      print("UNDEFINED: NOT ABLE TO DETERMINE SAT")
    except:
      print("ERROR IN EVALUATING SAT ")
      return module.parseTerm("(false).Bool");

def mkSolver():
  solver = cvc5.Solver()
  # We will ask the solver to produce models and unsat cores,
  # hence these options should be turned on.
  solver.setOption("produce-models", "true");
  solver.setOption("produce-unsat-cores", "false");
  # The simplest way to set a logic for the solver is to choose "ALL".
  # This enables all logics in the solver.
  # Alternatively, "QF_ALL" enables all logics without quantifiers.
  # To optimize the solver's behavior for a more specific logic,
  # use the logic name, e.g. "QF_BV" or "QF_AUFBV".
  # Set the logic
  solver.setLogic("QF_NRA");
  return solver;

def mkVars(vvs,vvsMap,solver):
  realSort = solver.getRealSort();
  args = list(vvs.arguments());
  # Case only one symbol
  if len(args) == 0:
    vvVar = solver.mkConst(realSort,str(vvs))
    vvsMap[str(vvs)] = vvVar
    return vvsMap;  
  for vv in list(vvs.arguments()):
    vvVar = solver.mkConst(realSort,str(vv))
    vvsMap[str(vv)] = vvVar
  return vvsMap;

def mkBool(term,module,vvsMap,solver):
  op = str(term.symbol())
  # print(op)
  if (op == "true"):
    return solver.mkTrue();
  if (op == "false"):
    return solver.mkFalse();    
  if (op == "_and_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.AND, b1, b2);
  if (op == "_or_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.OR, b1, b2);
  if (op == "_implies_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    b3 = solver.mkTerm(Kind.IMPLIES, b1, b2)
    return b3;
  if (op == "_xor_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    b2 = mkBool(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.XOR, b1, b2);
  if (op == "not_"):
    args = term.arguments()
    b1 = mkBool(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.NOT, b1);
  if (op == "_===_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    t3 = solver.mkTerm(Kind.EQUAL,t1,t2);
    return t3;
  if (op == "_<=_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    t3 = solver.mkTerm(Kind.LEQ,t1,t2);
    return t3;
  if (op == "_<_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.LT,t1,t2);
  if (op == "_>=_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.GEQ,t1,t2);
  if (op == "_>_"):
    args = term.arguments()
    t1 = mkArith(next(args),module,vvsMap,solver)
    t2 = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.GT,t1,t2);
  return 1 / 0;

def mkArith(term,module,vvsMap,solver):
  op = str(term.symbol())
  sort = str(term.getSort())
  # print(term)
  # print(op)
  # print(sort)
  # print(list(term.arguments()))
  # print(term.toFloat())
  if (op == "vv"):
    vvs = module.parseTerm("getVVs(" + str(term) + ",none)")
    vvs.reduce()
    return vvsMap[str(vvs)] 
  # PosRat
  if (list(term.arguments()) == []):
    return solver.mkReal(term.toFloat())
  if (op == "_+_"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.ADD,first,second)
  if (op == "-_"):    
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.SUB,solver.mkReal(0),first)
  if (op == "_-_"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    try:
      second = mkArith(next(args),module,vvsMap,solver)
      return solver.mkTerm(Kind.SUB,first,second)
    except:
      return solver.mkTerm(Kind.SUB,first)
  if (op == "_*_"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.MULT,first,second)
  if (op == "_/_" and sort == "SymReal"):
    args = term.arguments()
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.DIVISION,first,second)
  if (op == "_/_" and sort == "SymTerm"):
    args = term.arguments()
    # print(term)
    first = mkArith(next(args),module,vvsMap,solver)
    second = mkArith(next(args),module,vvsMap,solver)
    return solver.mkTerm(Kind.DIVISION,first,second)
  # print(term)
  # print(op)
  # print(sort)
  return 1 / 0
