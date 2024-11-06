#!/usr/bin/python

import pygame
import numpy as np
from pygame.locals import *
from pygame import gfxdraw


class Checkbox():
	def __init__(self, x, y, text, checked=False, radio=False):
		self.screen = pygame.display.get_surface()
		self.checked = checked
		self.text = text
		self.radio = radio

		if self.radio:
			self.pos = (x + 7, y + 7)
		else:
			self.checkboxRect = pygame.Rect(x, y, 15, 15)
			self.crossRect = pygame.Rect(x + 2, y + 2, 11, 11)

		if pygame.font:
			font = pygame.font.Font(None, 22)
			self.textDisp = font.render(self.text, 1, (75, 75, 75))

		self.textRect = self.textDisp.get_rect(x=x + 25, centery=y + 9)
	
	def update(self):
		if self.radio:
			pygame.gfxdraw.filled_circle(self.screen, int(self.pos[0]), int(self.pos[1]), 6, (150, 150, 150))
			pygame.gfxdraw.aacircle(self.screen, int(self.pos[0]), int(self.pos[1]), 6, (150, 150, 150))

			if self.checked:
				pygame.gfxdraw.filled_circle(self.screen, int(self.pos[0]), int(self.pos[1]), 4, (75, 75, 75))
				pygame.gfxdraw.aacircle(self.screen, int(self.pos[0]), int(self.pos[1]), 4, (75, 75, 75))
		else:
			pygame.draw.rect(self.screen, (150, 150, 150), self.checkboxRect)

			if self.checked:
				pygame.draw.rect(self.screen, (75, 75, 75), self.crossRect)

		self.screen.blit(self.textDisp, self.textRect)

	def onCheckbox(self, x_y):
		(x, y) = x_y
		if self.radio:
			if np.absolute(np.sqrt(((x - self.pos[0]) * (x - self.pos[0])) + ((y - self.pos[1]) * (y - self.pos[1])))) <= 6:
				return True
			elif x >= self.textRect.x and x <= (self.textRect.x + self.textRect.w) and y >= self.textRect.y and y <= (self.textRect.y + 15):
				return True
			else:
				return False
		else:
			if x >= self.checkboxRect.x and x <= (self.checkboxRect.x + 25 + self.textRect.w) and y >= self.checkboxRect.y and y <= (self.checkboxRect.y + 15):
				return True
			else:
				return False

	def changeState(self):
		if self.isChecked():
			self.uncheck()
		else:
			self.check()

	def isChecked(self):
		return self.checked

	def check(self):
		self.checked = True

	def uncheck(self):
		self.checked = False
