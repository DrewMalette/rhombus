#

import pygame

from .mob import *
import mechanics

class Player(Mob):
    def __init__(self, game, filename):
        Mob.__init__(self, game, filename)
        self.uid = "player" # overrides the uid set by filename
        self.game.mob_db[self.uid] = self
        self.in_dialogue = False
        
        self.action = mechanics.Action(self)
        self.statblock = None
        self.equip = None # need a different name for this; gear?
                
    def update(self):
        self.base_update() # defined in Mob
        self.moving = bool(self.game.controller.x_axis or self.game.controller.y_axis)	
        self.move(self.game.controller.x_axis, self.game.controller.y_axis)
        if self.game.controller.pressed_a == 1:
            self.action.interact()

