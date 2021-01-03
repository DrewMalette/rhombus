# states.py:

import os
import pygame
import core
from core import filepaths

###
def test_tmx_init(game, filename):
    # eventually I want to replace this with a generic onion sprite
    pygame.display.set_caption(filename)
    game.player = core.Player(game, "hero_sprite.png")
    game.load_scene(filename)
    game.camera.following = game.player
    game.debug_info_on = 1
    
    game.obj_stack = [ game.camera.scene ]
    game.camera.scene.paused = False
    game.next_script = test_tmx_loop
    game.fader.fade_in()
    
def test_tmx_loop(game):
    if game.controller.exit:
        game.next_script = game.exit
        game.fader.fade_out()
###

###
def draw_wrapper(pane, surface):
    label = pane.parent.font.render(pane.parent.v_string, 0, (0xff,0xff,0xff))
    
    x = pane.x + ((pane.w - label.get_width()) / 2)
    y = pane.y + ((pane.h - label.get_height()) / 2)
    
    surface.blit(label, (x,y))
    
def draw_inventory(pane, surface): draw_wrapper(pane, surface)
def draw_status(pane, surface): draw_wrapper(pane, surface)
def draw_gear(pane, surface): draw_wrapper(pane, surface)
def draw_save(pane, surface): draw_wrapper(pane, surface)
def draw_quit(pane, surface): draw_wrapper(pane, surface)
###

def newgame_init(game):
    game.camera.following = game.player # will this eventually move?
    game.load_scene("outpost_oak.tmx")
    game.obj_stack = [ game.camera.scene ]
    game.next_script = gameplay_loop
    game.fader.fade_in()
    
def switchscene_init(game):
    game.load_scene(game.next_scene[0])
    c,r = game.next_scene[1]
    game.player.place(c,r)
    game.player.facing = game.next_scene[2]
    game.next_script = gameplay_loop
    game.fader.fade_in()

def playermenu_init(game, value=0):
    game.camera.scene.paused = True
    game.obj_stack = [ game.camera.scene, game.ui["playermenu"] ]
    game.ui["playermenu"].start(value)
    #game.script = playermenu_loop
    game.script = None # the player menu doesn't need a script; everything is handled internally

###
def gameplay_init(game): # returning to gameplay
    game.obj_stack = [ game.camera.scene ]
    game.script = gameplay_loop
    game.camera.scene.paused = False
    
def gameplay_loop(game): # game.script will still exist but only in a minor way
    if game.controller.pressed_x:
        playermenu_init(game)
    
    for switch in game.camera.scene.switches.values():
        if game.player.colliderect(switch[0]):
            # 0: rect; 1: filename; 2: (col, row); 3: facing
            game.next_scene = [switch[1], switch[2], switch[3]]
            game.next_script = switchscene_init
            game.fader.fade_out()
    
    if game.controller.pressed_a:
        game.player.action.interact()
        if game.mob_talk != None:
            dialogue_init(game, [game.mob_db[game.mob_talk].dialogue])
            game.mob_talk = None
###

###         
def dialogue_init(game, dialogue):
    game.obj_stack = [ game.camera.scene, game.ui["dialoguebox"] ]
    game.ui["dialoguebox"].text_list = dialogue
    game.ui["dialoguebox"].start()
    game.script = dialogue_loop
    
def dialogue_loop(game): # I'll have to bind functions to dialogueboxes too

    if game.ui["dialoguebox"].returned:
        gameplay_init(game)
###

def title_init(game):

    game.obj_stack = [ game.title_card, game.ui["titleselect"] ]
    
    game.ui["titleselect"].start()
    
    game.music_tracks["titletrack"].play(-1)
    game.next_script = None
    game.fader.fade_in()

def title_newgame(game):

    game.next_script = newgame_init
    game.fader.fade_out()
    
def title_quit(game):

    game.music_tracks["titletrack"].fadeout(1000)
    game.next_script = game.exit
    game.fader.fade_out()

def quit_init(game):

    game.obj_stack = [ game.camera.scene, game.ui["dialoguebox"], game.ui["yesnobox"] ]
    game.camera.scene.paused = True
    
    game.ui["dialoguebox"].text_list = ["Quit to menu?", " ", " "]
    game.ui["dialoguebox"].start(wait_for=game.ui["yesnobox"])
    
    game.script = None

def quit_no(game):

    playermenu_init(game)
    game.ui["dialoguebox"].stop()
    
def quit_yes(game):

    game.next_script = title_init
    game.music_tracks["titletrack"].fadeout(1000)
    game.fader.fade_out()
    game.ui["dialoguebox"].stop()
            

