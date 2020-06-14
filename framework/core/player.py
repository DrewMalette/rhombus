
import pygame

from .mob import *

class Player(Mob):

	def __init__(self, game, filename, name):
	
		Mob.__init__(self, game, filename, name)
		
		self.action = pygame.Rect(0,0,12,12)
		
	def interact(self): # think of a better name (interact?)

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
		
		self.move(self.game.controller.x_axis, self.game.controller.y_axis)
		
		if self.game.controller.pressed_a == 1:
			self.interact()

