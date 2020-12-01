#

from . import filepaths
from . import utilities

class Scene:

    def __init__(self, filename, game_obj):

        self.uid = filename
        self.game = game_obj
        
        self.mob_filenames = []
        self.buildings = {}
        self.furniture = {}
        self.loot = {}
        self.loot_count = 0
        self.switches = {}
        self.layerdata = { "bottom": None, "middle": None, "top": None, "collide": None }
        self.tileset = None
        self.defaults = {}
        
        utilities.load_tmx(self.uid, self)
        
        self.paused = False		
        
    def add_loot(self, filename, x, y):
    
        uid = self.loot_count
        px = x
        py = y - 20
        self.loot[self.loot_count] = sprite.Loot(self, uid, filename, (px,py))
        self.loot_count = (self.loot_count + 1) % 256
        
    def add_mob(self, mob_obj):
    
        self.mobs[mob.name] = mob_obj
    
    def get_tile(self, layername, col, row):
    
        index = int((row % self.rows) * self.cols + (col % self.cols))
        return self.layerdata[layername][index]
        
    def get_mobs(self):
    
        l = []
        for mob_fn in self.mob_filenames:
            l.append(self.game.mob_db[mob_fn])
        return l
            
    def update(self):

        if not self.game.fader.fading and not self.paused:
            for filename in self.mob_filenames:
                self.game.mob_db[filename].update()
        self.game.camera.update() # this is reeeeeeetarded
        
    def render(self):


        self.game.camera.render()

