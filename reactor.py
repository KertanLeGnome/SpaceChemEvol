import waldo
import atom
import copy
import collections

class Reactor:
	
	def __init__(self):
		self.blueWaldo = waldo.Waldo("Blue", self)
		self.redWaldo = waldo.Waldo("Red", self)
		self.atomlist = []
		self.atomMap = 0
		self.moleculeA = 0
		self.moleculeB = 0
		self.moleculeY = 0
		self.moleculeW = 0
		self.verbose = False
		self.goalY = 0 
		self.goalW = 0
		self.doneY = 0
		self.doneW = 0
		self.bonders = []
		self.sensor = []
		self.splitter = []
		self.fuser = []
		self.tunnel=[]

	def setBonders(self, bonders):
		self.bonders = bonders

	def setFuser(self, fuser):
		self.fuser = fuser

	def setSplitter(self, splitter):
		self.splitter = splitter

	def setTunnel(self, tunnels):
		self.tunnel = tunnels


	def setSensor(self, sensor):
		self.sensor = sensor

	def setVerbose(self,verbose):
		self.verbose = verbose
		self.blueWaldo.setVerbose(verbose)
		self.redWaldo.setVerbose(verbose)

	def setGoal(self, location, goal):
		if(location == "Y"):
			self.goalY = goal
		elif(location == "W"):
			self.goalW = goal

	def isFinished(self):
		return (self.doneY >= self.goalY and self.doneW >= self.goalW)

	def setArrowMapBlue(self, map):
		return self.blueWaldo.setArrowMap(map)

	def setActionMapBlue(self, map):
		return self.blueWaldo.setActionMap(map)
	
	def setArrowMapRed(self, map):
		return self.redWaldo.setArrowMap(map)
	
	def setActionMapRed(self, map):
		return self.redWaldo.setActionMap(map)

	def doCycle(self, cycle):
		if(self.verbose):
			print("Cycle : "+ str(cycle))
		for i in range(0,10):
			redOut = self.redWaldo.move(cycle+(i/10.0))
			blueOut = self.blueWaldo.move(cycle+(i/10.0))
			if(redOut or blueOut or self.checkCollision(i==9)):
				return True
		self.redWaldo.setDirection()
		self.blueWaldo.setDirection()
		redOut = self.redWaldo.doAction(cycle)
		if(self.checkCollision(True)):
			return True
		blueOut = self.blueWaldo.doAction(cycle)
		if(redOut or blueOut or self.checkCollision(True)):
			return True
		self.redWaldo.printState()
		self.blueWaldo.printState()
		if(self.verbose):
			self.printAtoms()


	def checkCollision(self, isSecondHalf):
		if(isSecondHalf):
			atomMap = [["E" for Y in range(0,8)] for X in range(0,10)]
		else:
			return self.checkCollisionWithDistance()
		for atom in self.atomlist:
			atom.roundLocation()
			if(atomMap[int(atom.X)][int(atom.Y)] == "E"):
				atomMap[int(atom.X)][int(atom.Y)] = atom
			else:
				#Two atoms are at the same location
				return True
		self.atomMap = atomMap
		return False

	def generateAtomMap(self):
		self.atomMap = [["E" for Y in range(0,8)] for X in range(0,10)]
		for atom in self.atomlist:
			self.atomMap[int(atom.X)][int(atom.Y)] = atom

	def checkCollisionWithDistance(self):
		tempAtomList = copy.copy(self.atomlist)
		for atom in tempAtomList:
			tempAtomList.remove(atom)
			for otherAtom in tempAtomList:
				collision = atom.checkCollisionWithDistance(otherAtom)
				if(collision):
					return True
		return False

	def hasAtomAtLocation(self,x,y):
		if(self.atomMap[x][y] == "E"):
			return False
		return True

	def getAtomAtLocation(self,x,y):
		return self.atomMap[x][y]

	def setMolecule(self,location,molecule):
		if(location == "A"):
			self.moleculeA = molecule
		elif(location == "B"):
			self.moleculeB = molecule
		elif(location == "Y"):
			self.moleculeY = molecule.getHash(0,"Special")
		elif(location == "W"):
			self.moleculeW = molecule.getHash(0,"Special")

	def output(self,location,cycle,waldo):
		returnValue = False
		if(location == "Y"):
			rangeY = range(4,8)
		elif(location == "W"):
			rangeY = range(0,4)

		for x in range(6,10):
			for y in rangeY:
				if(self.atomMap[x][y] != "E"):
					atomToOutput = self.atomMap[x][y]
					if(atomToOutput.isOutputable(location, cycle, waldo)):
						returnValue = returnValue or self.outputAtom(atomToOutput,location, cycle, waldo)
						self.generateAtomMap()
		return returnValue

	def outputAtom(self,atom,location,cycle,waldo):
		if(location == "Y"):
			hashToCompare = self.moleculeY
		elif(location == "W"):
			hashToCompare = self.moleculeW
		atomToRemove = atom.returnAllAtoms(cycle,waldo)
		hashMol = atom.getHash(cycle,waldo)
		for atoms in atomToRemove:
			self.atomlist.remove(atoms)
		if(collections.Counter(hashMol) == collections.Counter(hashToCompare)):
			if(location == "Y"):
				self.doneY = self.doneY + 1
			elif(location == "W"):
				self.doneW = self.doneW + 1
			return False
		else:
			return True

	def addBond(self):
		tempBondList = copy.copy(self.bonders)
		for bonder in tempBondList:
			tempBondList.remove(bonder)
			for otherBonder in tempBondList:
				direction = self.getBonderDirection(bonder,otherBonder)
				if(direction != "Undef"):
					atom = self.atomMap[bonder[0]][bonder[1]]
					otherAtom = self.atomMap[otherBonder[0]][otherBonder[1]]
					if( atom != "E" and otherAtom != "E"):
						atom.bindWith(otherAtom,direction)

	def removeBond(self):
		tempBondList = copy.copy(self.bonders)
		for bonder in tempBondList:
			tempBondList.remove(bonder)
			for otherBonder in tempBondList:
				direction = self.getBonderDirection(bonder,otherBonder)
				if(direction != "Undef"):
					atom = self.atomMap[bonder[0]][bonder[1]]
					otherAtom = self.atomMap[otherBonder[0]][otherBonder[1]]
					if( atom != "E" and otherAtom != "E"):
						atom.removeBind(otherAtom,direction)

	def getBonderDirection(self, bonder, otherBonder):
		if(bonder[0] == otherBonder[0] and bonder[1] + 1 == otherBonder[1]):
			return "U"
		elif(bonder[0] == otherBonder[0] and bonder[1] == otherBonder[1] + 1):
			return "D"
		elif(bonder[0] == otherBonder[0] + 1 and bonder[1] == otherBonder[1]):
			return "L"
		elif(bonder[0] + 1 == otherBonder[0] and bonder[1] == otherBonder[1]):
			return "R"
		#Both bonders are not adjacent
		return "Undef"

	def getSymAtomAtSensor(self):
		if(len(self.sensor) == 2):
			atom = self.atomMap[self.sensor[0]][self.sensor[1]]
			return atom.getSymbol()

	def input(self,location, cycle, waldo):
		if(location == "A"):
			mol = copy.deepcopy(self.moleculeA)
		else:
			mol = copy.deepcopy(self.moleculeB)
		for i in mol.returnAllAtoms(cycle, waldo):
			self.atomlist.append(i)

	def sync(self, waldo):
		if(waldo == "Blue"): #Return true if the other one is not waiting for sync
			return not self.redWaldo.sync()
		elif(waldo == "Red"):
			return not self.blueWaldo.sync()

	def fuse(self):
		if(len(self.fuser) == 2):
			target = self.atomMap[self.fuser[0]][self.fuser[1]]
			toFuse = self.atomMap[self.fuser[0]-1][self.fuser[1]]
			if(target != "E" and toFuse != "E"):
				self.atomlist.remove(toFuse)
				return target.fuse(toFuse)

	def swap(self):
		if(len(self.tunnel) == 2):
			atom = atomMap[self.tunnel[0][0]][self.tunnel[0][1]]
			otherAtom = atomMap[self.tunnel[1][0]][self.tunnel[1][1]]
			if(atom != "E" and otherAtom != "E"):
				atom.swapWith(otherAtom)
			elif(atom == "E" and otherAtom != "E"):
				otherAtom.swapTo(self.tunnel[0][0],self.tunnel[0][1])
			elif(atom != "E" and otherAtom == "E"):
				atom.swapTo(self.tunnel[1][0],self.tunnel[1][1])
			else:
				return False

	def split(self):
		if(len(self.splitter == 2)):
			target = self.atomMap[self.fuser[0]][self.fuser[1]]
			if(target != "E"):
				if(self.atomMap[self.fuser[0]+1][self.fuser[1]] == "E"):
					newAtom = target.split()
					if(newAtom != False):
						self.atomlist.append(newAtom)
				else:
					return True

	def printAtoms(self):
		for i in self.atomlist:
			i.printState()