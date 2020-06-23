#

import pygame

from .mob import *
import mechanics
from mechanics import action

class Player(Mob):

	def __init__(self, uid, game_obj, filename):
	
		Mob.__init__(self, uid, game_obj, filename)
		
		self.action = None
		self.statblock = None
		self.equip = None
		self.in_dialogue = False
		
		action.Action(self)
		
	def update(self):
	
		self.base_update()
		
		self.move(self.game_obj.controller.x_axis, self.game_obj.controller.y_axis)
		
		if self.game_obj.controller.pressed_a == 1:
			self.action.interact()

