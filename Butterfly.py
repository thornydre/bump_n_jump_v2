#!/usr/bin/python

import pygame
import numpy as np
from random import randint
from pygame.locals import *
from Animation import Animation
from Object import Object


class Butterfly():
	def __init__(self, x, y, color=(255, 255, 255), objectList=[], spriteList=[], prey=None):
		self.objectList = objectList
		self.spriteList = spriteList

		self.rect = pygame.Rect(x, y, 15, 15)
		self.screen = pygame.display.get_surface()

		self.posx = self.rect.x + self.rect.w/2
		self.posy = self.rect.y + self.rect.h/2

		self.butterflyAnim = Animation("butterfly", 8)
		self.butterflyAnim.updateColor(color)
		self.butterflyAnim.setFrameRange(1, 8);
		self.butterflyAnim.setCurrentFrame(randint(1, 8))

		self.sprite = pygame.sprite.RenderPlain(self.butterflyAnim)

		self.butterflyAnim.playAnim()

		self.area = self.screen.get_rect()
		self.color = color

		self.floorLevel = self.screen.get_height() - self.rect.h

		self.degree = randint(0, 360)
		self.speed = 4
		self.steer = 4

		self.prey = prey
		self.comfort_zone = randint(50, 200)

		self.detlaUpdate = 0

		self.collide = False

		self.movePos = [0, 0.01]


	def update(self):
		if(self.detlaUpdate == 1):
			self.detlaUpdate = 0

			self.posx = self.rect.x + self.rect.w/2
			self.posy = self.rect.y + self.rect.h/2

			dist_to_prey = np.absolute(np.sqrt(((self.prey.posx - self.posx) * (self.prey.posx - self.posx)) + ((self.prey.posy - self.posy) * (self.prey.posy - self.posy))))

			if dist_to_prey > self.comfort_zone:
				self.degree -= int(self.preyDetection() * 0.05)

			limitBottom = self.degree - self.steer
			limitTop = self.degree + self.steer

			self.degree = randint(limitBottom, limitTop)

			self.degree = self.degree % 360

			if(randint(0, 1) == 0):
				if(self.speed < 6):
					self.speed += 1

			else:
				if(self.speed > 2):
					self.speed -= 1

			self.movePos[0] = np.cos(np.radians(self.degree)) * self.speed
			self.movePos[1] = np.sin(np.radians(self.degree)) * self.speed

			self.checkForCollision()

			newpos = self.rect.move(self.movePos)
			if self.area.contains(newpos) and not self.collide:
				self.rect = newpos

			self.butterflyAnim.getRect().x = self.rect.x
			self.butterflyAnim.getRect().y = self.rect.y

		else:
			self.detlaUpdate += 1

		self.butterflyAnim.update()
		self.sprite.update()
		self.sprite.draw(self.screen)


	def collisionDetection(self, obj, rabbit=False):
		objCenterX = obj.rect.x + obj.rect.w/2
		objCenterY = obj.rect.y + obj.rect.h/2

		dist = np.absolute(np.sqrt(((objCenterX - self.posx) * (objCenterX - self.posx)) + ((objCenterY - self.posy) * (objCenterY - self.posy))))
		
		if dist < 50:
			distX = np.absolute(objCenterX - self.posx)
			angle = np.degrees(np.arccos(distX/dist))

			if (objCenterX <= self.posx) and (objCenterY <= self.posy):
				angle = 270 - angle

			elif (objCenterX > self.posx) and (objCenterY <= self.posy):
				angle = 360 - angle

			elif (objCenterX <= self.posx) and (objCenterY > self.posy):
				angle = 180 - angle

			angle += 180
			angle = angle % 360

			self.degree = int(angle)


	def screenCollisionDetection(self):
		distBorder = self.posx
		if distBorder < 10:
			self.degree = 0

		if (self.posy) < distBorder:
			distBorder = self.posy
			if distBorder < 10:
				self.degree = 90

		if (self.screen.get_rect().w - self.posx) < distBorder:
			distBorder = self.screen.get_rect().w - self.posx
			if distBorder < 10:
				self.degree = 180

		if (self.screen.get_rect().h - self.posy) < distBorder:
			distBorder = self.screen.get_rect().h - self.posy
			if distBorder < 10:
				self.degree = 270


	def checkForCollision(self):
		for obj in self.objectList:
			if obj.getType() != Object.CARROT:
				self.collisionDetection(obj, False)

		self.screenCollisionDetection()

		#for rabbit in self.rabbitList:
		#	self.collisionDetection(rabbit, True)
	

	def preyDetection(self):
		dist_x = self.prey.posx - self.posx
		dist_y = self.prey.posy - self.posy

		angle_rad = np.arctan(dist_y / dist_x)

		adj = np.cos(angle_rad) * 20
		opp = np.sin(angle_rad) * 20

		a = np.array([int(self.posx) + self.movePos[0] * 30, int(self.posy) + self.movePos[1] * 30])
		b = np.array([self.posx, self.posy])

		if dist_x >= 0:
			c = np.array([int(self.posx) + adj, int(self.posy) + opp])
		else:
			c = np.array([int(self.posx) - adj, int(self.posy) - opp])

		ba = a - b
		bc = c - b

		ang_a = np.arctan2(*ba[::-1])
		ang_b = np.arctan2(*bc[::-1])
		angle = np.rad2deg((ang_a - ang_b) % (2 * np.pi))
		if angle > 180:
			angle = angle - 360

		return angle


	def moveLeftStart(self):
		self.movingLeft = True
		self.movingRight = False


	def moveLeftStop(self):
		self.movingLeft = False
		self.movePos[0] = 0


	def moveRightStart(self):
		self.movingRight = True
		self.movingLeft = False
	

	def moveRightStop(self):
		self.movingRight = False
		self.movePos[0] = 0


	def getAnim(self):
		return self.butterflyAnim
