# main.py:

import os

import pygame
import core
from core import filepaths

from . import states

def start(filename=None):

    pygame.init()
    pygame.display.set_caption("rhombus 1.1.0 (Dec 19 2020, 22:05:11)")
    game = core.Game()
    
    if filename == None:
        # setup the title menu
        game.title_card = pygame.image.load(os.path.join(filepaths.image_path, "titlecard.png"))
        game.music_tracks["titletrack"] = pygame.mixer.Sound(os.path.join(filepaths.sound_path, "rstheme.ogg"))
        
        # setup the interface objects
        game.ui["dialoguebox"] = core.UI_Dialogue("dialoguebox", game, (170,360,300,100))
        
        title_bindings = { "New Game": states.title_newgame,
                           "Quit to Desktop": states.title_quit }
        game.ui["titleselect"] = core.UI_Select("titleselect", game, (245,300,150,54), title_bindings)
        
        quit_bindings = { "No": states.quit_no,
                          "Yes": states.quit_yes }
        game.ui["yesnobox"] = core.UI_Select("yesnobox", game, (170,296,54,54), quit_bindings)
        
        menu_bindings = { "Inventory": states.draw_inventory,
                          "Status": states.draw_status,
                          "Gear": states.draw_gear,
                          "Save": states.draw_save,
                          "Quit": states.quit_init }
        game.ui["playermenu"] = core.UI_PlayerMenu("playermenu", game, (105,90,120,124),
                                                   menu_bindings, states.gameplay_init)
        game.ui["childpane"] = core.UI_SubMenuPane("childpane", game, game.ui["playermenu"], (300,300))
        game.ui["inventory"] = core.UI_Inventory(game, "Inventory", game.ui["childpane"])
        game.ui["status"] = core.UI_Status("Status", game, game.ui["childpane"])
        
        # load item icons
        game.load_icon("potion_ico.png")
        
        # setup the player mob
        game.player = core.Player(game, "hero_sprite.png")
        
        # initialize to title screen and start game program
        states.title_init(game)
    else:
        states.test_tmx_init(game, filename)
        
    game.main()

