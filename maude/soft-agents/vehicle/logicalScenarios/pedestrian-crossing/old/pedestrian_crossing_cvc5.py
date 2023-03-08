import sys
sys.path.append('../../../../lib_py')
import maude
from maude_cvc5 import *
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
import basic_lib


maude.init()
# maude.load("vehicle/examples/pedestrian-crossing/load-pedestrian.maude")

hook = SMT_CHECK()
maude.connectEqHook('smt_check',hook)

# maude.load("vehicle/examples/pedestrian-crossing/debug/exp-scenario-pedestrian-debug.maude")
# m = maude.getModule('DEBUG-SCENARIO-PLATOONING')
# t = m.parseTerm("condFinal@checkDur")
# t.reduce()

m = maude.getModule('SCENARIO-CROSSING')
# t = m.parseTerm("checkTimeDurSPtoSP1TimeStepsBot(saferSP,saferSP,asysPedXLineFixed(3,3/1,2/1,1/1,1/10),dt)")
# start = timer()
# print("=====> Start Time =", start)
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
# # ====> Total Time = 68.86222250600001
# # 0:01:08.862223

# t = m.parseTerm("checkTimeDurSPtoSP1TimeStepsBot(saferSP,safeSP,asysPedXLineFixed(3,3/1,2/1,1/1,1/10),dt)")
# start = timer()
# print("=====> Start Time =", start)
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
# # ====> Total Time = 94.73067677899999
# # 0:01:34.730677

# t = m.parseTerm("checkTimeDurSPtoSP1TimeStepsBot(safeSP,safeSP,asysPedXLineFixed(3,3/1,2/1,1/1,1/10),dt)")
# start = timer()
# print("=====> Start Time =", start)
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
# ====> Total Time = 42.89463604
# 0:00:42.894636

# t = m.parseTerm("checkTimeDurSPtoSP1TimeStepsBot(safeSP,unsafeSP,asysPedXLineFixed(3,3/1,2/1,1/1,1/10),dt)")
# start = timer()
# print("=====> Start Time =", start)
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
# # ====> Total Time = 66.201985764
# # 0:01:06.201986

# t = m.parseTerm("checkTimeDurSPtoSP1TimeStepsBot(unsafeSP,unsafeSP,asysPedXLineFixed(3,3/1,2/1,1/1,1/10),dt)")
# start = timer()
# print("=====> Start Time =", start)
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
# ====> Total Time = 0.008508337000000005
# 0:00:00.008508


# t = m.parseTerm("enforceSP(unsafeSP,asysPedXLine(3,3/1,2/1,1/1,1/10))");
# t.rewrite(10)
# print(t)

# start = timer()
# print("=====> Start Time =", start)
# t = m.parseTerm("isResilient(['SCENARIO-CROSSING], asysPedXLineFixed(2,3/1,2/1,1/1,1/10), 2, safeSP,badSP,saferSP)")
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
# # (false).Bool
# # ====> End Time = 20.316805249
# # ====> Total Time = 20.087639164000002
# # 0:00:20.087639

# start = timer()
# print("=====> Start Time =", start)
# t = m.parseTerm("isResilient(['SCENARIO-CROSSING], asysPedXLineFixed(3,3/1,2/1,1/1,1/10), 3, safeSP,badSP,saferSP)")
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))



# start = timer()
# print("=====> Start Time =", start)
# t = m.parseTerm("checkTimeDur(asysPedXLineFixed(3,3/1,2/1,1/1,1/10))")
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
