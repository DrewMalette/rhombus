#

import pygame

from .mob import *
import mechanics

health_potion = { "icon": "potion_ico.png", "name": "Health Potion", "description": "Heals 50 health" }
strength_potion = { "icon": "potion_ico.png", "name": "Strength Potion", "description": "Increases STR by 5 for 10 mins" }

class Player(Mob):
    def __init__(self, game, filename):
        Mob.__init__(self, game, filename, "player")
        self.game.mob_db[self.uid] = self
        self.in_dialogue = False
        
        # drop in mechanics; tailorable to your specifications
        self.action = mechanics.Action(self)
        self.statblock = None
        self.equip = None # need a different name for this; gear?
        
        self.inventory = { 0: None, 1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None }
        
        # debug
        self.add_loot(0, health_potion)
        self.add_loot(1, strength_potion)
    
    def add_loot(self, slot, loot, quantity=1):
        if slot >= 0 and slot < len(self.inventory):
            self.inventory[slot] = [loot, quantity]
        else:
            # self.game.script = inventory_full_dialogue
            # this problem right here is why I need a game.message list
            # self.game.msg_queue("inventory_full") # "text_list = [ "Your inventory is full", " ", " " ]
            print("inventory is full")
                
    def update(self):
        self.base_update() # defined in Mob
        self.moving = bool(self.game.controller.x_axis or self.game.controller.y_axis)	
        self.move(self.game.controller.x_axis, self.game.controller.y_axis)
        #if self.game.controller.pressed_a == 1:
        #    self.action.interact()

