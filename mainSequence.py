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
redArrowMap[1][6] = "D"
redArrowMap[1][4] = "R"
redArrowMap[6][4] = "U"
redArrowMap[7][5] = "U"
redArrowMap[6][6] = "L"
redArrowMap[7][6] = "L"

redActionMap[4][6] = "SL"
redActionMap[2][6] = "INA"
redActionMap[1][6] = "GR"
redActionMap[1][5] = "SER0"
redActionMap[1][4] = "GD"
redActionMap[2][4] = "SY"
redActionMap[6][6] = "OUTY"
redActionMap[7][6] = "GD"

blueArrowMap[1][7] = "D"
blueArrowMap[1][3] = "R"
blueArrowMap[2][3] = "U"
blueArrowMap[2][6] = "R"
blueArrowMap[7][6] = "U"
blueArrowMap[7][7] = "L"

blueActionMap[4][7] = "SL"
blueActionMap[3][7] = "SY"
blueActionMap[1][4] = "GD"
blueActionMap[1][3] = "SY"
blueActionMap[2][4] = "B+"
blueActionMap[2][6] = "B+"
blueActionMap[7][6] = "GD"
blueActionMap[6][7] = "OUTY"

a = atom.Atom("H",False)
a.setLocation(1,6)
b = atom.Atom("H",False)
b.setLocation(1,6)
bb = atom.Atom("H",False)
bb.setLocation(2,6)
b.bindWith(bb,"R")

r.addMolecule("A",a)
r.addMolecule("A",b)

r.setMolecule("Y",copy.deepcopy(b))

r.setSequence("A", [1,1,1,0,0,0,1,0,1,0,0,1,1,0,1,0,1,0,1,0,1,1,0,0,1,0,1])
r.setGoal("Y",20)

r.setArrowMapBlue(blueArrowMap)
r.setActionMapBlue(blueActionMap)
r.setArrowMapRed(redArrowMap)
r.setActionMapRed(redActionMap)

r.setBonders([[1,4],[2,4]])
r.setSensor([2,5])
r.setSenseList(["H"])

for i in range(1,1000):
	if(r.doCycle(i)):
		print("Reactor has crash")
		quit()
	if(r.isFinished()):
		print("Reactor has completed is goal in " +  str(i) + " cycles")
		quit()
