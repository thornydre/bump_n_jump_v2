#!/usr/bin/python

import pygame
import Resources
from pygame.locals import *


class Button():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()

	def __init__(self, x, y, width, height, text):
		self.screen = pygame.display.get_surface()
		self.text = text
		self.buttonRect = pygame.Rect(x, y, width, height)

		self.base_color = pygame.Color(150, 150, 150)
		self.hover_color = pygame.Color(200, 200, 200)

		self.color = self.base_color

		self.buttonSound = pygame.mixer.Sound("resources/sound/button.wav")
		self.buttonSound.set_volume(float(Resources.getOptionValue("sound"))/100)

		if pygame.font:
			font = pygame.font.Font(None, 22)
			self.textDisp = font.render(self.text, 1, (100, 100, 100))

		self.textRect = self.textDisp.get_rect(center=(x + width/2, y + height/2 + 1))


	def eventListener(self, event):
		mse = pygame.mouse.get_pos()

		if event.type == MOUSEBUTTONDOWN:
			if self.buttonRect.collidepoint(mse):
				self.buttonSound.play()
		elif event.type == MOUSEMOTION:
			if self.buttonRect.collidepoint(mse):
				self.color = self.hover_color
			else:
				self.color = self.base_color


	def update(self):
		pygame.draw.rect(self.screen, self.color, self.buttonRect)
		self.screen.blit(self.textDisp, self.textRect)


	def clicked(self):
		self.buttonSound.play()
		self.command()


	def setCommand(self, command):
		self.command = command


	def onButton(self, pos):
		return self.buttonRect.collidepoint(pos)


	def getX(self):
		return self.buttonRect.x


	def getY(self):
		return self.buttonRect.y


	def getWidth(self):
		return self.buttonRect.w


	def getHeight(self):
		return self.buttonRect.h


	def getText(self):
		return self.text


	def setY(self, y):
		self.buttonRect.y = y
		self.textRect = self.textDisp.get_rect(centerx=self.buttonRect.x + self.buttonRect.w/2, centery=self.buttonRect.y + self.buttonRect.h/2 + 1)


	def setColor(self, color):
		self.color = color