#

import os

import pygame

from . import filepaths
from . import utilities

class Tileset:

	def __init__(self, width, height):
	
		self.width = height
		self.height = height
					
		self.textures = {}
		
	def update(self, filename, colourkey, firstgid=1):
		
		textures = utilities.load_tileset(os.path.join(filepaths.scene_path, filename), self.width, self.height, colourkey, firstgid)
		self.textures.update(textures)
				
	def __getitem__(self, key=-1):
	
		if key == -1:
			return self.textures
		if key != -1:
			return self.textures[key]

