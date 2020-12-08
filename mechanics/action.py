#

import pygame

class Action(pygame.Rect):
    def __init__(self, mob):
        pygame.Rect.__init__(self, (0,0,12,12)) # defaults to basic interaction rect
        self.mob = mob
        
    def interact(self):
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
        self.w = 12
        self.h = 12
        
        for mob in self.mob.scene.mobs:
            if self.colliderect(self.mob.game.mob_db[mob]):
                if self.mob.game.mob_db[mob] is not self.mob:
                    print(self.mob.game.mob_db[mob].uid)
        
    def attack(self, target):	
        # self.w, self.h = self.mob.weapon.get_size()
        pass
