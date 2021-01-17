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
        
        for i, label in enumerate(self.game.player.statblock.stats):
            stat_label = self.game.ui_font.render("{}:".format(label.upper()), 0, (0,0xff,0xff))
            value = str(self.game.player.statblock.stats[label])
            if label in ("str","vit","agi","mnd"):
                value += " ("
                value += str(int((self.game.player.statblock.stats[label] - 10)/2))+")"
            val_label = self.game.ui_font.render(value, 0, (0xff,0xff,0xff))
            self.display.blit(stat_label, (x+40,y+self.game.ui_font.get_height()*(i+1)))
            self.display.blit(val_label, (x+40+stat_label.get_width(),y+self.game.ui_font.get_height()*(i+1)))
