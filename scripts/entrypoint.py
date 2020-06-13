# entrypoint.py

import os

import pygame
import framework.core
from framework.core import filepaths
	
def newgame_init(game):

	game.load_scene("scene1", os.path.join(filepaths.scene_path, "scene_cottage.tmx"))
	
	game.obj_stack = []
	game.obj_stack.append(game.scene)
	game.obj_stack.append(game.fader)
	
	game.player.facing = "south"
	game.renderer.following = game.player
	
	game.next_script = newgame_loop # eventually newgame will not have a loop
	game.fader.fade_in()
	
def newgame_loop(game):

	if game.controller.exit:
		game.next_script = title_init
		game.music_tracks["titletrack"].fadeout(1000)
		game.fader.fade_out()

def title_init(game): # inits always clear game.obj_stack

	game.obj_stack = []
	game.obj_stack.append(game.title_card)
	game.obj_stack.append(game.ui["titleselect"])
	game.obj_stack.append(game.fader)
		
	game.ui["titleselect"].start()
	
	game.music_tracks["titletrack"].play(-1)
	game.next_script = title_loop
	game.fader.fade_in()
	
def title_loop(game):

	if game.ui["titleselect"]._returned:
		if game.ui["titleselect"].value == 0: # New Game
			game.next_script = newgame_init
			game.fader.fade_out()			
		elif game.ui["titleselect"].value == 1: # Quit to Desktop
			game.music_tracks["titletrack"].fadeout(1000)
			game.next_script = game.exit
			game.fader.fade_out()
		game.ui["titleselect"].visible = False

def init():

	pygame.init()
	game = framework.core.Game(os.path.join(filepaths.image_path, "titlecard.png"))
	game.ui["dialoguebox"] = framework.core.UI_Dialogue("dialoguebox", game, (170,360), (300,100))
	game.ui["titleselect"] = framework.core.UI_Select("titleselect", game, (245,300), (150,54), ["New Game", "Quit to Desktop"])
	game.player = framework.core.Player(game, os.path.join(filepaths.image_path, "spr_ark2.png"), "Ark")
	game.music_tracks["titletrack"] = pygame.mixer.Sound(os.path.join(filepaths.sound_path, "titlemusic.ogg"))
	
	title_init(game)
	game.main()

