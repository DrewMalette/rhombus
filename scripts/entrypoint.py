# entrypoint.py; rename to main.py

import os

import pygame
import core
from core import filepaths

def test_tmx_init(game_obj, filename):

	# eventually I want to replace this with a generic onion sprite
	pygame.display.set_caption(filename)
	game_obj.player = core.Player("Ark", game_obj, os.path.join(filepaths.image_path, "spr_ark2.png"))
	game_obj.load_scene(filename, os.path.join(filepaths.scene_path, filename))
	game_obj.renderer.following = game_obj.player
	game_obj.debugging = 1
	
	game_obj.set_stack(game_obj.scene_obj)
	game_obj.scene_obj.paused = False
	game_obj.next_script = test_tmx_loop
	game_obj.fader.fade_in()
	
def test_tmx_loop(game_obj):

	if game_obj.controller.exit:
		game_obj.next_script = game_obj.exit
		game_obj.fader.fade_out()
	
def newgame_init(game_obj):

	game_obj.player = core.Player("Ark", game_obj, os.path.join(filepaths.image_path, "spr_ark2.png"))
	game_obj.load_scene("scene1", os.path.join(filepaths.scene_path, "scene_cottage.tmx"))
	game_obj.renderer.following = game_obj.player
		
	game_obj.set_stack(game_obj.scene_obj)
	
	game_obj.next_script = gameplay_loop
	game_obj.fader.fade_in()

def playermenu_init(game_obj):

	game_obj.scene_obj.paused = True
	game_obj.set_stack(game_obj.scene_obj, game_obj.ui["playermenu"])
	game_obj.ui["playermenu"].start()
	game_obj.script = playermenu_loop

def playermenu_loop(game_obj):

	if game_obj.controller.pressed_a:
		if game_obj.ui["playermenu"].value == 4:
			quit_init(game_obj)

	if game_obj.controller.pressed_b:
		gameplay_init(game_obj)

def gameplay_init(game_obj): # returning to gameplay

	game_obj.set_stack(game_obj.scene_obj)
	game_obj.script = gameplay_loop
	game_obj.scene_obj.paused = False
	
def gameplay_loop(game_obj):

	#if game_obj.controller.exit:
	#	game_obj.next_script = title_init
	#	game_obj.music_tracks["titletrack"].fadeout(1000)
	#	game_obj.fader.fade_out()
		
	if game_obj.controller.pressed_a and not game_obj.player.in_dialogue:
		dialogue = ["Greetings and welcome", "to a sample scene", "for the rhombus", "framework", " ", " "]
		dialogue_init(game_obj, dialogue)
	elif game_obj.controller.pressed_x:
		playermenu_init(game_obj)
		
def dialogue_init(game_obj, dialogue):

	game_obj.set_stack(game_obj.scene_obj, game_obj.ui["dialoguebox"])
	game_obj.ui["dialoguebox"].text_list = dialogue
	game_obj.ui["dialoguebox"].start()
	game_obj.script = dialogue_loop
	
def dialogue_loop(game_obj):

	if game_obj.ui["dialoguebox"]._returned: gameplay_init(game_obj)

def title_init(game_obj):

	game_obj.set_stack(game_obj.title_card, game_obj.ui["titleselect"])
	
	game_obj.ui["titleselect"].start()
	
	game_obj.music_tracks["titletrack"].play(-1)
	game_obj.next_script = title_loop
	game_obj.fader.fade_in()
	
def title_loop(game_obj):

	if game_obj.ui["titleselect"]._returned:
		if game_obj.ui["titleselect"].value == 0: # New Game
			game_obj.next_script = newgame_init
			game_obj.fader.fade_out()			
		elif game_obj.ui["titleselect"].value == 1: # Quit to Desktop
			game_obj.music_tracks["titletrack"].fadeout(1000)
			game_obj.next_script = game_obj.exit
			game_obj.fader.fade_out()
		game_obj.ui["titleselect"].visible = False

def quit_init(game_obj):

	game_obj.set_stack(game_obj.scene_obj, game_obj.ui["dialoguebox"], game_obj.ui["yesnobox"])
	game_obj.scene_obj.paused = True
	
	game_obj.ui["dialoguebox"].text_list = ["Quit to menu?", " ", " "]
	game_obj.ui["dialoguebox"].start(wait_for=game_obj.ui["yesnobox"])
	
	game_obj.script = quit_loop
	
def quit_loop(game_obj):

	if game_obj.ui["yesnobox"]._returned:
		if game_obj.ui["yesnobox"].value == 0:
			game_obj.next_script = title_init
			game_obj.music_tracks["titletrack"].fadeout(1000)
			game_obj.fader.fade_out()	
		elif game_obj.ui["yesnobox"].value == 1: #if game_obj.controller.exit:
			gameplay_init(game_obj)
		game_obj.ui["dialoguebox"].stop()
			
def init(filename=None):

	print("rhombus framework - June 2020")

	pygame.init()
	game_obj = core.Game()
	
	if filename == None:
		game_obj.title_card = pygame.image.load(os.path.join(filepaths.image_path, "titlecard.png"))
		game_obj.music_tracks["titletrack"] = pygame.mixer.Sound(os.path.join(filepaths.sound_path, "titlemusic.ogg"))
	
		game_obj.ui["dialoguebox"] = core.UI_Dialogue("dialoguebox", game_obj, (170,360), (300,100))
		game_obj.ui["titleselect"] = core.UI_Select("titleselect", game_obj, (245,300), (150,54), ["New Game", "Quit to Desktop"])
		game_obj.ui["yesnobox"] = core.UI_Select("yesnobox", game_obj, (170,296), (54,54), ["Yes","No"])
		game_obj.ui["playermenu"] = core.UI_LiveMenu("playermenu", game_obj, (105,90), (120,120), 
													 core.UI_SubmenuPane("submenupane", game_obj, (300,300), core.func_dict), core.labels)
		title_init(game_obj)
	else:
		test_tmx_init(game_obj, filename)

	game_obj.main()

