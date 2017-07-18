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
redArrowMap[1][2] = "R"
redArrowMap[3][2] = "U"
redArrowMap[3][4] = "R"
redArrowMap[6][4] = "D"
redArrowMap[6][1] = "L"
redArrowMap[2][1] = "U"
redArrowMap[2][5] = "R"
redArrowMap[7][5] = "U"
redArrowMap[7][6] = "L"

redActionMap[4][6] = "SL"
redActionMap[3][6] = "INA"
redActionMap[1][6] = "GD"
redActionMap[1][4] = "B-"
redActionMap[1][3] = "SY"
redActionMap[1][2] = "SY"
redActionMap[3][4] = "B-"
redActionMap[5][4] = "SY"
redActionMap[6][4] = "SY"
redActionMap[2][4] = "B+"
redActionMap[7][6] = "GD"
redActionMap[6][6] = "OUTY"

blueArrowMap[3][1] = "U"
blueArrowMap[3][7] = "D"
blueArrowMap[2][3] = "U"
blueArrowMap[2][5] = "R"
blueArrowMap[7][5] = "D"
blueArrowMap[7][1] = "L"

blueActionMap[3][1] = "SU"
blueActionMap[3][2] = "SY"
blueActionMap[3][3] = "FLL0"
blueActionMap[3][4] = "GD"
blueActionMap[3][6] = "SY"
blueActionMap[3][7] = "SY"
blueActionMap[2][3] = "B+"
blueActionMap[2][4] = "GD"
blueActionMap[7][3] = "GD"
blueActionMap[7][1] = "OUTW"

#Input A
a = atom.Atom("H",False)
a.setLocation(0,6)
b = atom.Atom("H",False)
b.setLocation(1,7)
c = atom.Atom("H",False)
c.setLocation(1,5)
d = atom.Atom("H",False)
d.setLocation(2,7)
e = atom.Atom("H",False)
e.setLocation(2,5)
f = atom.Atom("H",False)
f.setLocation(3,6)
g = atom.Atom("C",False)
g.setLocation(1,6)
h = atom.Atom("C",False)
h.setLocation(2,6)

a.bindWith(g,"R")
b.bindWith(g,"D")
c.bindWith(g,"U")
d.bindWith(h,"D")
e.bindWith(h,"U")
f.bindWith(h,"L")
g.bindWith(h,"R")

#Output Y
aa = atom.Atom("H",False)
bb = atom.Atom("H",False)
cc = atom.Atom("H",False)
dd = atom.Atom("H",False)
ee = atom.Atom("C",False)
ff = atom.Atom("C",False)

aa.bindWith(ee,"D")
bb.bindWith(ee,"U")
cc.bindWith(ff,"D")
dd.bindWith(ff,"U")
ee.bindWith(ff,"R")
ee.bindWith(ff,"R")

#Output w

aaa = atom.Atom("H",False)
bbb = atom.Atom("H",False)

aaa.bindWith(bbb,"R")

r.setMolecule("A",a)

r.setMolecule("Y",aa)
r.setMolecule("W",aaa)

r.setGoal("Y",10)
r.setGoal("W",10)

r.setArrowMapBlue(blueArrowMap)
r.setActionMapBlue(blueActionMap)
r.setArrowMapRed(redArrowMap)
r.setActionMapRed(redActionMap)

r.setBonders([[2,4],[3,4]])

for i in range(1,1000):
	if(r.doCycle(i)):
		print("Reactor has crash")
		quit()
	if(r.isFinished()):
		print("Reactor has completed is goal in " +  str(i) + " cycles")
		quit()
