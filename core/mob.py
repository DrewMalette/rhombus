#

import os
import pygame
from . import utilities
from . import scene_sprite

heading = { (0,-1): "north", (0,1): "south", (-1,0): "west", (1,0): "east",
            (-1,-1): "north", (1,1): "south", (-1,1): "west", (1,-1): "east" }

north_rect = lambda mob: (mob.x, mob.y - mob.h)
south_rect = lambda mob: (mob.x, mob.y + mob.h)
west_rect = lambda mob: (mob.x - mob.w, mob.y)
east_rect = lambda mob: (mob.x + mob.w, mob.y)

talk_rect = { "north": north_rect, "south": south_rect, "west": west_rect, "east": east_rect }

# basic mob class; enough to appear in a Scene,
#  but no other functionality, not even mechanics.Action
class Mob(pygame.Rect):
    pattern = [0,1,0,2]
    facings = { "south": 0, "north": 1, "east": 2, "west": 3 }

    def __init__(self, game, filename, uid): # filename of spritesheet
        self.game = game
        self.uid = uid
        self.game.mob_db[self.uid] = self
        
        self.sprite = filename
        if self.sprite not in self.game.sprite_db:
            scene_sprite.Sprite(self.sprite, game)
            print("spritesheet '{}' not found; loading".format(self.sprite))
        pygame.Rect.__init__(self, self.game.sprite_db[self.sprite].rect)
                
        self.moving = False
        self.facing = "south"
        self.frame = 0
        self.speed = 2
        self.alive = True # going to StatBlock?
        self.dying = False
        self.opacity = 255
        self.scene = None
                        
    def spawn(self, filename): # filename = Scene.uid and dict key    
        self.scene = self.game.scene_db[filename]
        col, row = self.scene.defaults[self.uid]
        self.place(col, row)
        self.facing = "south"
        
    def place(self, col, row):        
        self.x = col * self.scene.tilesize + (self.scene.tilesize - self.w) / 2
        self.y = row * self.scene.tilesize + (self.scene.tilesize - self.h) - 4

    def move(self, x_axis, y_axis):
        x = (not self.collision(x_axis * self.speed, 0)) * (x_axis * self.speed)
        y = (not self.collision(0, y_axis * self.speed)) * (y_axis * self.speed)
        self.move_ip(x*self.moving, y*self.moving)
        if x_axis != 0 or y_axis != 0: self.facing = heading[(x_axis,y_axis)]

    def collision(self, x_axis, y_axis):
        for c in range(4):
            xm = ((self.x + x_axis * self.speed) + (c % 2) * self.w)
            ym = ((self.y + y_axis * self.speed) + int(c / 2) * self.h)

            col = int(xm / self.scene.tilesize) # is this slow?
            row = int(ym / self.scene.tilesize)

            if self.scene.get_tile("collide", col, row) != "0":
                return True

        for mob in self.scene.get_mobs():
            if mob is not self:
                xm = self.speed * x_axis + self.x
                ym = self.speed * y_axis + self.y
                if mob.colliderect((xm, ym, self.w, self.h)):
                    return True
        return False
        
    def base_update(self):
        # self.statblock.upkeep() TODO move this to a derivative class
        self.frame += self.moving & (self.game.tick % 12 == 0) * 1
        self.frame = self.frame % len(self.pattern) * self.moving
        
    def update(self): # overridden by classes derived
        self.base_update()
        
    def render(self, surface, x_off=0, y_off=0):
        frame = self.pattern[self.frame]
        facing = self.facings[self.facing]
        x = (self.x - self.game.sprite_db[self.sprite].x_off) + x_off
        y = (self.y - self.game.sprite_db[self.sprite].y_off) + y_off
        surface.blit(self.game.sprite_db[self.sprite].get_cell(frame, facing), (x,y))
        
