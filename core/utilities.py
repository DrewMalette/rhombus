#

import os, math
import xml.etree.ElementTree as ET

import pygame

from . import filepaths
from . import mob
from . import scene_tileset

def distance(r1, r2):
    a = abs(r1.x - r2.x)
    b = abs(r1.y - r2.y)
    return int(math.sqrt(a**2 + b**2))

def load_image(filename, colourkey=None):
    try:
        image = pygame.image.load(filename)
    except:
        print("failed to load image '{}' ".format(filename))
        return

    image = image.convert()
    if colourkey != None:
        if colourkey == -1:
            colourkey = image.get_at((0,0))
        image.set_colorkey(colourkey, pygame.RLEACCEL)

    return image

def load_sprite(filename): # load sprite, Dec '20
    image = pygame.image.load(filename)
    image.convert()
    image.set_colorkey(image.get_at((0,0)), pygame.RLEACCEL)
    cell_w, cell_h = image.get_at((0, image.get_height()-1))[:2]
    rect = pygame.Rect((0,0)+image.get_at((1, image.get_height()-1))[:2])
    offsets = image.get_at((2, image.get_height()-1))[:2]
    cols = int(image.get_width() / cell_w)
    rows = int(image.get_height() / cell_h)

    cells = {}
    for row in range(rows):
        for col in range(cols):
            cells[row*cols+col] = image.subsurface((col*cell_w, row*cell_h, cell_w, cell_h))

    return { "cols": cols, "rows": rows, "cells": cells, "rect": rect, "offsets": offsets }

def load_tileset(filename, width, height, firstgid=1):
    image = load_image(filename)
    image.set_colorkey((255,0,255), pygame.RLEACCEL)
    
    gid = int(firstgid)
    textures = {}
    cols = int(image.get_width() / width)
    rows = int(image.get_height() / height)
    for row in range(rows):
        for col in range(cols):
            x = col * width
            y = row * height
            textures[str(gid)] = image.subsurface((x, y, width, height))
            gid += 1
    
    return textures

def get_tileset(root, scene):
    for tilesettag in root.iter("tileset"):
        filename = tilesettag.attrib["source"]
        tsxtree = ET.parse(os.path.join(filepaths.scene_path, filename))
        tsxroot = tsxtree.getroot()
        for tsx in tsxroot.iter("tileset"):
            for i in tsx.iter("image"):
                filename = i.attrib["source"]
                firstgid = tilesettag.attrib["firstgid"]
                scene.tileset.update(filename, firstgid)

def get_layers(root, scene):
    for layer in root.iter("layer"):
        for data in layer.iter("data"):
            name = layer.attrib['name']
            rawdata = data.text.split(",")
            cleandata = []
            for tile in rawdata:
                cleandata.append(tile.strip())
            scene.layerdata[name] = cleandata

def get_objects(root, scene):            
    for layer in root.iter("objectgroup"):
        for rect in layer.iter("object"):
            rectattribs = {}
            for v in rect.attrib.keys():
                rectattribs[v] = rect.attrib[v]
            for proptag in rect.iter("properties"):
                for propchild in proptag.iter("property"):
                    index = propchild.attrib["name"]
                    value = propchild.attrib["value"]
                    rectattribs[index] = value
            
            col = int(float(rectattribs["x"]) / scene.tile_w)
            row = int(float(rectattribs["y"]) / scene.tile_h)
            if rectattribs["type"] == "player":
                if scene.game.player is None:
                    print("player object is not defined")
                    print("exiting")
                    pygame.quit()
                    exit()
                scene.mobs.append("player")
                scene.defaults["player"] = (col,row)
            elif rectattribs["type"] == "mob":
                m = mob.Mob(scene.game, rectattribs["Filename"], rectattribs["id"])
                m.dialogue = rectattribs["dialogue"]
                scene.mobs.append(m.uid)
                scene.defaults[m.uid] = (col,row)
                
            elif rectattribs["type"] == "switch":
                uid = rectattribs["id"]
                scenefile = rectattribs["Filename"]
                x = int(float(rectattribs["x"]) / scene.tile_w) * scene.tile_w
                y = int(float(rectattribs["y"]) / scene.tile_h) * scene.tile_h
                facing = rectattribs["facing"] # TODO
 #               try:
                c = int(rectattribs["col"])
                r = int(rectattribs["row"])
                scene.switches[uid] = [pygame.Rect((x,y,scene.tile_w,scene.tile_h)), scenefile, (c,r), facing]
#                except:
                    #print("defaulting to map defined placement position")
#                    scene.switches[uid] = [pygame.Rect((x,y,scene.tile_w,scene.tile_h)), uid, None, facing]
            #elif rectattribs["type"] == "static":
            #	filepath = "content/image/" + rectattribs["Filename"]
            #	name = rectattribs["name"]
            #	scene.sprites[uid] = sprite.Static(filepath, name)
            #	scene.sprites[uid].scene = scene
            #	scene.sprites[uid].place(col,row)

def load_tmx(filename, scene):
    tree = ET.parse(os.path.join(filepaths.scene_path, filename))
    root = tree.getroot()
    scene.cols = int(root.attrib["width"])
    scene.rows = int(root.attrib["height"])
    scene.tile_w = int(root.attrib["tilewidth"])
    scene.tile_h = int(root.attrib["tileheight"])
    scene.tilesize = scene.tile_w # assumes a square tile
    scene.tileset = scene_tileset.Tileset(scene.tile_w, scene.tile_h)
    get_tileset(root, scene)
    get_layers(root, scene)
    get_objects(root, scene)

