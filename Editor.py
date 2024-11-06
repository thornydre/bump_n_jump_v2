#!/usr/bin/python

import sys
import os
import random
import pygame
import glob
import Resources
import PauseEditorMenu
import LoadLevelMenu
import SaveLevelMenu
import MainMenu
from pygame.locals import *
from Object import Object
from Map import Map
from EditorToolbar import EditorToolbar


class Editor():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()

	def __init__(self, surface, levelPreset="empty"):
		self.screen = surface

		self.backgroundImage = Resources.loadPNG("background.png")
		self.backgroundRect = self.backgroundImage.get_rect()

		self.blockList = [Object(obj_type=Object.DIRT), Object(obj_type=Object.BOUNCE), Object(obj_type=Object.ICE)]

		self.currentBlockNumber = 0
		self.currentBlock = self.blockList[self.currentBlockNumber]
		self.currentSpriteBlock = pygame.sprite.RenderPlain(self.currentBlock)

		self.buttonSound = pygame.mixer.Sound("resources/sound/button.wav")
		self.buttonSound.set_volume(float(Resources.getOptionValue("sound"))/100)

		self.grid = False

		self.active = True

		self.pauseMenu = PauseEditorMenu.PauseEditorMenu()

		self.toolbar = EditorToolbar()

		self.level = Map(True)
		if levelPreset != "empty":
			self.level.load(levelPreset)
		
		pygame.display.flip()

	def update(self):
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()

		if self.active:
			for event in pygame.event.get():
				mse = pygame.mouse.get_pos()

				if (int(mse[0] / 50))*50 < self.toolbar.getX():
					self.currentBlock.rect.topleft = ((int(mse[0] / 50))*50, (int(mse[1] / 50))*50)
				else:
					self.currentBlock.rect.topleft = (self.toolbar.getX() - 50, (int(mse[1] / 50))*50)

				if event.type == QUIT or (key[K_F4] and key[K_LALT]):
					return False, self

				elif key[K_LCTRL] and key[K_s]:
					self.level.save("last")
					return True, SaveLevelMenu.SaveLevelMenu(self.level)

				elif key[K_LCTRL] and key[K_l]:
					return True, LoadLevelMenu.LoadLevelMenu("Editor")

				elif event.type == MOUSEBUTTONDOWN:
					if event.button == 5:
						self.currentBlockNumber = (self.currentBlockNumber - 1) % len(self.blockList)
					if event.button == 4:
						self.currentBlockNumber = (self.currentBlockNumber + 1) % len(self.blockList)
					if event.button == 3:
						self.level.removeObjectFromPos(mse)
					if event.button == 1:
						if not any(obj.rect.collidepoint(mse) for obj in self.level.blocksList):
							if self.currentBlock.getType() == Object.BOUNCE:
								if self.level.getObjectFromPos((mse[0], mse[1] + 50)).getType() != Object.BOUNCE:
									if not self.level.isInBlock((mse[0], mse[1] - 50)):
										self.level.addObject(self.currentBlock)
							else:
								if self.level.getObjectFromPos((mse[0], mse[1] + 50)).getType() != Object.BOUNCE:
									self.level.addObject(self.currentBlock)

					self.currentBlock = self.blockList[self.currentBlockNumber]
					self.currentSpriteBlock = pygame.sprite.RenderPlain(self.currentBlock)
					self.currentBlock.rect.topleft = ((int(mse[0] / 50))*50, (int(mse[1] / 50))*50)

				elif event.type == MOUSEMOTION:
					if mouse[0]:
						if not any(obj.rect.collidepoint(mse) for obj in self.level.blocksList):
							if self.currentBlock.getType() == Object.BOUNCE:
								if self.level.getObjectFromPos((mse[0], mse[1] + 50)).getType() != Object.BOUNCE:
									if not self.level.isInBlock((mse[0], mse[1] - 50)):
										self.level.addObject(self.currentBlock)
							else:
								if self.level.getObjectFromPos((mse[0], mse[1] + 50)).getType() != Object.BOUNCE:
									self.level.addObject(self.currentBlock)

					elif mouse[2]:
						self.level.removeObjectFromPos(mse)

				elif event.type == KEYDOWN:
					if event.key == K_g:
						if self.grid:
							self.grid = False
						else:
							self.grid = True

					elif event.key == K_ESCAPE:
						self.active = False
						self.level.save("last")

			self.screen.blit(self.backgroundImage, self.backgroundRect, self.backgroundRect)

			#LEVEL UPDATE
			self.level.update()

			#TOOLBAR UPDATE
			self.toolbar.update()

			self.currentBlock.update()
			self.currentSpriteBlock.draw(self.screen)

			if self.grid:
				self.drawGrid()

		else:
			for event in pygame.event.get():
				if event.type == QUIT or (key[K_F4] and key[K_LALT]):
					return False, self

				elif event.type == MOUSEBUTTONDOWN:
					mse = pygame.mouse.get_pos()

					if self.pauseMenu.buttons["resume"].onButton(mse):
						self.buttonSound.play()
						self.active = True

					elif self.pauseMenu.buttons["save"].onButton(mse):
						self.buttonSound.play()
						return True, SaveLevelMenu.SaveLevelMenu(self.screen, self.level)

					elif self.pauseMenu.buttons["load"].onButton(mse):
						self.buttonSound.play()
						return True, LoadLevelMenu.LoadLevelMenu(self.screen, "Editor")

					elif self.pauseMenu.buttons["mainMenu"].onButton(mse):
						self.buttonSound.play()
						return True, MainMenu.MainMenu(self.screen)

				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.active = True

			self.pauseMenu.update()

		pygame.display.update()

		return True, self

	def drawGrid(self):
		for i in range(50, self.screen.get_height(), 50):
			pygame.draw.line(self.screen, (5, 5, 5), (0, i - 1), (self.screen.get_width(), i - 1))
		for j in range(50, self.screen.get_width(), 50):
			pygame.draw.line(self.screen, (5, 5, 5), (j - 1, 0), (j - 1, self.screen.get_height()))