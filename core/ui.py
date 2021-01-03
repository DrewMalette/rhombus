import pygame

class UserInterface:
    def __init__(self, game, theme):
        self.game = game
        self.game.ui = self
        self.nodes = {} # a dict of UI objects
        
        self.bg_colour = theme["BGCOLOUR"] # druple (r,g,b)
        self.bg_alpha = theme["BGALPHA"] # int (0-255)
        self.txt_colour = theme["TXTCOLOUR"] # druple (r,g,b)
        self.hp_recover_colour = theme["HPRECOVER"] # (0,0xff,0)
        self.hp_damage_colour = theme["HPDAMAGE"] # (0xff,0,0)
        self.txt_font = pygame.font.Font(None, 24) # basic font for DialogueBox and DialogueSelector, etc.,
        self.hp_font = pygame.font.Font(None, 12) # used for the numbers that appear when a Mob's HP changes
        
    def add_node(self, idstr, ui_obj):
        if idstr in self.nodes:
            print("{} is already assigned to a node".format(idstr))
            pygame.quit()
        else:
            ui_obj.parent = self
            self.nodes[idstr] = ui_obj
            
    def __getitem__(self, key): return self.nodes[key]
