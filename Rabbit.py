#!/usr/bin/python

import pygame
import random
import Resources
from pygame.locals import *
from Animation import Animation
from Explosion import Explosion
from Carrot import Carrot
from Object import Object


class Rabbit():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()

	def __init__(self, name="", color=(255, 255, 255), objectsList=[], spritesList=[], x=0, y=0):
		self.name = name

		self.pos = pygame.math.Vector2(x, y)
		self.vel = pygame.math.Vector2(0.0, 0.0)

		self.objectsList = objectsList
		self.spritesList = spritesList

		self.rabbitsList = []

		self.color = color
		self.rect = pygame.Rect(x, y, 33, 32)
		self.rabbitAnim = Animation("rabbit", 30)
		self.rabbitAnim.updateColor(self.color)
		self.rabbitAnim.setFrameRange(1, 8);

		self.sprite = pygame.sprite.Group(self.rabbitAnim)

		self.rabbitAnim.stopAnim()

		self.screen = pygame.display.get_surface()
		self.area = self.screen.get_rect()
		self.area.h += 450
		self.area.y -= 550
		self.area.w -= 200

		self.explosion = Explosion()

		self.movingLeft = False
		self.movingRight = False
		self.isJumping = False
		self.isOnBlock = False
		self.sliding = True
		self.sliding_factor = 0
		self.sliding_incrementation = 0.4

		self.direction = "left"

		self.touched = False
		self.touchDelay = 0

		self.jumpSound = pygame.mixer.Sound("resources/sound/jump.wav")
		self.splashSound = pygame.mixer.Sound("resources/sound/splash.wav")
		self.carrotSound = pygame.mixer.Sound("resources/sound/carrot.wav")

		self.jumpSound.set_volume(float(Resources.getOptionValue("sound"))/100)
		self.splashSound.set_volume(float(Resources.getOptionValue("sound"))/100)
		self.carrotSound.set_volume(float(Resources.getOptionValue("sound"))/100)

		self.maxSpeed = 5
		self.gravity = 0.6

		self.reset()

		self.points = 0
		self.carrots = 0

		self.thrownCarrots = []

		self.blood = Resources.getOptionValue("blood")


	def __str__(self):
		print("Rabbit ", self.id,  ": ", self.name)


	def update(self):
		if self.touched:
			self.touchDelayCalculation()

		else:
			self.updateVelocity()

		# Adding gravity
		self.vel[1] += self.gravity

		self.move()

		# self.carrotCollision()

		self.updateAnimation()

		tmpThrownCarrots = []

		for carrot in self.thrownCarrots:
			end = carrot.update()

			if not end:
				tmpThrownCarrots.append(carrot)

		self.thrownCarrots = tmpThrownCarrots

		self.rabbitAnim.update()
		self.sprite.update()
		self.sprite.draw(self.screen)
		self.explosion.update()


	def updateVelocity(self):
		# Left and right key presses
		if self.movingLeft:
			if self.vel[0] > -self.maxSpeed:
				self.vel[0] -= self.sliding_incrementation
			else:
				self.vel[0] = -self.maxSpeed

		if self.movingRight:
			if self.vel[0] < self.maxSpeed:
				self.vel[0] += self.sliding_incrementation
			else:
				self.vel[0] = self.maxSpeed

		# Sliding when no key is pressed
		if not self.movingRight and not self.movingLeft:
			if self.direction == "left":
				if self.vel[0] < 0:
					self.vel[0] += self.sliding_incrementation
				if self.vel[0] > 0:
					self.vel[0] = 0
			elif self.direction == "right":
				if self.vel[0] > 0:
					self.vel[0] -= self.sliding_incrementation
				if self.vel[0] < 0:
					self.vel[0] = 0


	def move(self):
		self.sliding_incrementation = 0.4

		near_objects_list = self.getNearObjects(self.objectsList, 100)

		# X axis
		self.rect.x += int(self.vel[0])
		hit_list = self.getCollisionList(near_objects_list)
		for obj in hit_list:
			if self.vel[0] > 0:
				self.rect.right = obj.rect.left
				self.vel[0] = 0
			elif self.vel[0] < 0:
				self.rect.left = obj.rect.right
				self.vel[0] = 0

		# Y axis
		self.rect.y += self.vel[1]
		hit_list = self.getCollisionList(near_objects_list)
		for obj in hit_list:
			if self.vel[1] > 0:
				self.isJumping = False
				self.isOnBlock = True
				self.rect.bottom = obj.rect.top
				self.vel[1] = 0

			elif self.vel[1] < 0:
				self.rect.top = obj.rect.bottom
				self.vel[1] = 0

			if self.isJumping:
				self.isOnBlock = False

			if self.isOnBlock:
				if (self.rect.x > (obj.rect.x + obj.rect.w)) or ((self.rect.x + self.rect.w) < obj.rect.x):
					self.isOnBlock = False

		# Get properties from blocks
		for obj in near_objects_list:
			if obj.isInBlock((self.rect.centerx, self.rect.bottom + 2)):
				self.sliding_incrementation = obj.getFriction()

				if obj.getType() == Object.BOUNCE:
					self.jump(12.7)

		# Rabbit detection
		for rabbit in self.rabbitsList:
			if self.vel[1] > 0:
				if rabbit.rect.collidepoint(self.rect.bottomleft) or rabbit.rect.collidepoint(self.rect.bottomright):
					self.isJumping = False
					self.jump(5)
					if self.blood == 1:
						rabbit.explosion = Explosion(rabbit.rect.x, rabbit.rect.y, rabbit.color)
						rabbit.explosion.startExplosion()
						self.splashSound.play()
					rabbit.reset()
					self.points += 1


	def carrotCollision(self):
		print("CARROT COLLISION")


	def checkForCollision(self):
		self.sliding_incrementation = 0.5

		if self.vel[0] == 0 and self.vel[1] == 0  and not self.isJumping:
			return

		for obj in self.objectsList:
			if obj.getType() == Object.CARROT:
				if obj.isInBlock((self.rect.centerx, self.rect.bottom - 5)):
					self.carrotSound.play()
					self.carrots += 1
					self.objectsList.remove(obj)
					self.spritesList.remove(obj)

			else:
				self.collisionDetection(obj, False)
				if obj.isInBlock((self.rect.centerx, self.rect.bottom + 2)):
					self.sliding_incrementation = obj.getFriction()

		for rabbit in self.rabbitsList:
			self.collisionDetection(rabbit, True)


	def collisionDetection(self, obj, rabbit=False):
		collisionUndetected = True

		collision = self.rect.colliderect(obj.rect)

		if collision:
			if self.vel[1] > 0 and not self.isOnBlock:
				self.isJumping = False
				
				if rabbit:
					if self.vel[1] > 0.01:
						self.jump(5)
						if self.blood == 1:
							obj.explosion = Explosion(obj.rect.x, obj.rect.y, obj.color)
							obj.explosion.startExplosion()
							self.splashSound.play()
						obj.reset()
						self.points += 1

				elif obj.getType() == Object.BOUNCE:
					self.jump(12.7)

				else:
					self.rect.bottom = obj.rect.y
					self.vel[1] = 0
					self.isOnBlock = True

				collisionUndetected = False

		if collisionUndetected:
			if self.vel[1] < 0:
				if collision:
					self.vel[1] = 0.01
					collisionUndetected = False

		if collisionUndetected:
			if self.vel[0] != 0:
				if collision:
					self.vel[0] = 0

		if self.isJumping:
			self.isOnBlock = False

		if self.isOnBlock:
			if (self.rect.x > (obj.rect.x + obj.rect.w)) or ((self.rect.x + self.rect.w) < obj.rect.x):
				self.isOnBlock = False
				self.vel[1] = 0.01


	def getNearObjects(self, obj_list, search_radius):
		near_objects_list = []
		for obj in obj_list:
			if (pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(obj.rect.center)).length() < search_radius:
				near_objects_list.append(obj)

		return near_objects_list


	def getCollisionList(self, obj_list):
		hit_list = []

		for obj in obj_list:
			if self.rect.colliderect(obj.rect):
				hit_list.append(obj)

		return hit_list


	def jump(self, jump_vel=8.1):
		if not self.isJumping:
			self.jumpSound.play()
			self.vel[1] = -jump_vel
		self.isJumping = True


	def moveLeftStart(self):
		if self.rabbitAnim.getFlip():
			self.rabbitAnim.flipAnim()
		self.rabbitAnim.playAnim()
		self.movingLeft = True
		self.movingRight = False
		self.direction = "left"


	def moveLeftStop(self):
		if not self.movingRight:
			self.rabbitAnim.stopAnim()
			self.rabbitAnim.rewind()
		self.movingLeft = False


	def moveRightStart(self):
		if not self.rabbitAnim.getFlip():
			self.rabbitAnim.flipAnim()
		self.rabbitAnim.playAnim()
		self.movingRight = True
		self.movingLeft = False
		self.direction = "right"


	def moveRightStop(self):
		if not self.movingLeft:
			self.rabbitAnim.stopAnim()
			self.rabbitAnim.rewind()
		self.movingRight = False


	def appendRabbit(self, rabbit):
		self.rabbitsList.append(rabbit)


	def reset(self):
		self.touched = False

		while True:
			randObj = self.objectsList[random.randint(1, len(self.objectsList)) - 1]
			if self.isFloor(randObj):
				break

		self.rect.topleft = (randObj.rect.x, randObj.rect.y - randObj.rect.h)
		self.vel[1] = 0


	def isInBlock(self, pos):
		for obj in self.objectsList:
			if obj.isInBlock(pos):
				return True

		return False


	def isFloor(self, object):
		if self.isInBlock((object.getX() + 5, object.getY() - 5)):
			return False

		return True


	def touch(self):
		self.touched = True
		self.touchDelay = 180
		TOUCH = USEREVENT + 1
		touchevent = pygame.event.Event(TOUCH)
		pygame.event.post(touchevent)


	def touchDelayCalculation(self):
		# Rabbit freezes when touched by carrot
		self.touchDelay -= 1

		if(self.touchDelay == 0):
			self.touched = False
			UNTOUCH = USEREVENT + 2
			untouchevent = pygame.event.Event(UNTOUCH)
			pygame.event.post(untouchevent)


	def isTouched(self):
		return self.touched


	def throwCarrot(self):
		if(self.carrots > 0):
			if(self.direction == "right"):
				self.thrownCarrots.append(Carrot(self.direction, self.rect.x + 10, self.rect.y, self.objectsList, self.rabbitsList))
			else:
				self.thrownCarrots.append(Carrot(self.direction, self.rect.x, self.rect.y, self.objectsList, self.rabbitsList))
			self.carrots -= 1


	def updateColor(self, color):
		self.rabbitAnim.updateColor(color)


	def updateAnimation(self):
		if self.isJumping:
			self.rabbitAnim.setFrameRange(9, 15)
			if self.vel[1] < 0:
				self.rabbitAnim.stopAnim()
				self.rabbitAnim.setCurrentFrame(9)
			else:
				self.rabbitAnim.playAnim(False)

		else:
			self.rabbitAnim.setFrameRange(1, 8)
			if not self.movingLeft and not self.movingRight:
				self.rabbitAnim.stopAnim()
				self.rabbitAnim.rewind()
			else:
				self.rabbitAnim.playAnim()

		animRectOffset = pygame.math.Vector2(5, 16)
		self.rabbitAnim.setPos(self.rect.topleft - animRectOffset)


	def getId(self):
		return self.id


	def getName(self):
		return self.name


	def getPoints(self):
		return self.points


	def getCarrots(self):
		return self.carrots


	def getColor(self):
		return self.color


	def getAnim(self):
		return self.rabbitAnim


	def setId(self, id):
		self.id = id


	def setName(self, name):
		self.name = name


	def setPoints(self, points):
		self.points = points
