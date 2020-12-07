
import os
import pygame
from . import filepaths
from . import utilities

class Sprite(pygame.Rect):
    def __init__(self, filename, game):
        self.filename = filename
        self.game = game
        self.game.sprite_db[self.filename] = self
        
        data = utilities.load_mob(os.path.join(filepaths.image_path, filename))
        print(data["rect"])
        pygame.Rect.__init__(self, data["rect"])
        self.cols = data["cols"]
        self.rows = data["rows"]
        self.cells = data["cells"]
        self.x_off, self.y_off = data["offsets"]
        
    def get_cell(self, col, row):

        if (col >= 0 and col < self.cols) and (row >= 0 and row < self.rows):
            return self.cells[self.cols*row+col]
        else:
            print("col or row out of sprite's bounds")
            pygame.quit()
            exit()
