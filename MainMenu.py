#!/usr/bin/python

import pygame
import Resources
import Editor
import OptionMenu
import PlayModeMenu
from pygame.locals import *
from Button import Button
from Slider import Slider
from Checkbox import Checkbox
from Background import Background


class MainMenu():
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

		menu_pos_y = 175
		b_w = 200
		b_h = 40
		screen_rect = self.screen.get_rect()

		self.buttons["play"] = Button(screen_rect.centerx - b_w/2, menu_pos_y, b_w, b_h, "PLAY")
		self.buttons["editor"] = Button(screen_rect.centerx - b_w/2, menu_pos_y + 100, b_w, b_h, "EDITOR")
		self.buttons["option"] = Button(screen_rect.centerx - b_w/2, menu_pos_y + 200, b_w, b_h, "OPTION")
		self.buttons["quit"] = Button(screen_rect.centerx - b_w/2, menu_pos_y + 300, b_w, b_h, "QUIT")

		pygame.display.flip()


	def update(self):
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()
		mse = pygame.mouse.get_pos()

		for event in pygame.event.get():
			for button in self.buttons.values():
				button.eventListener(event)

			if event.type == QUIT or (key[K_F4] and key[K_LALT]):
				return False, self

			elif event.type == MOUSEBUTTONDOWN:
				if self.buttons["play"].onButton(mse):
					return True, PlayModeMenu.PlayModeMenu(self.screen)

				elif self.buttons["editor"].onButton(mse):
					return True, Editor.Editor(self.screen)

				elif self.buttons["option"].onButton(mse):
					return True, OptionMenu.OptionMenu(self.screen)

				elif self.buttons["quit"].onButton(mse):
					return False, self

		self.screen.blit(self.background, self.background.get_rect(), self.background.get_rect())

		if pygame.font:
			font = pygame.font.Font(None, 65)
			text = font.render("BUMP'N'JUMP", 1, (220, 220, 220))
			textpos = text.get_rect(centerx=self.screen.get_width()/2, y=70)
			self.screen.blit(text, textpos)

		for button in self.buttons.values():
			button.update()

		pygame.display.update()

		return True, self
