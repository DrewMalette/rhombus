#

import pygame

from .mob import *

class Player(Mob):

	def __init__(self, uid, game_obj, filename):
	
		Mob.__init__(self, uid, game_obj, filename)
		
		self.action = pygame.Rect(0,0,12,12)
		
		self.in_dialogue = False
		
	def interact(self):

		if self.facing == "north":
			x = (self.x + self.w / 2) - (self.w / 2) + 1
			y = self.y - self.action.h - 7
		elif self.facing == "south":
			x = (self.x + self.w / 2) - (self.action.w / 2) + 1
			y = self.y + self.h
		elif self.facing == "west":
			x = self.x - self.action.w
			y = (self.y + self.h / 2) - (self.action.h / 2) - 3
		elif self.facing == "east":
			x = self.x + self.w + 2
			y = (self.y + self.h / 2) - (self.action.h / 2) - 3
			
		self.action.x = x
		self.action.y = y
		
	def update(self):
	
		self.base_update()
		
		self.move(self.game_obj.controller.x_axis, self.game_obj.controller.y_axis)
		
		if self.game_obj.controller.pressed_a == 1:
			self.interact()

