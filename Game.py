#!/usr/bin/python

import sys
import os
import random
import pygame
import Resources
import PauseGameMenu
import WinnerMenu
import LoadLevelMenu
import MainMenu
from pygame.locals import *
from Rabbit import Rabbit
from Butterfly import Butterfly
from Prey import Prey
from Animation import Animation
from Object import Object
from Map import Map
from GameToolbar import GameToolbar


class Game():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()

	def __init__(self, surface, rabbit1, rabbit2, mode, levelPreset=Object.EMPTY):
		self.screen = surface

		self.buttonSound = pygame.mixer.Sound("resources/sound/button.wav")
		self.buttonSound.set_volume(float(Resources.getOptionValue("sound"))/100)

		self.backgroundImage = Resources.loadPNG("background.png")
		self.backgroundRect = self.backgroundImage.get_rect()

		self.active = True
		self.mode = mode
		self.timer = 5400

		self.level = Map()
		if levelPreset != Object.EMPTY:
			self.level.load(levelPreset)

		self.toolbar = GameToolbar()
		self.pauseMenu = PauseGameMenu.PauseGameMenu()

		self.color1 = rabbit1["color"]
		self.color2 = rabbit2["color"]

		self.regis = Rabbit(rabbit1["name"], self.color1, self.level.blocksList, self.level.objectSpritesList)
		self.john = Rabbit(rabbit2["name"], self.color2, self.level.blocksList, self.level.objectSpritesList)

		self.regis.appendRabbit(self.john)
		self.john.appendRabbit(self.regis)

		self.deltaCarrot = 0
		self.timeCarrot = random.randint(1, 4)
		
		self.prey = Prey()
		self.butterflies = []

		for l in range(10):
			while True:
				randPos = random.randint(0, len(self.level.blocksList)-1)
				if not self.level.isInBlock((self.level.blocksList[randPos].getX() + 10, self.level.blocksList[randPos].getY() - 26)):
					break

			butterfly = Butterfly(self.level.blocksList[randPos].getX() + 10, self.level.blocksList[randPos].getY() - 26, (255, 10, 100), self.level.blocksList, self.level.objectSpritesList, self.prey)
			self.butterflies.append(butterfly)

		pygame.display.flip()

	def update(self):
		key = pygame.key.get_pressed()

		if self.active:
			self.timer -= 1

			pygame.mouse.set_visible(0)

			for event in pygame.event.get():
				if event.type == QUIT or (key[K_F4] and key[K_LALT]):
					return False, self

				elif event.type == MOUSEMOTION and (key[K_LSHIFT] or key[K_LCTRL]):
					mse = pygame.mouse.get_pos()
					if not any(obj.rect.collidepoint(mse) for obj in self.level.blocksList):
						x = (int(mse[0]) / 50)*50
						y = (int(mse[1]) / 50)*50
						if key[K_LSHIFT]:
							self.level.addObject(x, y, Object.DIRT)
						else:
							self.level.addObject(x, y, Object.BOUNCE)

				elif event.type == MOUSEMOTION and key[K_LALT]:
					mse = pygame.mouse.get_pos()
					self.level.removeObjectFromPos(mse)

				elif event.type == KEYDOWN:
					if event.key == K_p:
						print(self.mode)
					#KEYS FOR JOHN
					if event.key == K_UP:
						self.john.jump()
					if event.key == K_LEFT:
						self.john.moveLeftStart()
					if event.key == K_RIGHT:
						self.john.moveRightStart()
					if event.key == K_KP0:
						self.john.throwCarrot()

					#KEYS FOR REGIS
					if event.key == K_w:
						self.regis.jump()
					if event.key == K_a:
						self.regis.moveLeftStart()
					if event.key == K_d:
						self.regis.moveRightStart()
					if event.key == K_e:
						self.regis.throwCarrot()

					if event.key == K_c:
						self.level.addCarrot()

					if event.key == K_ESCAPE:
						self.active = False
						self.john.moveLeftStop()
						self.john.moveRightStop()
						self.regis.moveLeftStop()
						self.regis.moveRightStop()

				elif event.type == KEYUP:
					if event.key == K_LEFT:
						self.john.moveLeftStop()
					if event.key == K_RIGHT:
						self.john.moveRightStop()
					if event.key == K_a:
						self.regis.moveLeftStop()
					if event.key == K_d:
						self.regis.moveRightStop()

				#IF A RABBIT IS TOUCHED
				elif event.type == USEREVENT + 1:
					print("touche")
					if self.john.isTouched():
						self.john.moveLeftStop()
						self.john.moveRightStop()

					elif self.regis.isTouched():
						self.regis.moveLeftStop()
						self.regis.moveRightStop()

				elif event.type == USEREVENT + 2:
					print("plus touche")

			self.screen.blit(self.backgroundImage, self.backgroundRect, self.backgroundRect)

			#LEVEL UPDATE
			self.level.update()

			#RABBITS UPDATE
			self.john.update()
			self.regis.update()

			#TOOLBAR UPDATE
			self.toolbar.update(self.john, self.regis)

			#BUTTERFLIES UPDATE
			self.prey.update()
			for b in self.butterflies:
				b.update()

			#NEW CARROTS
			if(self.deltaCarrot == self.timeCarrot * 3600):
				self.level.addCarrot()
				self.deltaCarrot = 0
				self.timeCarrot = random.randint(1, 4)
			else:
				self.deltaCarrot += 1

			winner = self.checkWinner()
			if winner:
				pygame.mouse.set_visible(1)
				return True, WinnerMenu.WinnerMenu(self.screen, winner)

		else:
			pygame.mouse.set_visible(1)

			for event in pygame.event.get():
				if event.type == QUIT or (key[K_F4] and key[K_LALT]):
					return False, self

				elif event.type == MOUSEBUTTONDOWN:
					mse = pygame.mouse.get_pos()

					if self.pauseMenu.buttons["resume"].onButton(mse):
						self.buttonSound.play()
						self.active = True

					elif self.pauseMenu.buttons["loadlevel"].onButton(mse):
						self.buttonSound.play()
						rabbit1 = {"color": self.regis.getColor(), "name": self.regis.getName()}
						rabbit2 = {"color": self.john.getColor(), "name": self.john.getName()}
						return True, LoadLevelMenu.LoadLevelMenu(self.screen, "Game", [rabbit1, rabbit2, self.mode])

					elif self.pauseMenu.buttons["mainMenu"].onButton(mse):
						self.buttonSound.play()
						return True, MainMenu.MainMenu(self.screen)

				elif event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						self.active = True

			self.pauseMenu.update()

		pygame.display.update()

		return True, self

	def checkWinner(self):
		if self.mode == "time":
			if pygame.font:
				font = pygame.font.Font(None, 20)
				text = font.render(str(int((self.timer/3600)%60)) + ":" + str(int((self.timer/60)%60)).zfill(2), 1, (10, 10, 10))
				textpos = text.get_rect(centerx=(self.screen.get_width() - 200)/2, y=20)
				self.screen.blit(text, textpos)

			if self.timer <= 0:
				if self.regis.getPoints() > self.john.getPoints():
					return self.regis.getName()
				elif self.john.getPoints() > self.regis.getPoints():
					return self.john.getName()
				else:
					return "draw"

		elif self.mode == "score":
			if self.regis.getPoints() == 5:
				return self.regis.getName()
			elif self.john.getPoints() == 5:
				return self.john.getName()

		return ""