# game_gamepad.py:

from . import game_controller

class Gamepad(game_controller.Controller):

    def __init__(self, game_obj):    
        game_controller.Controller.__init__(self, game_obj)
        
        self.interface = pygame.joystick.Joystick(0)
        self.interface.init()
        
    def update(self):    
        self.x_axis = round(self.interface.get_axis(0))
        self.y_axis = round(self.interface.get_axis(1))
        
        self.flush()
        
        self.held_a = self.interface.get_button(1)
        self.held_b = self.interface.get_button(2)
        self.held_x = self.interface.get_button(0)

        if self.interface.get_button(1) and not self.pressed_a_held:
            self.press("a")
        elif not self.interface.get_button(1) and self.pressed_a_held:
            self.pressed_a_held = False
        if self.interface.get_button(2) and not self.pressed_b_held:
            self.press("b")
        elif not self.interface.get_button(2) and self.pressed_b_held:
            self.pressed_b_held = False
        if self.interface.get_button(0) and not self.pressed_x_held:
            self.press("x")
        elif not self.interface.get_button(0) and self.pressed_x_held:
            self.pressed_x_held = False
            
        if self.interface.get_button(4) and self.interface.get_button(5): self.exit = 1
        
        self.base_update()

