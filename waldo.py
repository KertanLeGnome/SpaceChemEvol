import reactor
import atom

class Waldo:
	
	def __init__(self, name, reactor):
		self.reactor = reactor
		self.hasAtom = False
		self.atom = 0
		self.X = 0
		self.Y = 0
		self.direction = "Undef"
		self.actionMap = []
		self.arrowMap =[]
		self.name = name
		self.verbose = False
		self.isWaitingForSync = False
		self.senseList = []
		self.justWakeUp = False
		self.isRotating = False
		self.rotationDir = 0

	def setSenseList(self,senseList):
		self.senseList = senseList

	def setVerbose(self, verbose):
		self.verbose = verbose

	def setActionMap(self,actionMap):
		self.actionMap = actionMap
		for x in range(0,10):
			for y in range(0,8):
				if(actionMap[x][y] == "SU"):
					self.setStart(x,y,"U")
					return True
				elif(actionMap[x][y] == "SD"):
					self.setStart(x,y,"D")
					return True
				elif(actionMap[x][y] == "SL"):
					self.setStart(x,y,"L")
					return True
				elif(actionMap[x][y] == "SR"):
					self.setStart(x,y,"R")
					return True
		return False

	def setArrowMap(self,arrowMap):
		self.arrowMap = arrowMap
		return True

	def setStart(self,x,y,direction):
		self.X = x
		self.Y = y
		self.direction = direction

	def sync(self):
		if(self.isWaitingForSync):
			self.isWaitingForSync = not self.isWaitingForSync
			self.justWakeUp = True
			return True
		return False

	def move(self, cycle):
		self.justWakeUp = False
		returnValue = False
		if(not self.isWaitingForSync and not self.isRotating):
			returnValue = self.setNewLocation(cycle)
		elif(self.isRotating):
			if(self.hasAtom):
				if(cycle % 1.0 == 0):
					returnValue = self.atom.startRotate(self.rotationDir, cycle, self.name)
				returnValue = returnValue or self.atom.rotate(self.rotationDir,cycle, self.name)
		return returnValue

	def setDirection(self):
		self.X = int(round(self.X))
		self.Y = int(round(self.Y))
		if(self.arrowMap[self.X][self.Y] != "E"):
			self.direction = self.arrowMap[self.X][self.Y]

	def setNewLocation(self, cycle):
		if(self.direction == "L"):
			if(self.X != 0):
				self.X = self.X - 0.1 
		elif(self.direction == "R"):
			if(self.X != 9):
				self.X = self.X + 0.1 
		elif(self.direction == "U"):
			if(self.Y != 7):
				self.Y = self.Y + 0.1 
		elif(self.direction == "D"):
			if(self.Y != 0):
				self.Y = self.Y - 0.1
		if(self.hasAtom):
			return self.atom.setNewLocation(self.direction, cycle, self.name)
		return False

	def printState(self):
		if(self.verbose):
			print(self.name + " waldo, pos x: " + str(self.X) + " , pos y: " + str(self.Y) + " , direction : " + self.direction + ", has atom : " + str(self.hasAtom))

	def doAction(self, cycle):
		action = self.actionMap[self.X][self.Y]
		if(self.isRotating):
			self.isRotating = False
			return False
		if(self.verbose):
			print(self.name + " waldo, action : " + action)
		if(action == "INA"):
			return self.reactor.input("A", cycle, self.name)
		elif(action == "INB"):
			return self.reactor.input("B", cycle, self.name)
		elif(action == "OUTY"):
			return self.reactor.output("Y", cycle, self.name)
		elif(action == "OUTW"):
			return self.reactor.output("W", cycle, self.name)
		elif(action == "INB"):
			return self.reactor.output("W", cycle, self.name)
		elif(action == "GR"):
			return self.grab()
		elif(action == "GD"):
			if(self.hasAtom):
				return self.drop()
			else:
				return self.grab()
		elif(action == "DR"):
			return self.drop()
		elif(action == "B+"):
			return self.reactor.addBond()
		elif(action == "B-"):
			return self.reactor.removeBond()
		elif(action == "SY"):
			if(not self.isWaitingForSync and not self.justWakeUp):
				if(self.reactor.sync(self.name)): #if the other one is not waiting, then you have to wait
					self.isWaitingForSync = True
			return False
		elif(action == "SW"):
			return self.reactor.swap()
		elif(action == "FU"):
			self.reactor.fuse()
		elif(action == "SP"):
			self.reactor.split()
		elif(action == "ROCC"):
			self.isRotating = True
			self.rotationDir = 0
		elif(action == "ROC"):
			self.isRotating = True
			self.rotationDir = 1
		elif(action.startswith("SE")):
			self.sense(action[2], action[3])
		elif(action.startswith("FL")):
			self.flipflop(action[2], action[3])

	def flipflop(self, direction, isActivate):
		if(isActivate == "0"):
			self.actionMap[self.X][self.Y] = "FL" + direction + "1"
		elif(isActivate == "1"):
			self.actionMap[self.X][self.Y] = "FL" + direction + "0"
			self.direction = direction

	def sense(self, direction, atomNumber):
		if(int(atomNumber) < len(self.senseList)):
			atomSym = self.reactor.getSymAtomAtSensor()
			if(atomSym == self.senseList[int(atomNumber)]):
				self.direction = direction

	def drop(self):
		if(not self.hasAtom):
			return False
		self.hasAtom = False
		self.atom.dropAtom()
		self.atom = 0 

	def grab(self):
		if(self.hasAtom):
			return False
		if(self.reactor.hasAtomAtLocation(self.X,self.Y)):
			self.atom = self.reactor.getAtomAtLocation(self.X,self.Y)
			self.hasAtom = True
			return self.atom.grabAtom(self)