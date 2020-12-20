# game_camera.py:

import operator
import pygame

class Camera(pygame.Rect):
    def __init__(self, uid, game, x=0, y=0):    
        self.uid = uid
        self.game = game
        w,h = self.game.display.get_size()
        pygame.Rect.__init__(self, (x,y,w,h))
        
        self.tilesize = 0 # TODO where does this get set?
        self.cols = 0
        self.rows = 0
        self.blank = None
        self.following = None        
        self.scene = None
        
    def tile_prep(self, layer, col, row):
        x_offset = self.x % self.tilesize
        y_offset = self.y % self.tilesize

        c_index = int(self.x / self.tilesize + col)
        r_index = int(self.y / self.tilesize + row)
    
        index = self.scene.get_tile(layer, c_index, r_index)

        x = col * self.tilesize - x_offset
        y = row * self.tilesize - y_offset
        
        if index != "0":
            tile = self.scene.tileset[index]
            return (tile, x, y)
        else:			
            return ("0", x, y)
    
    def y_sort(self):
        return sorted(self.scene.get_mobs(), key=operator.attrgetter('y'))
            
    def update(self):    
        x,y = self.following.center
        
        if x > self.w / 2:
            self.x = x - self.w / 2
        elif x <= self.w / 2:
            self.x = 0
        
        if y > self.h / 2:
            self.y = y - self.h / 2
        elif y <= self.h / 2:
            self.y = 0
    
        if self.x + self.w > self.scene.cols * self.tilesize:
            self.x = self.scene.cols * self.tilesize - self.w
        elif self.x < 0:
            self.x = 0
            
        if self.y + self.h > self.scene.rows * self.tilesize:
            self.y = self.scene.rows * self.tilesize - self.h
        elif self.y < 0:
            self.y = 0

    def render(self):    
        for row in range(self.rows): # draw the bottom and middle tile layers
            for col in range(self.cols):
                x_offset = self.x % self.tilesize
                y_offset = self.y % self.tilesize

                c_index = int(self.x / self.tilesize + col)
                r_index = int(self.y / self.tilesize + row)
        
                bottom_i = self.scene.get_tile("bottom", c_index, r_index)
                middle_i = self.scene.get_tile("middle", c_index, r_index)

                c = col * self.tilesize - x_offset
                r = row * self.tilesize - y_offset
                
                if bottom_i != "0":
                    bottom_t = self.scene.tileset[bottom_i]
                    self.game.display.blit(bottom_t, (c,r))
                elif bottom_i == "0":
                    self.game.display.blit(self.blank, (c,r))

                if middle_i != "0":
                    middle_t = self.scene.tileset[middle_i]
                    self.game.display.blit(middle_t, (c,r))

        #if self.scene.loot: # TODO merge this with sprites for the y_sort
        #	for loot in self.scene.loot.values():
        #		loot.render(self.game.display, x_offset = -self.x, y_offset = -self.y)

        if self.scene.mobs: # draw the sprites
            #for sprite in self.scene.sprites.values():
            for sprite in self.y_sort():
                sprite.render(self.game.display, x_off = -self.x, y_off = -self.y)
        
        for row in range(self.rows): # draw the top layer
            for col in range(self.cols):
                tile, x, y = self.tile_prep("top", col, row)
                if tile != "0": self.game.display.blit(tile, (x, y))
        
        if self.game.debug_info_on == 1:
            x = self.game.player.action.x - self.x
            y = self.game.player.action.y - self.y
            w = self.game.player.action.w
            h = self.game.player.action.h
            rect = (x,y,w,h)
            pygame.draw.rect(self.game.display, (0xff,0,0), rect, 1)

