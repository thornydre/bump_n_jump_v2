#!/usr/bin/python

import pygame
import random


class Background():
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.screen_rect = self.screen.get_rect()

		self.background_color = pygame.Color(10, 22, 32)

		self.leaves_list = [[
			[random.randint(0, self.screen_rect.w), random.randint(0, self.screen_rect.h)],
			random.randint(5, 50),
			pygame.Color(
				random.randint(160, 180),
				random.randint(101, 121),
				random.randint(18, 38)
			)
		] for i in range(100)]

		self.dir_vec = [2, 5]

		self.prev_mse = pygame.mouse.get_pos()
		self.offset_vec = [0.0, 0.0]
		self.final_offset = [0.0, 0.0]

	def update(self):
		mse = pygame.mouse.get_pos()
		self.screen.fill(self.background_color)

		self.offset_vec[0] += (mse[0] - self.prev_mse[0]) / 20.0
		self.offset_vec[1] += (mse[1] - self.prev_mse[1]) / 20.0

		self.final_offset[0] += self.offset_vec[0]
		self.final_offset[1] += self.offset_vec[1]

		self.offset_vec[0] *= 0.99
		self.offset_vec[1] *= 0.99

		self.final_offset[0] *= 0.99
		self.final_offset[1] *= 0.99

		for i, leaf in enumerate(self.leaves_list):
			pos = [leaf[0][0] + self.final_offset[0] * i / 1000.0, leaf[0][1] + self.final_offset[1] * i / 1000.0]

			if leaf[0][0] < self.screen_rect.left + 50 or leaf[0][1] < self.screen_rect.bottom + 50:
				pygame.draw.circle(self.screen, leaf[2], pos, leaf[1])

		self.prev_mse = mse

