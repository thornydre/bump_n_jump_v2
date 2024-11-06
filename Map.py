#!/usr/bin/python

import pygame
import random
import json
from Object import Object


class Map():
	def __init__(self, empty=False):
		self.blocksList = []
		self.carrotsList = []
		self.objectSpritesList = pygame.sprite.Group()
		self.screen = pygame.display.get_surface()

		if not empty:
			self.generateMap()

		self.collideBlocksList = self.generateCollideBlocksList()


		for obj in self.blocksList:
			if not self.isFloor(obj):
				obj.replaceImage(obj.getType())
			self.objectSpritesList.add(obj)

		for obj in self.carrotsList:
			self.objectSpritesList.add(obj)


	def update(self):
		self.objectSpritesList.update()
		self.objectSpritesList.draw(self.screen)


	def updateFloor(self):
		for obj in self.blocksList:
			if not self.isFloor(obj):
				if obj.getType() == Object.BOUNCE:
					obj.replaceImage(Object.DIRT)
				else:
					obj.replaceImage(obj.getType())

			else:
				obj.replaceImage(obj.getType(), True)

			self.objectSpritesList.add(obj)


	def generateMap(self):
		for i in range(0, 16):
			objType = random.randint(1, 2)

			if objType == 1:
				self.blocksList.append(Object(i * 50, 550, Object.DIRT))
			elif objType == 2:
				self.blocksList.append(Object(i * 50, 550, Object.ICE))

		for k in range(0, 5):
			while True:
				randPos = random.randint(0, len(self.blocksList) - 1)
				if not self.isInBlock((self.blocksList[randPos].getX() + 10, self.blocksList[randPos].getY() - 26)):
					break

			if self.blocksList[randPos].getType():
				self.carrotsList.append(Object(self.blocksList[randPos].getX() + 10, self.blocksList[randPos].getY() - 26, Object.CARROT))


	def generateCollideBlocksList(self):
		collideList = []

		for obj in self.blocksList:
			if obj.getType() != Object.CARROT:
				if not self.isInBlock((obj.rect.left - 5, obj.rect.centery)):
					collideList.append(obj)
					continue
				if not self.isInBlock((obj.rect.centerx, obj.rect.top - 5)):
					collideList.append(obj)
					continue
				if not self.isInBlock((obj.rect.right + 5, obj.rect.centery)):
					collideList.append(obj)
					continue
				if not self.isInBlock((obj.rect.centerx, obj.rect.bottom + 5)):
					collideList.append(obj)
					continue

		return collideList


	def addObject(self, obj):
		self.blocksList.append(Object(from_obj=obj))
		self.objectSpritesList.add(self.blocksList[-1])
		self.updateFloor()


	def removeObject(self, obj):
		self.objectSpritesList.remove(obj)
		self.blocksList.remove(obj)
		self.updateFloor()


	def removeObjectFromPos(self, pos):
		for obj in self.blocksList:
			if obj.isInBlock(pos):
				self.objectSpritesList.remove(obj)
				self.blocksList.remove(obj)

		self.updateFloor()


	def getObjectFromPos(self, pos):
		for obj in self.blocksList:
			if obj.isInBlock(pos):
				return obj

		return Object(obj_type=Object.EMPTY)


	def isInBlock(self, pos):
		for obj in self.blocksList:
			if obj.isInBlock(pos):
				return True

		return False


	def isFloor(self, obj):
		if self.isInBlock((obj.getX() + 5, obj.getY() - 5)):
			return False

		return True


	def getObjectList(self):
		return self.blocksList


	def setObjectList(self, objectList):
		self.blocksList = objectList

		for obj in self.blocksList:
			self.objectSpritesList.add(obj)


	def addCarrot(self):
		while True:
			randPos = random.randint(0, len(self.blocksList) - 1)
			if not self.isInBlock((self.blocksList[randPos].getX() + 10, self.blocksList[randPos].getY() - 26)):
				break

		if self.blocksList[randPos].getType() != Object.CARROT:
			self.carrotsList.append(Object(self.blocksList[randPos].getX() + 10, self.blocksList[randPos].getY() - 26, Object.CARROT))

		for obj in self.blocksList:
			if not self.isFloor(obj):
				obj.replaceImage(obj.getType())

			self.objectSpritesList.add(obj)


	def save(self, name):
		temp_blocks_list = [{"pos":block.getPos(), "type":block.getType()} for block in self.blocksList]
		with open("save/maps/" + name + ".mabbit", "w") as f:
			json.dump(temp_blocks_list, f)


	def load(self, name):
		with open("save/maps/" + name + ".mabbit", "r") as f:
			temp_blocks_list = json.load(f)

		self.blocksList = [Object(block["pos"][0], block["pos"][1], block["type"]) for block in temp_blocks_list]
		self.objectSpritesList = pygame.sprite.Group()

		for obj in self.blocksList:
			self.objectSpritesList.add(obj)

		self.collideBlocksList = self.generateCollideBlocksList()

		self.updateFloor()
