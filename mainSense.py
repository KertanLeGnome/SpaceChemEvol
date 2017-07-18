import reactor
import atom
import copy

def genEmptyMap():
	return [["E" for Y in range(0,8)] for X in range(0,10)] 

r = reactor.Reactor()
r.setVerbose(True)
blueArrowMap = genEmptyMap()
redArrowMap = genEmptyMap()
blueActionMap = genEmptyMap()
redActionMap = genEmptyMap()

# gen of puzzle 
redArrowMap[1][7] = "D"
redArrowMap[1][5] = "R"
redArrowMap[2][5] = "U"
redArrowMap[2][6] = "R"
redArrowMap[5][5] = "R"
redArrowMap[9][5] = "U"
redArrowMap[9][6] = "U"
redArrowMap[9][7] = "L"

redActionMap[6][7] = "SL"
redActionMap[5][7] = "INA"
redActionMap[4][7] = "SY"
redActionMap[3][7] = "SY"
redActionMap[1][6] = "GR"
redActionMap[1][5] = "ROCC"
redActionMap[2][6] = "B+"
redActionMap[3][6] = "GD"
redActionMap[5][6] = "SED0"
redActionMap[8][5] = "GD"
redActionMap[9][5] = "ROCC"
redActionMap[9][6] = "GD"
redActionMap[8][7] = "OUTY"

blueArrowMap[4][2] = "L"
blueArrowMap[0][2] = "U"
blueArrowMap[0][7] = "R"
blueArrowMap[1][7] = "D"
blueArrowMap[1][1] = "R"
blueArrowMap[2][1] = "U"
blueArrowMap[2][6] = "R"
blueArrowMap[4][6] = "D"

blueActionMap[5][2] = "SL"
blueActionMap[4][2] = "INB"
blueActionMap[1][2] = "GD"
blueActionMap[0][6] = "DR"
blueActionMap[1][4] = "INB"
blueActionMap[1][1] = "SY"
blueActionMap[2][6] = "DR"
blueActionMap[3][6] = "B+"
blueActionMap[4][6] = "SY"

#Input A
a = atom.Atom("C",False)
a.setLocation(1,6)

#Input B
b = atom.Atom("H",False)
b.setLocation(1,2)

#Output Y
aa = atom.Atom("H",False)
bb = atom.Atom("H",False)
cc = atom.Atom("C",False)

aa.bindWith(cc,"L")
bb.bindWith(cc,"R")

dd = copy.deepcopy(cc)
ee = copy.deepcopy(cc)
ff = copy.deepcopy(cc)
gg = copy.deepcopy(cc)
hh = copy.deepcopy(cc)

dd.bindWith(cc,"U")
ee.bindWith(dd,"U")
ff.bindWith(ee,"U")
gg.bindWith(ff,"U")
hh.bindWith(gg,"U")

r.setMolecule("A",a)
r.setMolecule("B",b)
r.setMolecule("Y",aa)

r.setGoal("Y",10)

r.setArrowMapBlue(blueArrowMap)
r.setActionMapBlue(blueActionMap)
r.setArrowMapRed(redArrowMap)
r.setActionMapRed(redActionMap)

r.setBonders([[0,6],[1,6],[2,6],[3,6]])
r.setSensor([8,6])
r.setSenseList(["C"])
r.activateDoubleOutput()

for i in range(1,2000):
	if(r.doCycle(i)):
		print("Reactor has crash")
		quit()
	if(r.isFinished()):
		print("Reactor has completed is goal in " +  str(i) + " cycles")
		quit()
