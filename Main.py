#!/usr/bin/python

import pygame
import Resources
from pygame.locals import *
import MainMenu


class BumpNJump():
	def __init__(self):
		pygame.init()

		screen_size = (1000, 600)

		if(Resources.getOptionValue("fullscreen") == 1):
			pygame.display.set_mode(screen_size, FULLSCREEN)
		else:
			pygame.display.set_mode(screen_size, 0, 32)
		pygame.display.set_caption("Bump'N'Jump")

		pygame.mixer.music.load("resources/sound/music.wav")
		pygame.mixer.music.set_volume(float(Resources.getOptionValue("music"))/100)
		pygame.mixer.music.play(-1)

		screen = pygame.display.get_surface()
		surface = pygame.Surface(screen_size)

		currentScene = MainMenu.MainMenu(surface)

		clock = pygame.time.Clock()

		game = True

		while game:
			game, currentScene = currentScene.update()
			pygame.event.pump()

			screen.blit(pygame.transform.scale(surface, screen_size), (0, 0))

			clock.tick(60)

if __name__ == '__main__': 
	BumpNJump()