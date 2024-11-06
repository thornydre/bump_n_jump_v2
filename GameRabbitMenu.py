#!/usr/bin/python

import pygame
import Resources
import Game
import PlayModeMenu
from pygame.locals import *
from Button import Button
from Slider import Slider
from Checkbox import Checkbox
from Textfield import Textfield
from Animation import Animation


class GameRabbitMenu():
	pygame.mixer.pre_init(44100, -16, 2, 1024)
	pygame.mixer.init()

	def __init__(self, surface):
		self.screen = surface
		screen_rect = self.screen.get_rect()

		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill((50, 50, 50))

		self.buttonSound = pygame.mixer.Sound("resources/sound/button.wav")
		self.buttonSound.set_volume(float(Resources.getOptionValue("sound"))/100)

		self.textfields = {}

		self.textfields["name1"] = Textfield(x=screen_rect.w/4 - 250/2, y=33, placeholder="Regis")
		self.textfields["name2"] = Textfield(x=screen_rect.w - screen_rect.w/4 - 250/2, y=33, placeholder="John")

		self.sliders = {}

		self.sliders["red1"] = Slider(screen_rect.w/4 - 200/2, 100, 200, 200, 255)
		self.sliders["green1"] = Slider(screen_rect.w/4 - 200/2, 150, 200, 50, 255)
		self.sliders["blue1"] = Slider(screen_rect.w/4 - 200/2, 200, 200, 50, 255)

		self.sliders["red2"] = Slider(screen_rect.w - screen_rect.w/4 - 200/2, 100, 200, 50, 255)
		self.sliders["green2"] = Slider(screen_rect.w - screen_rect.w/4 - 200/2, 150, 200, 50, 255)
		self.sliders["blue2"] = Slider(screen_rect.w - screen_rect.w/4 - 200/2, 200, 200, 200, 255)

		self.currentSlider = None

		self.rabbitAnim1 = Animation("rabbit", 30)
		self.rabbitAnim1.setFrameRange(1, 8)
		self.rabbitAnim1.flipAnim()
		self.rabbitAnim1.setPos([self.screen.get_width()/4 - 21, 300])
		self.rabbit1Sprite = pygame.sprite.GroupSingle(self.rabbitAnim1)

		self.rabbitAnim2 = Animation("rabbit", 30)
		self.rabbitAnim2.setFrameRange(1, 8)
		self.rabbitAnim2.setPos([self.screen.get_width() - self.screen.get_width()/4 - 21, 300])
		self.rabbit2Sprite = pygame.sprite.GroupSingle(self.rabbitAnim2)

		self.updateColors()

		self.mode_radios = {}

		self.mode_radios["unlimited"] = Checkbox(self.screen.get_width()/2 - 50, 250, "Unlimited", True, True)
		self.mode_radios["time"] = Checkbox(self.screen.get_width()/2 - 50, 275, "Time Out", False, True)
		self.mode_radios["score"] = Checkbox(self.screen.get_width()/2 - 50, 300, "Score", False, True)

		self.buttons = {}

		self.buttons["play"] = Button(self.screen.get_width() - self.screen.get_width()/4 - 200/2, 450, 200, 40, "PLAY")
		self.buttons["back"] = Button(self.screen.get_width()/4 - 200/2, 450, 200, 40, "BACK")


	def update(self):
		key = pygame.key.get_pressed()
		mouse = pygame.mouse.get_pressed()

		for event in pygame.event.get():
			if event.type == QUIT or (key[K_F4] and key[K_LALT]):
				return False, self

			elif event.type == MOUSEBUTTONDOWN:
				mse = pygame.mouse.get_pos()

				for textfield in self.textfields.values():
					if textfield.onTextfield(mse):
						textfield.enable()
					else:
						textfield.disable()

				for sliderKey, slider in self.sliders.items():
					if slider.onSlider(mse):
						slider.setValueByMousePos(mse[0])
						self.currentSlider = sliderKey

						self.updateColors()

				out_radios = True
				for mode_radio in self.mode_radios.values():
					if mode_radio.onCheckbox(mse):
						out_radios = False
						mode_radio.check()
					else:
						if mode_radio.isChecked():
							radio_on = mode_radio
							mode_radio.uncheck()

				if out_radios:
					radio_on.check()

				if self.buttons["play"].onButton(mse):
					self.buttonSound.play()
					rabbit1 = {
						"color": self.color1,
						"name": self.textfields["name1"].get_text()
					}
					rabbit2 = {
						"color": self.color2,
						"name": self.textfields["name2"].get_text()
					}
					for mode_radio_key, mode_radio_val in self.mode_radios.items():
						if mode_radio_val.isChecked():
							mode = mode_radio_key
					return True, Game.Game(self.screen, rabbit1, rabbit2, mode)

				elif self.buttons["back"].onButton(mse):
					self.buttonSound.play()
					return True, PlayModeMenu.PlayModeMenu(self.screen)

			elif event.type == MOUSEMOTION:
				mse = pygame.mouse.get_pos()

				if self.currentSlider != None and mouse[0]:
					self.sliders[self.currentSlider].setValueByMousePos(mse[0])

					self.updateColors()

			elif event.type == MOUSEBUTTONUP:
				if self.currentSlider != None:
					self.currentSlider = None
			
			elif event.type == KEYDOWN or event.type == KEYUP:
				for textfield in self.textfields.values():
					textfield.event_listener(event)

				if event.type == KEYDOWN:
					if event.key == K_TAB:
						for textfield in self.textfields.values():
							if textfield.get_selected():
								textfield.disable()
							else:
								textfield.enable()

		self.screen.blit(self.background, self.background.get_rect(), self.background.get_rect())

		for textfield in self.textfields.values():
			textfield.update()

		for slider in self.sliders.values():
			slider.update()

		self.rabbitAnim1.update()
		self.rabbit1Sprite.update()
		self.rabbit1Sprite.draw(self.screen)

		self.rabbitAnim2.update()
		self.rabbit2Sprite.update()
		self.rabbit2Sprite.draw(self.screen)

		for mode_radio in self.mode_radios.values():
			mode_radio.update()

		for button in self.buttons.values():
			button.update()

		pygame.display.update()

		return True, self


	def updateColors(self):
		self.color1 = (
			self.sliders["red1"].getValue(),
			self.sliders["green1"].getValue(),
			self.sliders["blue1"].getValue()
		)

		self.color2 = (
			self.sliders["red2"].getValue(),
			self.sliders["green2"].getValue(),
			self.sliders["blue2"].getValue()
		)

		self.rabbitAnim1.updateColor(self.color1)
		self.rabbitAnim2.updateColor(self.color2)
