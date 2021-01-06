# game_controller.py:

import pygame

class Controller:

    buttons = ["a", "b", "x"] # ["a","b","x","y"]

    def __init__(self, game):    
        self.game = game
        
        self.x_axis = self.y_axis = 0
        self.x_repeat = self.y_repeat = False
        self.x_pressed = self.y_pressed = False # USE THESE!!! Yes but actually no
        self.x_tick = self.y_tick = 0
        
        self.y_axis_sr = 0 # special repeat; delayed repeat
        self.y_axis_phase1 = 0 # for the first, and longer, delay
        self.y_axis_phase2 = 0 # for the constant and shorter delay
        
        # buttons: A, B, X, Y
        self.pressed_a_held = False
        self.pressed_a = 0
        self.held_a = 0
        
        self.pressed_b_held = False
        self.pressed_b = 0
        self.held_b = 0
        
        self.pressed_x_held = False
        self.pressed_x = 0
        self.held_x = 0
        
        self.exit = 0
        
        self.pressed_f1 = False
        
    def press(self, button):    
        #print("pressing "+button)
    
        attribute = "pressed_"+button
        setattr(self, attribute, 1)
        setattr(self, attribute+"_held", True)

    def flush(self):        
        for button in self.buttons: setattr(self, "pressed_"+button, 0)
        self.exit = 0
        self.y_axis_sr = 0
        
    def base_update(self):
        pygame.event.pump()
        if self.x_axis != 0 and not self.x_pressed:
            self.x_tick = pygame.time.get_ticks()
            self.x_pressed = True
        elif self.x_axis == 0 and self.x_pressed:
            self.x_pressed = False
        self.x_repeat = self.x_pressed and (pygame.time.get_ticks() - self.x_tick >= 800)
        
        if self.y_axis != 0 and not self.y_pressed:
            self.y_pressed = True
            self.y_tick = pygame.time.get_ticks()
            self.y_axis_sr = 1 # special repeat
            self.y_axis_phase1 = 1
        
        if self.y_pressed:
            if self.y_axis_phase1:
                if pygame.time.get_ticks() - self.y_tick >= 800:
                    self.y_axis_phase2 = 1
                    self.y_axis_phase1 = 0
                    self.y_tick = pygame.time.get_ticks()
            elif self.y_axis_phase2:
                if pygame.time.get_ticks() - self.y_tick >= 100:
                    self.y_axis_sr = 1
                    self.y_tick = pygame.time.get_ticks()
                
        if self.y_axis == 0 and self.y_pressed:
            self.y_pressed = False

    def y_ax_sr(self):
    
        return self.y_axis_sr * self.y_axis
