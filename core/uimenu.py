import pygame



# not using a dict because this way preserves order
# apparently dicts now preserve orders. TIL...

# bindings to consolidate and replace func_dict and labels

# declare a UI_PlayerMenu before declaring UI_SubMenuPane
class UI_PlayerMenu:

	def __init__(self, uid, game_obj, rect, bindings, b_func):
	
		self.uid = uid
		self.game = game_obj
		self.x, self.y = rect[:2]
		self.bindings = bindings # []
		self.b_func = b_func # called when the B button is pressed
		
		self.value = 0
		self.v_string = self.bindings.values()[self.value]
		self.visible = True
		self._returned = 0

		self.back = pygame.Surface(rect[2:]).convert_alpha()
		self.back.fill((0,0,0,127))
		
		self.font = pygame.font.Font(None, 24)
		
		self.child = None
		#self.child.value = self.labels[self.value].lower()
				
	def start(self):
	
		self.visible = True
		self.child.value = self.value = 0
		self._returned = 0
		#self.game.controller.flush()
	
	def stop(self):
	
		self.visible = False
		self._returned = 1
		#self.game.controller.flush()
	
	def update(self):
	
		self._returned = 0

		if self.visible: # and not self.game.fader.fading:
			if self.game.controller.y_axis_sr != 0:			
				self.value = (self.value + self.game.controller.y_axis_sr * self.game.controller.y_axis) % len(self.bindings)
				self.v_string = self.bindings.values()[self.value]
				self.child.value = self.value
			if self.game.controller.pressed_a:
				print(self.child.v_string)
				self.bindings[self.v_string](self.game)
			if self.game.controller.pressed_b:
				self.b_func(self.game)
		
		#self.child.update()		
			#if self.game.controller.pressed_a == 1:
			#	self.stop()
				#list(self.tDict.values())[self.value]()
				
	def render(self):
	
		if self.visible:
			self.game.display.blit(self.back, (self.x, self.y))
			
			for b in range(len(self.bindings)):	
			#for l, text in enumerate(self.bindings): # self.tDict.keys()
				text = list(self.bindings.keys())[b] + (" <" * b == self.value)
				#if b == self.value: text += " <"
				x = self.x + 5 # padding
				y = self.y + 7 * (b+1) + b * self.font.get_height() # 0:15; 1:40; 2:65
				#label_image = self.game.ui_font.render(label, 0, (0xff,0xff,0xff))
				label_image = self.font.render(text, 0, (0xff,0xff,0xff))
				#self.game.display.blit(label_image, (x,y))
				self.game.display.blit(label_image, (x,y))
				
			self.child.render()

# needs a parent (UI_PlayerMenu) to work
class UI_SubMenuPane: # why does this need bindings? why doesn't it just run off of parent?

	def __init__(self, uid, parent, size):
	
		self.uid = uid
		self.parent = parent
		self.game = parent.game
		self.x = self.y = 0
		self.w, self.h = size
		self.bindings = self.parent.bindings # binds a function to a label
		self.value = 0

		self.parent.child = self
		self.x = self.parent.x + self.parent.back.get_width() + 10
		self.y = self.parent.y
		
		self.back = pygame.Surface(size).convert_alpha()
		self.back.fill((0,0,0,127))
		
		self.visible = True
		
	def render(self):
	
		if self.visible:
			self.game.display.blit(self.back, (self.x,self.y))
			
			# passing self to get the x and y values of self
			# self.bindings[self.value]((self.x,self.y), self.game.display)
			#  ^ theoretically you could do this
			#self.bindings[self.value](self, self.game.display)
			self.parent.bindings.[self.parent.v_string](self, self.game.display)

if __name__ == "__main__":

	pygame.init()
	
	display = pygame.display.set_mode((640,480))
	display.fill((0,0,0xff))
		
	func_dict = { "status": draw_status, "inventory": draw_inventory, "gear": draw_gear, "save": draw_save }
	submenu = UI_SubmenuPane("submenu_pane", (300,300), func_dict)
	
	labels = [ "Inventory", "Status", "Gear", "Save" ]
	livemenu = UI_LiveMenu("livemenu", (105,90), (120,100), submenu, labels)
	
	while 1:
	
		livemenu.update()
		livemenu.render(display)
		
		pygame.display.flip()
		display.fill((0,0,0xff))
