#

import pygame

class UI_Inventory(object): # will bind to a SubMenuPane and draw's relative to the SubMenuPane's x/y coordinates

    def __init__(self, game, uid, childpane):
    
        self.game = game
        self.uid = uid
        self.childpane = childpane # this is only used for rendering
        self.childpane.submenu_bindings[uid] = self
        #self.x, self.y = loc
        #self.w, self.h = size
        
        #self.back = pygame.Surface((self.w, self.h)).convert_alpha()
        #self.back.fill((0,0,0,127))
    
        #self.visible = False
    
        self.value = 0
        self.sel_value = 0
        self.selected = False
        
        print("UIInventory initialized")
    
    def normalize_cursor(self): # what does this do again?
    
        inv = self.game.player.inventory
        count = 0
        while inv[count] == None and count < 7:
            count += 1
        self.value = count
    
    def start(self):
    
        self.selected = False
        self.normalize_cursor()
        
        #self.game.uiQueue.append(self)
        #self.game.controlFocus = self
        #self.visible = True
                
    def stop(self):
    
        #self.visible = False
        #self.game.ui_pop() # change this to self.game.ui_pop()
        self.childpane.parent.submenu = None
        
    def is_empty(self):
    
        for i in range(8):
            if self.game.player.inventory[i] != None:
                return False
        return True
    
    def update(self):
    
        y_axis = self.game.controller.y_axis_sr
        
        a_button = self.game.controller.pressed_a
        b_button = self.game.controller.pressed_b
        
        if y_axis != 0:
            inv = self.game.player.inventory
            if not self.selected:
                self.value = (self.value + y_axis) % 8
                while inv[self.value] == None:
                    self.value = (self.value + y_axis) % 8
                
            if self.selected:
                self.sel_value = (self.sel_value + y_axis) % 8
        
        if a_button == 1:
            if self.is_empty():
                self.stop()
                return
                
            if self.selected:
                if self.value == self.sel_value:
                    #print("Item is doing a thing")
                    inv = self.game.player.inventory
                    item, quantity = inv[self.value]
                    item.effect()
                    if item.consumable: inv[self.value][1] -= 1
                    if item.consumable and inv[self.value][1] == 0:
                        inv[self.value] = None
                        self.normalize_cursor()
                    self.selected = False
                    return
                elif self.value != self.sel_value:
                    inv = self.game.player.inventory
                    a = {}
                    a[self.sel_value] = inv[self.value]
                    a[self.value] = inv[self.sel_value]
                    for i in a.keys():
                        inv[i] = a[i]
                    self.value = self.sel_value
                    self.selected = False
                    return
                    
            if not self.selected:
                self.selected = True
                self.sel_value = self.value
            
        elif b_button == 1:
            if not self.selected:
                self.stop()
                return
            if self.selected:
                self.selected = False
            
    def render(self):
    
        #self.game.canvas.blit(self.back, (self.x, self.y))
    
        inv = self.game.player.inventory
        for i in range(8): # TODO this is hard coded
            label = ""
            if inv[i] != None:
                if i == self.value:	label += ">      "
                label += inv[i][0]["name"]
            if self.selected and i == self.sel_value:
                label = label + "<"
            if label != "":
                x = self.childpane.x + 25 # padding
                y = self.childpane.y + 10 * (i+1) + i * self.game.ui_font.get_height() # 0:15; 1:40; 2:65
                icon = self.game.icon_db[inv[i][0]["icon"]]
                txt_img = self.game.ui_font.render(label, 0, (0xff,0xff,0xff))
                qty = self.game.ui_font.render(str(inv[i][1]), 0, (0,0xff,0xff))
                # add the other bits like the icon and quantity
                self.game.display.blit(icon, (x, y))
                self.game.display.blit(txt_img, (x-12,y))
                self.game.display.blit(qty, (x+200,y))
