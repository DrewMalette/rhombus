#

import pygame

class UI_Select:

	def __init__(self, uid, game_obj, rect, bindings): # TODO bindings here
	
		self.uid = uid
		self.game = game_obj
		
		self.value = 0
		self.visible = False
		self._returned = 0

		self.x, self.y = rect[:2]
		self.bindings = bindings
		self.back = pygame.Surface(rect[2:]).convert_alpha()
		self.back.fill((0,0,0,127))
		
	def start(self):
	
		self.visible = True
		self.value = 0
		self._returned = 0
		self.game.controller.flush()
	
	def stop(self):
	
		self.visible = False
		self._returned = 1
		self.game.controller.flush()
		self.bindings[self.value][1](self.game)
	
	def update(self):

		self._returned = 0
	
		if self.visible and not self.game.fader.fading:
			self.value = (self.value + self.game.controller.y_ax_sr()) % len(self.bindings)
			
			if self.game.controller.pressed_a == 1:
				self.stop()
		
	def render(self):
	
		if self.visible:
			self.game.display.blit(self.back, (self.x, self.y))
				
			for l, text in enumerate(self.bindings):
				if l == self.value:
					label = text[0] + " <"
				else:
					label = text[0]
				x = self.x + 5 # padding
				y = self.y + 7 * (l+1) + l * self.game.ui_font.get_height() # 0:15; 1:40; 2:65
				label_image = self.game.ui_font.render(label, 0, (0xff,0xff,0xff))
				self.game.display.blit(label_image, (x,y))
