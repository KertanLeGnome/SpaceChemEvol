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
redArrowMap[2][6] = "L"
redArrowMap[1][6] = "D"
redArrowMap[1][4] = "R"
redArrowMap[2][4] = "U"

redActionMap[4][6] = "SL"
redActionMap[2][6] = "INA"
redActionMap[1][6] = "GR"
redActionMap[1][5] = "FU"
redActionMap[2][4] = "SY"
redActionMap[2][5] = "DR"

blueArrowMap[7][1] = "L"
blueArrowMap[2][1] = "U"
blueArrowMap[2][5] = "R"
blueArrowMap[7][5] = "D"

blueActionMap[7][3] = "SD"
blueActionMap[7][2] = "SY"
blueActionMap[7][1] = "SY"
blueActionMap[6][1] = "SY"
blueActionMap[5][1] = "SY"
blueActionMap[4][1] = "SY"
blueActionMap[3][1] = "SY"
blueActionMap[2][1] = "SY"
blueActionMap[2][2] = "SY"
blueActionMap[2][3] = "SY"
blueActionMap[2][4] = "SY"
blueActionMap[2][5] = "GR"
blueActionMap[6][5] = "DR"
blueActionMap[7][5] = "OUTY"

a = atom.Atom("H",False)
a.setLocation(1,6)
b = atom.Atom("NE",False)


r.setMolecule("A",a)
r.setMolecule("Y",b)

r.setGoal("Y",10)


r.setArrowMapBlue(blueArrowMap)
r.setActionMapBlue(blueActionMap)
r.setArrowMapRed(redArrowMap)
r.setActionMapRed(redActionMap)

r.setFuser([2,5])

for i in range(1,1000):
	if(r.doCycle(i)):
		print("Reactor has crash")
		quit()
	if(r.isFinished()):
		print("Reactor has completed is goal in " +  str(i) + " cycles")
		quit()
