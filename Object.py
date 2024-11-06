#!/usr/bin/python

import pygame
import Resources


class Object(pygame.sprite.Sprite):
	EMPTY = 0
	DIRT = 1
	ICE = 2
	BOUNCE = 3
	CARROT = 4

	def __init__(self, x=0, y=0, obj_type=DIRT, from_obj=None):
		self.typeList = {
			self.DIRT:"earth.png",
			self.ICE:"ice.png",
			self.BOUNCE:"boing.png",
			self.CARROT:"carrot.png"
		}

		if from_obj:
			pos = from_obj.getPos()
			self.type = from_obj.getType()
		else:
			pos = pygame.math.Vector2(x, y)
			self.type = obj_type

		self.friction = 0.6

		if self.type == self.ICE:
			self.friction = 0.1

		if self.type == self.EMPTY:
			self.rect = pygame.Rect(0, 0, 0, 0)
		else:
			pygame.sprite.Sprite.__init__(self)
			self.image = Resources.loadPNG(self.typeList[self.type])
			self.rect = self.image.get_rect()

		self.rect.topleft = pos


	def __str__(self):
		print(f"Object {self.id} ({self.rect.left}, {self.rect.top} {self.type})")


	def replaceImage(self, objType, isFloor=False):
		if isFloor or self.type == self.BOUNCE:
			self.image = Resources.loadPNG(self.typeList[objType])
		else:
			self.image = Resources.loadPNG(f"middle_{self.typeList[objType]}")


	def getPos(self):
		return self.rect.topleft


	def getX(self):
		return self.rect.left


	def getY(self):
		return self.rect.top


	def getType(self):
		return self.type


	def isInBlock(self, pos):
		return self.rect.collidepoint(pos)


	def getFriction(self):
		return self.friction