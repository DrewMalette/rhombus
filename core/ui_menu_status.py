# uistatus.py:

class UI_Status:
    def __init__(self, uid, game, childpane):
        self.uid = uid
        self.game = game
        self.display = self.game.display
        self.childpane = childpane # childpane.parent is UI_PlayerMenu
        self.childpane.bindings[uid] = self
        
    def render(self):
        spr_name = self.game.player.sprite
        avatar = self.game.sprite_db[spr_name].cells[0]
        x = self.childpane.x + 10
        y = self.childpane.y + 10
        self.display.blit(avatar, (x,y))
        
        name_label = self.game.ui_font.render(self.game.player.name, 0, (0xff,0xff,0xff))
        self.display.blit(name_label, (x+40,y))
        
        level_label = self.game.ui_font.render("Level:", 0, (0xff,0xff,0xff))
        level_num = self.game.ui_font.render(str(self.game.player.statblock.level), 0, (0,0xff,0xff))
        self.display.blit(level_label, (x+200,y))
        self.display.blit(level_num, (x+200+level_label.get_width(),y))
