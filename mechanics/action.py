#

import pygame

class Action(pygame.Rect):

	def __init__(self):
	
		pygame.Rect.__init__(self, (0,0,12,12))
		
	def interact(self, mob): # this comes from the Player class

		if mob.facing == "north":
			x = (mob.x + mob.w / 2) - (mob.w / 2) + 1
			y = mob.y - self.h - 7
		elif mob.facing == "south":
			x = (mob.x + mob.w / 2) - (self.w / 2) + 1
			y = mob.y + mob.h
		elif mob.facing == "west":
			x = mob.x - self.w
			y = (mob.y + mob.h / 2) - (self.h / 2) - 3
		elif mob.facing == "east":
			x = mob.x + mob.w + 2
			y = (mob.y + mob.h / 2) - (self.h / 2) - 3
			
		self.x = x
		self.y = y
