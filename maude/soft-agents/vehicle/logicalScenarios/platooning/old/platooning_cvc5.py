import maude
from maude_cvc5 import *
from timeit import default_timer as timer
from datetime import timedelta
from isResilient import *
import basic_lib

maude.init()
# maude.load("vehicle/examples/platooning/load-platooning-manh-4SP.maude")
# maude.load("vehicle/examples/platooning/load-platooning-manh-4SP-timesteps.maude")
maude.load("vehicle/examples/platooning/load-platooning-manh-4SP-timesteps-split.maude")
hook = SMT_CHECK()
maude.connectEqHook('smtCheck',hook)
m = maude.getModule('SCENARIO-PLATOONING')

asys = m.parseTerm("asys0")
asys.reduce()

checkTimeDur(m,asys)

# start = timer()
# print("=====> Start Time =", start)
# t = m.parseTerm("as0(2)");
# t.rewrite(6)
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))

# start = timer()
# print("=====> Start Time =", start)

# t = m.parseTerm("isResilient(['SCENARIO-PLATOONING], as0(3), 3, safeSP,badSP,saferSP)")
# t.reduce()
# print(t)
# end = timer()
# print("====> End Time =", end)
# print("====> Total Time =", end - start)
# print(timedelta(seconds=end-start))
