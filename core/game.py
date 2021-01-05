#

import os

import pygame

from . import filepaths
from . import utilities
from . import game_camera
from . import game_fader
from . import game_keyboard
from . import mob
from . import scene

class Game:
    fps = 60
    display_size = (640,480)

    def __init__(self):
        # this is going to be replaced/modified
        self.obj_stack = [] # active objects; updated and rendered in order of iteration
        
        self.scene_db = {}
        self.mob_db = {}
        self.sprite_db = {}
        self.icon_db = {}
        self.music_tracks = {} # sound_db
                
        self.last_script = None # unimplemented
        self.script = None
        self.next_script = None
        self.player = None
        self.next_scene = None
        self.mob_talk = None
        self.next_mode = None
        
        self.title_card = None
        
        self.display = pygame.display.set_mode(self.display_size)
        self.fader = game_fader.Fader(self, self.display.get_size())
        self.camera = game_camera.Camera(self)
        
        # incoming ui subsystem (Jan 3, 2021)
        self.ui = {}
        self.ui_font = pygame.font.Font(None, 24)
        self.debug_font = pygame.font.Font(None, 20)
        
        self.controller = game_keyboard.Keyboard(self)
                
        self.clock = pygame.time.Clock()
        self.tick = 0
        
        self.debug_info_on = -1
        
    def load_scene(self, filename): # setup_scene
        if filename not in self.scene_db:
            self.scene_db[filename] = scene.Scene(filename, self)
            print("loading '{}'".format(filename))
    
    def setup_scene(self, filename):
        if filename not in self.scene_db: self.load_scene(filename)
        self.camera.scene = self.scene_db[filename]
        self.camera.following = self.player
        # assumes tile is square
        self.camera.tilesize = self.camera.scene.tile_w
        self.camera.cols = int(self.camera.w / self.camera.scene.tilesize + 2)
        self.camera.rows = int(self.camera.h / self.camera.scene.tilesize + 2)
        self.camera.blank = pygame.Surface((self.camera.scene.tilesize,self.camera.scene.tilesize)).convert()
        self.camera.blank.fill((0,0,0))
                
        # reset mobs in scene to default positions and facings
        for mob_fn in self.camera.scene.mobs:
            self.mob_db[mob_fn].spawn(filename)
        
        self.player.moving = False
        self.camera.update() # centre camera on camera.following before fade_in begins
        
    def load_icon(self, filename):
        if not filename in self.icon_db:
            image = pygame.image.load(os.path.join(filepaths.icon_path, filename))
            image.set_colorkey(image.get_at((0,0)), pygame.RLEACCEL)
            self.icon_db[filename] = image
            print("icon '{}' not found; loading".format(filename))
        else:
            print("'{}' is already in icon database".format(filename))
    
    def add_mode(self, id_str, obj_list, script):
        self.modes[id_str] = obj_list
        self.scripts[id_str] = script
    
    def main(self):
        self.running = True
        
        while self.running:
            self.update()
            self.render()

    def exit(self, _): # "_" because an argument is required
        pygame.quit()
        exit()

    def fade_loop(self, _):    
        if self.fader.faded_out or self.fader.faded_in:
            self.script = self.next_script

    def update(self):    
        self.clock.tick(self.fps)
        self.tick = (self.tick + 1) % 4294967296
        
        pygame.event.pump()
        self.controller.update()
        
        for obj in self.obj_stack:
            if getattr(obj, "update", None): obj.update()
        
        if self.script:
            self.script(self)
        
        self.fader.update() # this will be removed
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1: self.debug_info_on = -self.debug_info_on

    def render(self):
        for obj in self.obj_stack:
            if getattr(obj, "render", None):
                obj.render()
            else:
                self.display.blit(obj, (0,0))
                
        self.fader.render()
        
        if self.debug_info_on == 1: utilities.draw_debug_info(self)
        
        pygame.display.flip()

