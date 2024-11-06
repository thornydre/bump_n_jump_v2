#!/usr/bin/python

import pygame
import numpy as np
from pygame.locals import *
from pygame import gfxdraw
from random import randint


class Prey():
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.color = pygame.Color(10, 10, 10)
		self.size = 6
		self.posx = randint(0, 1000)
		self.posy = randint(0, 600)

		self.alive = True

		self.movePos = [0,0.01]

		self.degree = randint(-20, 20)
		self.speed = 1
		self.steer = 20


	def update(self):
		if self.alive:
			limitBottom = self.degree - self.steer
			limitTop = self.degree + self.steer

			self.degree = randint(limitBottom, limitTop)

			self.degree = self.degree % 360

			self.checkForCollision()

			self.movePos[0] = np.cos(np.radians(self.degree)) * self.speed
			self.movePos[1] = np.sin(np.radians(self.degree)) * self.speed

			self.posx += self.movePos[0]
			self.posy += self.movePos[1]

		# pygame.gfxdraw.filled_circle(self.screen, int(self.posx), int(self.posy), self.size, self.color)
		# pygame.gfxdraw.aacircle(self.screen, int(self.posx), int(self.posy), self.size, self.color)


	def screenCollisionDetection(self):
		if self.posx < 10:
			self.degree = 10
		elif self.posy < 10:
			self.degree = 90
		elif self.posx > self.screen.get_rect().w - 10:
			self.degree = 180
		elif self.posy > self.screen.get_rect().h - 10:
			self.degree = 270


	def collisionDetection(self):
		carPosX = self.posx
		carPosY = self.posy

		dist = np.absolute(np.sqrt(((obstPosX - carPosX) * (obstPosX - carPosX)) + ((obstPosY - carPosY) * (obstPosY - carPosY))))


	def checkForCollision(self):
		self.screenCollisionDetection()


	def reset(self, posx, posy):
		self.alive = True
		self.posx = posx
		self.posy = posy
		self.degree = 0
		self.nearest_border_dist = []