# entrypoint.py; rename to main.py

import os

import pygame
import core
from core import filepaths

def test_tmx_init(game, filename):

	# eventually I want to replace this with a generic onion sprite
	pygame.display.set_caption(filename)
	game.player = core.Player("Ark", game, os.path.join(filepaths.image_path, "spr_ark2.png"))
	game.load_scene(filename, os.path.join(filepaths.scene_path, filename))
	game.camera.following = game.player
	game.debug_info_on = 1
	
	game.obj_stack = [ game.scene ]
	game.scene.paused = False
	game.next_script = test_tmx_loop
	game.fader.fade_in()
	
def test_tmx_loop(game):

	if game.controller.exit:
		game.next_script = game.exit
		game.fader.fade_out()

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

def newgame_init(game):

	game.player = core.Player("Ark", game, os.path.join(filepaths.image_path, "spr_ark2.png"))
	game.load_scene("scene_cottage.tmx")
	game.camera.following = game.player
		
	game.obj_stack = [ game.scene ]
	
	game.next_script = gameplay_loop
	game.fader.fade_in()

def playermenu_init(game):

	game.scene.paused = True
	game.obj_stack = [ game.scene, game.ui["playermenu"] ]
	game.ui["playermenu"].start()
	#game.script = playermenu_loop
	game.script = None

def gameplay_init(game): # returning to gameplay

	game.obj_stack = [ game.scene ]
	game.script = gameplay_loop
	game.scene.paused = False
	
def gameplay_loop(game): # game.script will still exist but only in a minor way
	
	if game.controller.pressed_a:# and not game.player.in_dialogue:
		dialogue = ["Greetings and welcome", "to a sample scene", "for the rhombus", "framework", " ", " "]
		dialogue_init(game, dialogue)
	elif game.controller.pressed_x:
		playermenu_init(game)
		
def dialogue_init(game, dialogue):

	game.obj_stack = [ game.scene, game.ui["dialoguebox"] ]
	game.ui["dialoguebox"].text_list = dialogue
	game.ui["dialoguebox"].start()
	game.script = dialogue_loop
	
def dialogue_loop(game): # I'll have to bind functions to dialogueboxes too

	if game.ui["dialoguebox"]._returned:
		gameplay_init(game)

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

	game.obj_stack = [ game.scene, game.ui["dialoguebox"], game.ui["yesnobox"] ]
	game.scene.paused = True
	
	game.ui["dialoguebox"].text_list = ["Quit to menu?", " ", " "]
	game.ui["dialoguebox"].start(wait_for=game.ui["yesnobox"])
	
	game.script = None

def quit_no(game):

	gameplay_init(game)
	game.ui["dialoguebox"].visible = False
	
def quit_yes(game):

	game.next_script = title_init
	game.music_tracks["titletrack"].fadeout(1000)
	game.fader.fade_out()
	game.ui["dialoguebox"].visible = False
			
def start(filename=None):

	pygame.init()
	pygame.display.set_caption("rhombus 1.0.2 (Jul 12 2020, 18:29:46)")
	game = core.Game()
	
	if filename == None:
		game.title_card = pygame.image.load(os.path.join(filepaths.image_path, "titlecard.png"))
		game.music_tracks["titletrack"] = pygame.mixer.Sound(os.path.join(filepaths.sound_path, "titlemusic.ogg"))
	
		game.ui["dialoguebox"] = core.UI_Dialogue("dialoguebox", game, (170,360,300,100))
		
		title_bindings = { "New Game": title_newgame, "Quit to Desktop": title_quit }
		game.ui["titleselect"] = core.UI_Select("titleselect", game, (245,300,150,54), title_bindings)
		
		quit_bindings = { "No": quit_no, "Yes": quit_yes }
		game.ui["yesnobox"] = core.UI_Select("yesnobox", game, (170,296,54,54), quit_bindings)
		
		menu_bindings = { "Inventory": draw_inventory, "Status": draw_status, "Gear": draw_gear, "Save": draw_save, "Quit": quit_init }
		game.ui["playermenu"] = core.UI_PlayerMenu("playermenu", game, (105,90,120,124), menu_bindings, gameplay_init)
		game.ui["childpane"] = core.UI_SubMenuPane("childpane", game.ui["playermenu"], (300,300))
		
		title_init(game)
	else:
		test_tmx_init(game, filename)

	game.main()

