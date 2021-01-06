#

import pygame

from . import mob
import mechanics
import data
from data.items import potions

class Player(mob.Mob):
    def __init__(self, game, filename):
        mob.Mob.__init__(self, game, filename, "player")
        self.game.mob_db[self.uid] = self
        self.in_dialogue = False
        
        self.name = "Drew" # obviously will be changed
        
        # drop in mechanics; tailorable to your specifications
        self.action = mechanics.Action(self)
        #self.statblock = mechanics.StatBlock(10,12,12,11,11,10)
        self.equip = None # need a different name for this; gear?
        
        self.inventory = { 0: None, 
                           1: None, 
                           2: None, 
                           3: None, 
                           4: None, 
                           5: None, 
                           6: None, 
                           7: None }
        
        # debug
        self.add_loot(0, potions.health_potion)
        self.add_loot(1, potions.strength_potion)
    
    def add_loot(self, slot, loot, quantity=1):
        if slot >= 0 and slot < len(self.inventory): # assert?
            self.inventory[slot] = [loot, quantity]
        else:
            # self.game.script = inventory_full_dialogue
            # this problem right here is why I need a game.message list
            # self.game.msg_queue("inventory_full") # "text_list = [ "Your inventory is full", " ", " " ]
            print("inventory is full")
    
    def check_quests(self): pass
    
    def update(self):
        self.base_update() # defined in Mob
        self.moving = bool(self.game.controller.x_axis or self.game.controller.y_axis)	
        self.move(self.game.controller.x_axis, self.game.controller.y_axis)
        #if self.game.controller.pressed_a == 1:
        #    self.action.interact()

