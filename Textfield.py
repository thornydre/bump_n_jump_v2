#!/usr/bin/python

import pygame
from pygame.locals import *
import os.path


class Textfield():
	def __init__(self, font_size=30, background_color=(150, 150, 150), text_color=(50, 50, 50), cursor_color=(50, 50, 50), x=0, y=0, width=250, height=35, placeholder="", limit=20):
		pygame.font.init()

		self.selected = False

		self.screen = pygame.display.get_surface()

		# Background variables
		self.background_color = background_color
		self.background_rect = pygame.Rect(x, y, width, height)

		# Text variables
		self.text_color = text_color
		self.input_string = placeholder # Inputted text
		self.font_object = pygame.font.Font(pygame.font.match_font(""), font_size)
		self.textfield_rect = pygame.Rect(x + 5, y + (height - self.font_object.get_height()) * 0.65, width, height)

		# Vars to make keydowns repeat after user pressed a key for some time:
		self.keyrepeat_counters = {} # {event.key: (counter_int, event.unicode)} (look for "***")
		self.keyrepeat_intial_interval_ms = 35

		# Things cursor:
		self.cursor_color = cursor_color
		self.cursor_rect = pygame.Rect(x, y + 3, 1, font_size * 0.9)
		self.cursor_position = len(self.input_string)
		self.cursor_visible = True
		self.cursor_switch_ms = 40
		self.cursor_ms_counter = 0

		self.limit = limit


	def event_listener(self, event):
		if self.selected:
			if event.type == KEYDOWN:
				self.cursor_visible = True # So the user sees where he writes

				# If none exist, create counter for that key:
				if not event.key in self.keyrepeat_counters:
					self.keyrepeat_counters[event.key] = [0, event.unicode]

				if event.key == K_BACKSPACE: # FIXME: Delete at beginning of line?
					self.input_string = self.input_string[:max(self.cursor_position - 1, 0)] + self.input_string[self.cursor_position:]

					# Subtract one from cursor_pos, but do not go below zero:
					self.cursor_position = max(self.cursor_position - 1, 0)
				elif event.key == K_DELETE:
					self.input_string = self.input_string[:self.cursor_position] + self.input_string[self.cursor_position + 1:]

				elif event.key == K_RETURN:
					return True

				elif event.key == K_RIGHT:
					# Add one to cursor_pos, but do not exceed len(input_string)
					self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

				elif event.key == K_LEFT:
					# Subtract one from cursor_pos, but do not go below zero:
					self.cursor_position = max(self.cursor_position - 1, 0)

				elif event.key == K_END:
					self.cursor_position = len(self.input_string)

				elif event.key == K_HOME:
					self.cursor_position = 0

				elif event.key == K_TAB:
					pass

				else:
					# If no special key is pressed, add unicode of key to input_string
					if len(self.input_string) < self.limit:
						self.input_string = self.input_string[:self.cursor_position] + event.unicode + self.input_string[self.cursor_position:]
						self.cursor_position += len(event.unicode) # Some are empty, e.g. K_UP

			elif event.type == KEYUP:
				# *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
				if event.key in self.keyrepeat_counters:
					del self.keyrepeat_counters[event.key]

			# Update key counters:
			for key in self.keyrepeat_counters :
				# self.keyrepeat_counters[key][0] += self.clock.get_time() # Update clock
				self.keyrepeat_counters[key][0] += 1 # Update clock
				# Generate new key events if enough time has passed:
				if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
					self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - 15

					event_key, event_unicode = key, self.keyrepeat_counters[key][1]
					pygame.event.post(pygame.event.Event(KEYDOWN, key=event_key, unicode=event_unicode))

		return False


	def update(self):
		if self.selected:
			# Draw background
			pygame.draw.rect(self.screen, self.background_color, self.background_rect)

			# Draw text
			self.screen.blit(self.font_object.render(self.input_string, True, self.text_color), self.textfield_rect)

			# Draw cursor
			self.cursor_ms_counter += 1
			if self.cursor_ms_counter >= self.cursor_switch_ms:
				self.cursor_ms_counter %= self.cursor_switch_ms
				self.cursor_visible = not self.cursor_visible

			if self.cursor_visible:
				cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
				if self.cursor_position > 0:
					cursor_y_pos -= self.cursor_rect.width
				self.cursor_rect.x = self.textfield_rect.x + cursor_y_pos
				pygame.draw.rect(self.screen, self.cursor_color, self.cursor_rect)

		else:
			# Draw background
			pygame.draw.rect(self.screen, self.background_color, self.background_rect)

			# Draw text
			self.screen.blit(self.font_object.render(self.input_string, True, self.text_color), self.textfield_rect)


	def onTextfield(self, x_y):
		(x, y) = x_y
		if x >= self.background_rect.x and x <= (self.background_rect.x + self.background_rect.w) and y >= self.background_rect.y and y <= (self.background_rect.y + self.background_rect.h):
			return True
		else:
			return False


	def enable(self):
		self.selected = True


	def disable(self):
		self.selected = False


	def get_selected(self):
		return self.selected


	def get_surface(self):
		return self.surface


	def get_text(self):
		return self.input_string


	def get_cursor_position(self):
		return self.cursor_position


	def set_text_color(self, color):
		self.text_color = color


	def set_cursor_color(self, color):
		self.cursor_surface.fill(color)
