#!/usr/bin/python

import pygame
import Resources
from pygame.locals import *


class Animation(pygame.sprite.Sprite):
	def __init__(self, image, nbFrames):
		pygame.sprite.Sprite.__init__(self)

		self.flip = False
		self.interval = 0
		self.nbFrames = nbFrames
		self.play = True
		self.start = 0
		self.end = nbFrames - 1
		self.cyclic = True
		self.imageName = image

		self.origArrAnim = []
		for i in range(0, self.nbFrames):
			self.origArrAnim.append(Resources.loadPNG(f"{self.imageName}{str(i + 1).zfill(4)}.png", True))

		self.arrAnim = [img.copy() for img in self.origArrAnim]

		self.currentFrameNb = self.start
		self.image = self.arrAnim[self.currentFrameNb]
		self.rect = self.image.get_rect()


	def update(self):
		if self.interval < 60./24:
			self.interval += 1
		else:
			self.interval = 0
			if self.play:
				self.currentFrameNb += 1

				if self.currentFrameNb > self.end:
					if self.cyclic:
						self.currentFrameNb = self.start
					else:
						self.currentFrameNb = self.end

			if self.flip:
				self.image = self.arrAnim[int(self.currentFrameNb + self.nbFrames/2)]
			else:
				self.image = self.arrAnim[self.currentFrameNb]


	def updateColor(self, color):
		self.arrAnim = [img.copy() for img in self.origArrAnim]

		for img in self.arrAnim:
			img.fill(color, special_flags=BLEND_MULT)


	def playAnim(self, cyclic=True):
		self.play = True
		if not cyclic:
			self.cyclic = False
		else:
			self.cyclic = True


	def stopAnim(self):
		self.play = False


	def isRunning(self):
		return self.play


	def rewind(self):
		self.currentFrameNb = 0


	def nextFrame(self):
		self.currentFrameNb += 1


	def setCurrentFrame(self, index):
		self.currentFrameNb = index - 1


	def flipAnim(self):
		if self.flip:
			self.flip = False
		else:
			self.flip = True


	def setFrameRange(self, start, end):
		self.start = start - 1
		self.end = end - 1


	def getFlip(self):
		return self.flip


	def getRect(self):
		return self.rect


	def setRect(self, rect):
		self.rect = rect


	def setPos(self, pos):
		self.rect.topleft = pos

		# for img in self.arrAnim:
		# 	img[1].x = x
		# 	img[1].y = y
