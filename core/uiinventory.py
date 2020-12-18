#

import pygame

class UI_Inventory(object): # will bind to a SubMenuPane and draw's relative to the SubMenuPane's x/y coordinates

    def __init__(self, game, uid, childpane):    
        self.game = game
        self.uid = uid
        self.childpane = childpane # childpane.parent is UI_PlayerMenu
        self.childpane.bindings[uid] = self
        self.cursor = ">"
        self.value = 0
        self.sel_value = 0
        self.selected = False
        self.font_colour = (0xc0,0xc0,0xc0)
    
    def normalize_cursor(self):
        inv = self.game.player.inventory
        count = 0
        while inv[count] == None and count < 7:
            count += 1
        self.value = count
    
    def start(self):
        self.selected = False
        self.normalize_cursor()
        self.cursor = ">"
                
    def stop(self):
        self.childpane.parent.submenu = None
        self.cursor = ">"
        
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
                self.value = (self.value + y_axis * self.game.controller.y_axis) % 8
                while inv[self.value] == None:
                    self.value = (self.value + y_axis * self.game.controller.y_axis) % 8
                
            if self.selected:
                self.sel_value = (self.sel_value + y_axis * self.game.controller.y_axis) % 8
        
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
                    self.cursor = ">"
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
                    self.cursor = ">"
                    return
                    
            if not self.selected:
                self.selected = True
                self.sel_value = self.value
                self.cursor = "|"
            
        elif b_button == 1:
            if not self.selected:
                self.stop()
                return
            if self.selected:
                self.selected = False
                self.cursor = ">"
            
    def render(self):
        inv = self.game.player.inventory # <-- you realize this is being called every tick, right?
        for i in range(8): # TODO this is hard coded
            x = self.childpane.x + 25 # padding
            y = (self.childpane.y + 10 * (i+1) + i * self.game.ui_font.get_height()) + 25 # 0:15; 1:40; 2:65
            if inv[i] != None: # blit in order, from left to right
                colour = self.childpane.parent.white[int(self.childpane.parent.submenu!=None)]
                if i == self.value:
                    cursor = self.game.ui_font.render(self.cursor, 0, colour)
                    self.game.display.blit(cursor, (x+15,y))
                #
                icon = self.game.icon_db[inv[i][0]["icon"]]
                self.game.display.blit(icon, (x+30, y))
                #
                label = inv[i][0]["name"]
                txt_img = self.game.ui_font.render(label, 0, colour)
                self.game.display.blit(txt_img, (x+60,y))
                #
                colour = self.childpane.parent.cyan[int(self.childpane.parent.submenu!=None)]
                qty = self.game.ui_font.render(str(inv[i][1]), 0, colour)
                self.game.display.blit(qty, (x+230,y))
            if self.selected and i == self.sel_value:
                sel_cursor = self.game.ui_font.render(">", 0, self.childpane.parent.white[int(self.childpane.parent.submenu!=None)])
                self.game.display.blit(sel_cursor, (x,y))
                
