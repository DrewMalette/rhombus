#

import pygame

class Action(pygame.Rect):

	def __init__(self, mob):
	
		pygame.Rect.__init__(self, (0,0,12,12))
	
		self.mob = mob
		if self.mob: self.mob.action = self
		
	def interact(self): # this comes from the Player class

		if self.mob.facing == "north":
			x = (self.mob.x + self.mob.w / 2) - (self.mob.w / 2) + 1
			y = self.mob.y - self.h - 7
		elif self.mob.facing == "south":
			x = (self.mob.x + self.mob.w / 2) - (self.w / 2) + 1
			y = self.mob.y + self.mob.h
		elif self.mob.facing == "west":
			x = self.mob.x - self.w
			y = (self.mob.y + self.mob.h / 2) - (self.h / 2) - 3
		elif self.mob.facing == "east":
			x = self.mob.x + self.mob.w + 2
			y = (self.mob.y + self.mob.h / 2) - (self.h / 2) - 3
			
		self.x = x
		self.y = y
