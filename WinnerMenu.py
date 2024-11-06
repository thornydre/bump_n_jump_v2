#!/usr/bin/python

import pygame
import Resources
import MainMenu
from pygame.locals import *
from Button import Button


class WinnerMenu():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()


	def __init__(self, surface, winner):
		self.screen = surface

		self.buttonSound = pygame.mixer.Sound("resources/sound/button.wav")
		self.buttonSound.set_volume(float(Resources.getOptionValue("sound"))/100)

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((50, 50, 50))

		self.winner = winner

		self.buttons = {}

		self.buttons["return"] = Button(self.screen.get_width()/2 - 200/2, 175, 200, 40, "RETURN TO MENU")

		pygame.display.flip()


	def update(self):
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()

		for event in pygame.event.get():
			if event.type == QUIT or (key[K_F4] and key[K_LALT]):
				return False, self

			elif event.type == MOUSEBUTTONDOWN:
				mse = pygame.mouse.get_pos()

				if self.buttons["return"].onButton(mse):
					self.buttonSound.play()
					return True, MainMenu.MainMenu(self.screen)

		self.screen.blit(self.background, self.background.get_rect(), self.background.get_rect())

		if pygame.font:
			font = pygame.font.Font(None, 65)
			if self.winner == "draw":
				text = font.render("DRAW !", 1, (220, 220, 220))
			else:
				text = font.render("THE WINNER IS \"" + self.winner.upper() + "\" !", 1, (220, 220, 220))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, y=70)
			self.screen.blit(text, textpos)

		for button in self.buttons.values():
			button.update()

		pygame.display.update()

		return True, self
