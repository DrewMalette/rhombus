import pygame

class UI_Select(object):

	def __init__(self, uid, game_obj, loc, size, labels):
	
		self.uid = uid
		self.game_obj = game_obj
		
		self.value = 0
		self.visible = False
		self._returned = 0

		self.x, self.y = loc
		self.labels = labels
		self.back = pygame.Surface(size).convert_alpha()
		self.back.fill((0,0,0,127))
		
	def start(self):
	
		self.visible = True
		self.value = 0
		self._returned = 0
		self.game_obj.controller.flush()
	
	def stop(self):
	
		self.visible = False
		self._returned = 1
		self.game_obj.controller.flush()
	
	# each update needs to read the keystate of Engine
	def update(self):
	
		self._returned = 0
	
		if self.visible and not self.game_obj.fader.fading:
			if self.game_obj.controller.y_axis_sr != 0:			
				self.value = (self.value + self.game_obj.controller.y_axis_sr) % len(self.labels)
				
			if self.game_obj.controller.pressed_a == 1:
				self.stop()
				#list(self.tDict.values())[self.value]()
				
	def render(self):
	
		if self.visible:
			self.game_obj.display.blit(self.back, (self.x, self.y))
				
			for l, text in enumerate(self.labels): # self.tDict.keys()
				if l == self.value:
					label = text + " <"
				else:
					label = text
				x = self.x + 5 # padding
				y = self.y + 7 * (l+1) + l * self.game_obj.ui_font.get_height() # 0:15; 1:40; 2:65
				label_image = self.game_obj.ui_font.render(label, 0, (0xff,0xff,0xff))
				self.game_obj.display.blit(label_image, (x,y))
