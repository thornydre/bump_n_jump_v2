#!/usr/bin/python

import pygame
from pygame.locals import *


class EditorToolbar():
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.rect = pygame.Rect(self.screen.get_rect().w - 200, 0, 200, self.screen.get_rect().h)
	
	def update(self):
		pygame.draw.rect(self.screen, (50, 50, 50), self.rect)

	def getX(self):
		return self.rect.x

	def getY(self):
		return self.rect.y

	def getWidth(self):
		return self.rect.w

	def getValue(self):
		return self.value
