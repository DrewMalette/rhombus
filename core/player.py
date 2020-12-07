#

import pygame

from .mob import *
import mechanics

class Player(Mob):

    def __init__(self, game, filename):
        Mob.__init__(self, game, filename)
        self.uid = "player" # overrides the uid set by filename
        self.game.mob_db[self.uid] = self
        self.action = None
        self.statblock = None
        self.equip = None # I gotta find a different name for this
        self.in_dialogue = False
        self.action = mechanics.Action()
        
    def update(self):
        self.base_update()
        self.moving = bool(self.game.controller.x_axis or self.game.controller.y_axis)	
        self.move(self.game.controller.x_axis, self.game.controller.y_axis)
        if self.game.controller.pressed_a == 1:
            self.action.interact(self)

