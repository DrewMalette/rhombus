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
        self.display = pygame.display.set_mode(self.display_size)
        self.fader = game_fader.Fader(self, self.display.get_size())
        self.camera = game_camera.Camera("camera", self)
        
        self.controller = game_keyboard.Keyboard(self)
                
        self.clock = pygame.time.Clock()
        self.tick = 0
        
        self.obj_stack = [] # active objects; updated and rendered in order of iteration
        
        self.last_script = None # unimplemented
        self.script = None
        self.next_script = None
        self.player = None
        
        self.scene_db = {}
        self.mob_db = {}
        self.sprite_db = {}
        self.icon_db = {}
        
        self.ui = {}
        self.ui_font = pygame.font.Font(None, 24)
        self.title_card = None
        self.music_tracks = {}
        
        self.debug_info_on = -1
        self.debug_font = pygame.font.Font(None, 20)
        
        self.next_scene = None
        self.mob_talk = None

    def load_scene(self, filename):        
        if filename not in self.scene_db:
            self.scene_db[filename] = scene.Scene(filename, self)
            print("loading '{}'".format(filename))
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

    def draw_debug_info(self):    
        labels = []
        c = r = 0
        
        if self.camera.scene:
            labels.append(self.debug_font.render("Scene: "+self.camera.scene.uid, 0, (0xff,0xff,0xff)))
            c = int(self.player.x / self.camera.scene.tilesize)
            r = int(self.player.y / self.camera.scene.tilesize)
        else:
            labels.append(self.debug_font.render("no scene is loaded", 0, (0xff,0xff,0xff)))
            
        if self.script: labels.append(self.debug_font.render("Script: "+self.script.__name__, 0, (0xff,0xff,0xff)))
        
        if self.player:
            labels.append(self.debug_font.render("player.in_dialogue: "+str(self.player.in_dialogue), 0, (0xff,0xff,0xff)))
            labels.append(self.debug_font.render("player.x (pixel): "+str(self.player.x), 0, (0xff,0xff,0xff)))
            labels.append(self.debug_font.render("player.y (pixel): "+str(self.player.y), 0, (0xff,0xff,0xff)))
            labels.append(self.debug_font.render("player.c (tile): "+str(c), 0, (0xff,0xff,0xff)))
            labels.append(self.debug_font.render("player.r (tile): "+str(r), 0, (0xff,0xff,0xff)))
            labels.append(self.debug_font.render("action.x: "+str(self.player.action.x), 0, (0xff,0xff,0xff)))
            labels.append(self.debug_font.render("action.y: "+str(self.player.action.y), 0, (0xff,0xff,0xff)))
            labels.append(self.debug_font.render("facing: "+self.player.facing, 0, (0xff,0xff,0xff)))
        
        if self.camera.scene: labels.append(self.debug_font.render("paused: "+str(self.camera.scene.paused), 0, (0xff,0xff,0xff)))
        labels.append(self.debug_font.render("obj_stack: "+str(self.obj_stack), 0, (0xff,0xff,0xff)))
        labels.append(self.debug_font.render("fading: "+str(self.fader.fading), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("player: "+str(self.player), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("scene: "+str(self.camera.scene), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("camera.following: "+str(self.camera.following), 0, (0xff,0xff,0xff)))    
        #labels.append(self.debug_font.render("pressed_a: "+str(self.controller.pressed_a), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("held_a: "+str(self.controller.held_a), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("pressed_b: "+str(self.controller.pressed_b), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("held_b: "+str(self.controller.held_b), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("pressed_x: "+str(self.controller.pressed_x), 0, (0xff,0xff,0xff)))
        #labels.append(self.debug_font.render("held_x: "+str(self.controller.held_x), 0, (0xff,0xff,0xff)))
        
        for i, label in enumerate(labels):
            label.set_alpha(160)
            self.display.blit(label, (10, 10 + (i * self.debug_font.get_height()))) 

    def update(self):    
        self.clock.tick(self.fps)
        self.tick = (self.tick + 1) % 4294967296
        
        pygame.event.pump()
        self.controller.update()
        
        for obj in self.obj_stack:
            if getattr(obj, "update", None): obj.update()
        
        if self.script:
            self.script(self)
        
        self.fader.update()
        
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
        
        if self.debug_info_on == 1: self.draw_debug_info()
        
        pygame.display.flip()

