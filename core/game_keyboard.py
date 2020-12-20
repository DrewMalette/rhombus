# game_keyboard.py:

import pygame
from . import game_controller

class Keyboard(game_controller.Controller):
    def __init__(self, game):    
        game_controller.Controller.__init__(self, game)
            
    def update(self):        
        keys = pygame.key.get_pressed()
        
        self.x_axis = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT] 
        self.y_axis = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        
        self.flush()
            
        #self.pressed_a = 0
        self.held_a = keys[pygame.K_RCTRL]
        self.held_b = keys[pygame.K_RSHIFT]
        self.held_x = keys[pygame.K_RETURN]
        
        if keys[pygame.K_RCTRL] == 1 and not self.pressed_a_held:
            self.press("a")
        elif keys[pygame.K_RCTRL] == 0 and self.pressed_a_held:
            self.pressed_a_held = False
        if keys[pygame.K_RSHIFT] == 1 and not self.pressed_b_held:
            self.press("b")
        elif keys[pygame.K_RSHIFT] == 0 and self.pressed_b_held:
            self.pressed_b_held = False
        if keys[pygame.K_RETURN] == 1 and not self.pressed_x_held:
            self.press("x")
        elif keys[pygame.K_RETURN] == 0 and self.pressed_x_held:
            self.pressed_x_held = False
                    
        if keys[pygame.K_ESCAPE] == 1: self.exit = 1
            
        self.base_update()

