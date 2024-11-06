#!/usr/bin/python

import pygame
import Resources
import MultiMenu
import GameRabbitMenu
import MainMenu
from pygame.locals import *
from Button import Button


class PlayModeMenu():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()


	def __init__(self, surface):
		self.screen = surface

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((50, 50, 50))

		self.buttonSound = pygame.mixer.Sound("resources/sound/button.wav")
		self.buttonSound.set_volume(float(Resources.getOptionValue("sound"))/100)

		self.buttons = {}

		self.buttons["local"] = Button(self.screen.get_width()/2 - 200/2, self.screen.get_height()/2 - 150 - 40/2, 200, 40, "LOCAL")
		self.buttons["network"] = Button(self.screen.get_width()/2 - 200/2, self.screen.get_height()/2 - 50 - 40/2, 200, 40, "NETWORK")
		self.buttons["back"] = Button(self.screen.get_width()/2 - 200/2, self.screen.get_height()/2 + 50 - 40/2, 200, 40, "BACK")
		pygame.display.flip()


	def update(self):
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()

		for event in pygame.event.get():
			if event.type == QUIT or (key[K_F4] and key[K_LALT]):
				return False, self

			elif event.type == MOUSEBUTTONDOWN:
				mse = pygame.mouse.get_pos()

				if self.buttons["local"].onButton(mse):
					self.buttonSound.play()
					return True, GameRabbitMenu.GameRabbitMenu(self.screen)

				elif self.buttons["network"].onButton(mse):
					self.buttonSound.play()
					return True, MultiMenu.MultiMenu(self.screen)

				elif self.buttons["back"].onButton(mse):
					self.buttonSound.play()
					return True, MainMenu.MainMenu(self.screen)

		self.screen.blit(self.background, self.background.get_rect(), self.background.get_rect())

		for button in self.buttons.values():
			button.update()

		pygame.display.update()

		return True, self