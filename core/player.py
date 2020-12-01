#

import pygame

from .mob import *
import mechanics

class Player(Mob):

	def __init__(self, filename, game):
	
		Mob.__init__(self, filename, game)
		self.uid = "player" # overrides the uid set by filename
		
		self.action = None
		self.statblock = None
		self.equip = None # I gotta find a different name for this
		self.in_dialogue = False
		
		self.action = mechanics.Action()
		
	def update(self):
	
		self.base_update()
		
		self.move(self.game.controller.x_axis,
				  self.game.controller.y_axis)
		
		if self.game.controller.pressed_a == 1:
			self.action.interact(self)

