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
redArrowMap[4][0] = "U"
redArrowMap[4][7] = "L"
redArrowMap[2][7] = "D"
redArrowMap[2][5] = "R"
redArrowMap[3][5] = "U"
redArrowMap[3][6] = "L"
redArrowMap[1][6] = "D"
redArrowMap[1][4] = "R"
redArrowMap[7][4] = "U"
redArrowMap[7][5] = "R"
redArrowMap[8][5] = "D"
redArrowMap[8][0] = "L"

redActionMap[4][0] = "SU"
redActionMap[4][1] = "SY"
redActionMap[4][4] = "GR"
redActionMap[4][5] = "ROCC"
redActionMap[4][6] = "INA"
redActionMap[2][6] = "B+"
redActionMap[2][5] = "ROCC"
redActionMap[3][5] = "INA"
redActionMap[7][5] = "DR"
redActionMap[8][4] = "OUTY"
redActionMap[5][0] = "SY"

blueArrowMap[1][0] = "U"
blueArrowMap[1][3] = "L"
blueArrowMap[0][3] = "U"
blueArrowMap[0][7] = "R"
blueArrowMap[2][7] = "D"
blueArrowMap[2][5] = "R"
blueArrowMap[3][5] = "U"
blueArrowMap[3][6] = "L"
blueArrowMap[1][6] = "D"
blueArrowMap[1][4] = "R"
blueArrowMap[7][4] = "D"
blueArrowMap[7][0] = "L"

blueActionMap[1][0] = "SU"
blueActionMap[1][1] = "INB"
blueActionMap[1][2] = "GR"
blueActionMap[1][7] = "INA"
blueActionMap[2][6] = "B+"
blueActionMap[2][5] = "ROCC"
blueActionMap[3][5] = "INA"
blueActionMap[4][4] = "DR"
blueActionMap[5][4] = "SY"
blueActionMap[2][0] = "SY"

#Input A
a = atom.Atom("H",False)
a.setLocation(1,6)

#Input B
b = atom.Atom("C",False)
b.setLocation(1,2)

#Output Y
aa = atom.Atom("H",False)
bb = atom.Atom("H",False)
cc = atom.Atom("H",False)
dd = atom.Atom("H",False)
ee = atom.Atom("C",False)

aa.bindWith(ee,"D")
bb.bindWith(ee,"U")
cc.bindWith(ee,"L")
dd.bindWith(ee,"R")

r.setMolecule("A",a)
r.setMolecule("B",b)
r.setMolecule("Y",aa)

r.setGoal("Y",10)

r.setArrowMapBlue(blueArrowMap)
r.setActionMapBlue(blueActionMap)
r.setArrowMapRed(redArrowMap)
r.setActionMapRed(redActionMap)

r.setBonders([[1,6],[2,6]])

for i in range(1,1000):
	if(r.doCycle(i)):
		print("Reactor has crash")
		quit()
	if(r.isFinished()):
		print("Reactor has completed is goal in " +  str(i) + " cycles")
		quit()
