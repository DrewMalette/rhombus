import pygame

def draw_wrapper(pane, surface):

    label = pane.parent.font.render(pane.parent.v_string, 0, (0xff,0xff,0xff))
    
    x = pane.x + ((pane.w - label.get_width()) / 2)
    y = pane.y + ((pane.h - label.get_height()) / 2)
    
    surface.blit(label, (x,y))

# declare a UI_PlayerMenu before declaring UI_SubMenuPane
class UI_PlayerMenu:

    def __init__(self, uid, game_obj, rect, bindings, b_func):
    
        self.uid = uid
        self.game = game_obj
        self.x, self.y = rect[:2]
        self.bindings = bindings # []
        self.b_func = b_func # called when the B button is pressed
        
        self.value = 0
        self.v_string = list(self.bindings.keys())[self.value]
        self.visible = True
        self.returned = 0

        self.back = pygame.Surface(rect[2:]).convert_alpha()
        self.back.fill((0,0,0,127))
        
        self.font = pygame.font.Font(None, 24)
        
        self.child = None
        self.submenu = None #
        self.font_colour = (0xc0,0xc0,0xc0)
                
    def start(self, value=0):
    
        self.visible = True
        self.value = value
        self.v_string = list(self.bindings.keys())[self.value]
        self.returned = 0
        #self.game.controller.flush()
    
    def stop(self):
    
        self.visible = False
        self.returned = 1
        self.submenu = None
        #self.game.controller.flush()
    
    def update(self):
    
        self.returned = 0
    
        if self.submenu == None:
            if self.visible:
                if self.game.controller.y_axis_sr != 0:			
                    self.value = (self.value + self.game.controller.y_axis_sr * self.game.controller.y_axis) % len(self.bindings)
                    self.v_string = list(self.bindings.keys())[self.value]
                if self.game.controller.pressed_a:
                    if self.v_string in self.child.bindings:
                        self.submenu = self.child.bindings[self.v_string]
                        self.submenu.start()
                        self.game.controller.flush()
                    else:
                        self.bindings[self.v_string](self.game) #, self.game.display) # this is here just cuz
                        # TODO put a function here that works properly
                if self.game.controller.pressed_b:
                    self.b_func(self.game)
        else:
            self.submenu.update()
                    
    def render(self):
    
        if self.visible:
            self.game.display.blit(self.back, (self.x, self.y))
            
            if self.submenu == None:
                self.font_colour = (0xff,0xff,0xff)
            else:
                self.font_colour = (0xc0,0xc0,0xc0)

            for b in range(len(self.bindings)):	
                text = list(self.bindings.keys())[b] + " <" * (b == self.value)
                x = self.x + 5 # padding
                y = self.y + 7 * (b+1) + b * self.font.get_height() # 0:15; 1:40; 2:65
                #self.submenu.render()  *** OR ***
                # list(self.bindings.keys())[self.value].render()
                #label_image = self.game.ui_font.render(label, 0, (0xff,0xff,0xff))
                label_image = self.font.render(text, 0, self.font_colour)
                self.game.display.blit(label_image, (x,y))
                
            self.child.render()
            #draw_wrapper(self.child, self.game.display)

# needs a parent (UI_PlayerMenu) to work
class UI_SubMenuPane:

    def __init__(self, uid, parent, size):
    
        self.uid = uid
        self.parent = parent
        self.game = parent.game
        self.x = self.y = 0
        self.w, self.h = size

        self.parent.child = self
        self.x = self.parent.x + self.parent.back.get_width() + 10
        self.y = self.parent.y
        
        self.back = pygame.Surface(size).convert_alpha()
        self.back.fill((0,0,0,127))
        
        self.visible = True
        
        self.bindings = {}
        
    def render(self):
    
        if self.visible:
            self.game.display.blit(self.back, (self.x,self.y))
            key = list(self.parent.bindings.keys())[self.parent.value]
            if key in self.bindings:
                self.bindings[key].render()
            
