import json
import reactor
import hashlib
import math

class Atom:
	
	symboleDataFile = open('symboleData.json')
	symboleData = json.load(symboleDataFile)
	symboleDataFile.close()
	numberSymbole = ["H","HE","LI","BE","B","C","N","O","F","NE","NA","MG","AL","SI","P","S","CL","AR","K","CA","SC","TI","V","CR","MN","FE","CO","NI","CU","ZN",
	"GA","GE","AS","SE","BR","KR","RB","SR","Y","ZR","NB","MO","TC","RU","RH","PD","AG","CD","IN","SN","SB","TE","I","XE","CS","BA","LA","CE","PR","ND","PM","SM",
	"EU","GD","TB","DY","HO","ER","TM","YB","LU","HF","TA","W","RE","OS","IR","PT","AU","HG","TL","PB","BI","PO","AT","RN","FR","RA","AC","TH","PA","U","NP","PU",
	"AM","CM","BK","CF","ES","FM","MD","NO","LR","RF","DB","SG","BH","HS","MT"]
	radius = 0.36

	def __init__(self, symbole,isNumberInsteadOfSymbol):
		self.sym = symbole
		if(isNumberInsteadOfSymbol):
			self.sym = Atom.numberSymbole[symbole-1]
		self.number = Atom.symboleData[self.sym]["AN"]
		self.maxLink = Atom.symboleData[self.sym]["ML"] 
		self.left = 0
		self.right = 0
		self.up = 0
		self.down = 0 
		self.X = 0
		self.Y = 0
		self.leftLink = 0
		self.rightLink = 0
		self.upLink = 0
		self.downLink = 0
		self.direction = "U"
		self.lastMoveCycle = 0
		self.lastMoveWaldo = ""
		self.lastMoveDirection = "E"
		self.isGrabbed = False
		self.waldo = 0
		self.lastActionCycle = 0
		self.lastActionWaldo = 0
		self.lastHashCycle = 0
		self.lastHashWaldo = 0
		self.lastOutputableCheckCycle = 0
		self.lastOutputableCheckWaldo = 0

	def getSymbole(self):
		return self.sym

	def setLocation(self,x,y):
		self.X = x
		self.Y = y

	def grabAtom(self, waldo):
		if(self.isGrabbed):
			return True
		else:
			self.isGrabbed = True
			self.waldo = waldo
			return False

	def dropAtom(self):
		self.isGrabbed = False
		self.waldo = 0

	def setNewLocation(self,direction, cycle, waldo):
		if(self.lastMoveCycle == cycle):
			#If moved twice the same turn and waldo due to a loop in bond
			if(self.lastMoveWaldo == waldo): 
				return False
			#If moved by the other waldo	
			else:
				#Is ok if both waldo moved it in the same direction
				if(self.lastMoveDirection == direction):
					return False
				#Byt if they didn't, it should crash the reactor
				else:
					return True
		self.lastMoveDirection = direction
		self.lastMoveWaldo = waldo
		self.lastMoveCycle = cycle
		if(direction == "L"):
			if(self.X != 0):
				self.X = self.X - 0.1
			else:
				return True
		elif(direction == "R"):
			if(self.X != 9):
				self.X = self.X + 0.1
			else:
				return True
		elif(direction == "U"):
			if(self.Y != 7):
				self.Y = self.Y + 0.1
			else:
				return True
		elif(direction == "D"):
			if(self.Y != 0):
				self.Y = self.Y - 0.1
			else:
				return True
		leftReturn = False
		rightReturn = False
		upReturn = False
		downReturn = False
		if(self.leftLink != 0):
			leftReturn = self.left.setNewLocation(direction,cycle,waldo)
		if(self.rightLink != 0):
			rightReturn = self.right.setNewLocation(direction,cycle,waldo)
		if(self.upLink != 0):
			upReturn = self.up.setNewLocation(direction,cycle,waldo)
		if(self.downLink != 0):
			downReturn = self.down.setNewLocation(direction,cycle,waldo)
		return (leftReturn or rightReturn or upReturn or downReturn)

	def roundLocation(self):
		self.X = int(round(self.X))
		self.Y = int(round(self.Y))

	def startRotate(self, direction, cycle, waldo):
		if(self.lastActionCycle == cycle and self.lastActionWaldo == waldo): #Already in the list
			return False
		self.lastActionWaldo = waldo
		self.lastActionCycle = cycle
		if(direction == 0):
			if(self.direction == "L"):
				self.direction = "D"
			elif(self.direction == "R"):
				self.direction = "U"
			elif(self.direction == "U"):
				self.direction = "L"
			elif(self.direction == "D"):
				self.direction = "R"
		if(direction == 1):
			if(self.direction == "L"):
				self.direction = "U"
			elif(self.direction == "R"):
				self.direction = "D"
			elif(self.direction == "U"):
				self.direction = "R"
			elif(self.direction == "D"):
				self.direction = "L"
		if(self.leftLink != 0):
			self.left.startRotate(direction,cycle,waldo)
		if(self.rightLink != 0):
			self.right.startRotate(direction,cycle,waldo)
		if(self.upLink != 0):
			self.up.startRotate(direction,cycle,waldo)
		if(self.downLink != 0):
			self.down.startRotate(direction,cycle,waldo)
		return False


	def rotate(self,direction,cycle,waldo):
		if(self.lastMoveCycle == cycle):
			#If moved twice the same turn and waldo due to a loop in bond
			if(self.lastMoveWaldo == waldo): 
				return False
			#If moved by the other waldo	
			else:
				return True
		self.lastMoveWaldo = waldo
		self.lastMoveCycle = cycle

		#Since it's the pivot, it does not move
		leftReturn = False
		rightReturn = False
		upReturn = False
		downReturn = False
		if(self.leftLink != 0):
			leftReturn = self.left.rotateAroundAtom(direction,self,cycle,waldo)
		if(self.rightLink != 0):
			rightReturn = self.right.rotateAroundAtom(direction,self,cycle,waldo)
		if(self.upLink != 0):
			upReturn = self.up.rotateAroundAtom(direction,self,cycle,waldo)
		if(self.downLink != 0):
			downReturn = self.down.rotateAroundAtom(direction,self,cycle,waldo)
		return (leftReturn or rightReturn or upReturn or downReturn)


	def rotateAroundAtom(self,direction, pivot, cycle,waldo):
		if(self.lastMoveCycle == cycle):
			#If moved twice the same turn and waldo due to a loop in bond
			if(self.lastMoveWaldo == waldo): 
				return False
			#If moved by the other waldo	
			else:
				return True
		self.lastMoveWaldo = waldo
		self.lastMoveCycle = cycle

		self.doRotation(direction,pivot)

		leftReturn = False
		rightReturn = False
		upReturn = False
		downReturn = False
		if(self.leftLink != 0):
			leftReturn = self.left.rotateAroundAtom(direction,pivot,cycle,waldo)
		if(self.rightLink != 0):
			rightReturn = self.right.rotateAroundAtom(direction,pivot,cycle,waldo)
		if(self.upLink != 0):
			upReturn = self.up.rotateAroundAtom(direction,pivot,cycle,waldo)
		if(self.downLink != 0):
			downReturn = self.down.rotateAroundAtom(direction,pivot,cycle,waldo)
		return (leftReturn or rightReturn or upReturn or downReturn)

	def doRotation(self,direction,pivot):
		factor = 1
		if(direction == 1):
			factor = -1
		s = math.sin(factor*math.pi/20)
		c = math.cos(factor*math.pi/20)

		oldX = self.X - pivot.X
		oldY = self.Y - pivot.Y

		newX = oldX * c - oldY * s
		newY = oldX * s + oldY * c

		self.X = newX + pivot.X
		self.Y = newY + pivot.Y



	def returnAllAtoms(self, cycle, waldo):
		if(self.lastActionCycle == cycle and self.lastActionWaldo == waldo): #Already in the list
			return []
		self.lastActionWaldo = waldo
		self.lastActionCycle = cycle
		listAtoms = [self]
		if(self.leftLink != 0):
			listAtoms.extend(self.left.returnAllAtoms(cycle,waldo))
		if(self.rightLink != 0):
			listAtoms.extend(self.right.returnAllAtoms(cycle,waldo))
		if(self.upLink != 0):
			listAtoms.extend(self.up.returnAllAtoms(cycle,waldo))
		if(self.downLink != 0):
			listAtoms.extend(self.down.returnAllAtoms(cycle,waldo))
		return listAtoms
		
	def bindWith(self, otherAtom, direction):
		if(direction == "L"):
			otherAtomDirection = "R"
		elif(direction == "R"):
			otherAtomDirection = "L"
		elif(direction == "U"):
			otherAtomDirection = "D"
		elif(direction == "D"):
			otherAtomDirection = "U"
		otherAtomDirection = otherAtom.getTrueDirection(otherAtomDirection)
		direction = self.getTrueDirection(direction)
		if(self.canAddLink(direction) and otherAtom.canAddLink(otherAtomDirection)):
			self.addLink(direction,otherAtom)
			otherAtom.addLink(otherAtomDirection,self)
		return

	def removeBind(self, otherAtom, direction):
		if(direction == "L"):
			otherAtomDirection = "R"
		elif(direction == "R"):
			otherAtomDirection = "L"
		elif(direction == "U"):
			otherAtomDirection = "D"
		elif(direction == "D"):
			otherAtomDirection = "U"
		otherAtomDirection = otherAtom.getTrueDirection(otherAtomDirection)
		direction = self.getTrueDirection(direction)
		self.removeLink(direction,otherAtom)
		otherAtom.removeLink(otherAtomDirection,self)
		return

	def removeLink(self, direction, otherAtom):
		if(direction == "U" and self.up == otherAtom):
			self.upLink = self.upLink - 1
			if(self.upLink == 0):
				self.up = 0
		elif(direction == "D" and self.down == otherAtom):
			self.downLink = self.downLink - 1
			if(self.downLink == 0):
				self.down = 0
		elif(direction == "L" and self.left == otherAtom):
			self.leftLink = self.leftLink - 1
			if(self.leftLink == 0):
				self.left = 0
		elif(direction == "R" and self.right == otherAtom):
			self.rightLink = self.rightLink - 1
			if(self.rightLink == 0):
				self.right = 0

	def fuse(self, otherAtom):
		otherNb = otherAtom.number
		self.number = self.number + otherNb
		if(self.number > len(Atom.numberSymbole)):
			return True
		self.sym = Atom.numberSymbole[self.number-1]
		otherAtom.remove()
		newMaxLink = Atom.symboleData[self.sym]["ML"] 
		if(newMaxLink < self.maxLink):
			self.removeOverLink(self.upLink+self.downLink+self.leftLink+self.rightLink - newMaxLink)
		self.maxLink = newMaxLink

	def removeOverLink(self, linkToRemove):
		if(linkToRemove < 1):
			return
		linkRemoved = 0
		for i in range(3,0,-1):
			if(self.upLink == i):
				self.up.removeOneLinkWithAtom(self)
				linkRemoved = linkRemoved + 1
				if(i == 1):
					self.up = 0 
			if(linkRemoved == linkToRemove):
				return
			if(self.downLink == i):
				self.down.removeOneLinkWithAtom(self)
				linkRemoved = linkRemoved + 1
				if(i == 1):
					self.down = 0 
			if(linkRemoved == linkToRemove):
				return
			if(self.leftLink == i):
				self.left.removeOneLinkWithAtom(self)
				linkRemoved = linkRemoved + 1
				if(i == 1):
					self.left = 0 
			if(linkRemoved == linkToRemove):
				return
			if(self.rightLink == i):
				self.right.removeOneLinkWithAtom(self)
				linkRemoved = linkRemoved + 1
				if(i == 1):
					self.right = 0 
			if(linkRemoved == linkToRemove):
				return

	def swapWith(self, otherAtom):
		self.remove()
		otherAtom.remove()
		newX = otherAtom.X
		newY = otherAtom.Y
		otherAtom.X = self.X
		otherAtom.Y = self.Y
		self.X = newX
		self.Y = newY

	def swapTo(self, newX, newY):
		self.remove()
		self.X = newX
		self.Y = newY

	def remove(self):
		if(self.upLink != 0):
			self.up.removeLinkWithAtom(self)
		if(self.downLink != 0):
			self.down.removeLinkWithAtom(self)
		if(self.leftLink != 0):
			self.left.removeLinkWithAtom(self)
		if(self.rightLink != 0):
			self.right.removeLinkWithAtom(self)

	def removeLinkWithAtom(self, otherAtom):
		if(self.up == otherAtom):
			self.up = 0
			self.upLink = 0
		elif(self.down == otherAtom):
			self.down = 0
			self.downLink = 0
		elif(self.left == otherAtom):
			self.left = 0
			self.leftLink = 0
		elif(self.right == otherAtom):
			self.right = 0
			self.rightLink = 0

	def removeOneLinkWithAtom(self, otherAtom):
		if(self.up == otherAtom):
			self.upLink = self.upLink - 1
			if(self.upLink == 0):
				self.up = 0
		elif(self.down == otherAtom):
			self.downLink = self.downLink - 1
			if(self.downLink == 0):
				self.down = 0
		elif(self.left == otherAtom):
			self.leftLink = self.leftLink - 1
			if(self.leftLink == 0):
				self.left = 0
		elif(self.right == otherAtom):
			self.rightLink = self.rightLink - 1
			if(self.rightLink == 0):
				self.right = 0

	def split(self):
		newNb = self.number / 2.0
		otherNb = math.floor(newNb)
		newNb = math.ceil(newNb)
		if(otherNb != 0):
			self.number = self.newNb
			self.sym = Atom.numberSymbole[newNb-1]
			newMaxLink = Atom.symboleData[self.sym]["ML"] 
			if(newMaxLink < self.maxLink):
				self.removeOverLink(self.maxLink - newMaxLink)
			self.maxLink = newMaxLink
			newAtom = Atom(otherNb,True)
			newAtom.setLocation(self.X + 1, self.Y)
			return newAtom 
		else:
			return False

	def addLink(self,direction, otherAtom):
		if(direction == "U"):
			self.upLink = self.upLink + 1
			self.up = otherAtom
		elif(direction == "D"):
			self.downLink = self.downLink + 1
			self.down = otherAtom
		elif(direction == "L"):
			self.leftLink = self.leftLink + 1
			self.left = otherAtom
		elif(direction == "R"):
			self.rightLink = self.rightLink + 1
			self.right = otherAtom

	def canAddLink(self,direction):
		if(self.leftLink + self.rightLink + self.upLink + self.downLink < self.maxLink):
			if(direction == "U" and self.upLink < 3):
				return True
			elif(direction == "D" and self.downLink < 3):
				return True
			elif(direction == "L" and self.leftLink < 3):
				return True
			elif(direction == "R" and self.rightLink < 3):
				return True
		return False

	def getTrueDirection(self,direction):
		if(self.direction == "U"):
			return direction
		elif(self.direction == "L"):
			if(direction == "L"):
				return "U"
			elif(direction == "R"):
				return "D"
			elif(direction == "U"):
				return "R"
			elif(direction == "D"):
				return "L"
		elif(self.direction == "R"):
			if(direction == "L"):
				return "D"
			elif(direction == "R"):
				return "U"
			elif(direction == "U"):
				return "L"
			elif(direction == "D"):
				return "R"
		elif(self.direction == "D"):
			if(direction == "L"):
				return "R"
			elif(direction == "R"):
				return "L"
			elif(direction == "U"):
				return "D"
			elif(direction == "D"):
				return "U"

	def checkCollisionWithDistance(self, otherAtom):
		distance = ((self.X - otherAtom.X)**2 + (self.Y - otherAtom.Y)**2)**(1/2)
		if(distance < 2*Atom.radius):
			return True
		return False

	def getHash(self, cycle, waldo):
		if(self.lastHashCycle == cycle and self.lastHashWaldo == waldo): #Already in the list
			return []
		self.lastHashWaldo = waldo
		self.lastHashCycle = cycle
		hashList = [hashlib.md5(self.getAtomString().encode('UTF-8')).hexdigest()]
		if(self.leftLink != 0):
			hashList.extend(self.left.getHash(cycle,waldo))
		if(self.rightLink != 0):
			hashList.extend(self.right.getHash(cycle,waldo))
		if(self.upLink != 0):
			hashList.extend(self.up.getHash(cycle,waldo))
		if(self.downLink != 0):
			hashList.extend(self.down.getHash(cycle,waldo))
		return sorted(hashList)

	def getAtomString(self):
		AtomString = self.sym
		nbNeighbour = 0
		listNeighbour = []
		if(self.upLink != 0):
			nbNeighbour = nbNeighbour + 1
			listNeighbour.append(self.up.sym+str(self.upLink))
		else:
			listNeighbour.append("XX")
		if(self.downLink != 0):
			nbNeighbour = nbNeighbour + 1
			listNeighbour.append(self.down.sym+str(self.downLink))
		else:
			listNeighbour.append("XX")
		if(self.leftLink != 0):
			nbNeighbour = nbNeighbour + 1
			listNeighbour.append(self.left.sym+str(self.leftLink))
		else:
			listNeighbour.append("XX")
		if(self.rightLink != 0):
			nbNeighbour = nbNeighbour + 1
			listNeighbour.append(self.right.sym+str(self.rightLink))
		else:
			listNeighbour.append("XX")
		AtomString = AtomString + str(nbNeighbour)
		for strings in sorted(listNeighbour):
			AtomString =  AtomString + strings
		return AtomString

	def isOutputable(self,location, cycle, waldo, bigOutput, isFirst):
		if(self.lastOutputableCheckCycle == cycle and self.lastOutputableCheckWaldo == waldo): #Already in the list
			return not isFirst
		self.lastOutputableCheckWaldo = waldo
		self.lastOutputableCheckCycle = cycle
		returnValue = self.isInOutputLocation(location, bigOutput) and not self.isGrabbed
		if(self.leftLink != 0):
			if(not self.left.isOutputable(location,cycle,waldo, bigOutput, False)):
				returnValue = False
		if(self.rightLink != 0):
			if(not self.right.isOutputable(location,cycle,waldo, bigOutput,False)):
				returnValue = False
		if(self.upLink != 0):
			if(not self.up.isOutputable(location,cycle,waldo, bigOutput, False)):
				returnValue = False
		if(self.downLink != 0):
			if(not self.down.isOutputable(location,cycle,waldo, bigOutput, False)):
				returnValue = False
		return returnValue

	def isInOutputLocation(self,location, bigOutput):
		if(location == "Y"):
			if(not bigOutput):
				return (self.X > 5 and self.Y > 3)
			else:
				return (self.X > 5)
		elif(location == "W"):
			return (self.X > 5 and self.Y < 4)

	def printState(self):
		print("Atome symbole : " + self.sym + " pos x : " + str(self.X) + " pos y : " + str(self.Y) + " dir : " + self.direction + " link left : " + 
			str(self.leftLink) + " link right : " + str(self.rightLink) + " up link : " + str(self.upLink) + " down link : " + str(self.downLink) + " is grabbed : " + str(self.isGrabbed))