import pygame

# declare this before UI_LiveMenu
class UI_SubmenuPane(object):

	def __init__(self, uid, loc, size, func_dict): # func_dict keys coorespond to a list in UI_LiveMenu
	
		self.uid = uid
		#self.game = game
		self.x, self.y = loc
		self.w, self.h = size
		self.parent = None
		self.func_dict = func_dict
		self.value = ""
		
		self.back = pygame.Surface(size).convert_alpha()
		self.back.fill((0,0,0,127))
		
		self.visible = True
		
	def render(self, surface):
	
		if self.visible:
			surface.blit(self.back, (self.x,self.y))
			self.func_dict[self.value](self, surface)

# NEEDS a child in order to work properly
class UI_LiveMenu(object):

	def __init__(self, uid, loc, size, child, labels):
	
		self.uid = uid
		#self.game = game
		
		self.value = 0
		self.visible = True
		self._returned = 0

		self.x, self.y = loc
		self.labels = labels # []
		self.back = pygame.Surface(size).convert_alpha()
		self.back.fill((0,0,0,127))
		
		self.font = pygame.font.Font(None, 24)
		
		self.child = child
		self.child.value = self.labels[self.value].lower()
		self.child.parent = self
		
	def start(self):
	
		self.visible = True
		self.value = 0
		self._returned = 0
		#self.game.controller.flush()
	
	def stop(self):
	
		self.visible = False
		self._returned = 1
		#self.game.controller.flush()
	
	# each update needs to read the keystate of Engine
	def update(self):
	
		self._returned = 0
		
		y_axis = 0
		
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					y_axis = 1
				elif event.key == pygame.K_UP:
					y_axis = -1
					
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					exit()
	
		if self.visible: # and not self.game.fader.fading:
			#if self.game.controller.y_axis_sr != 0:			
			if y_axis != 0:			
				self.value = (self.value + y_axis) % len(self.labels)
				self.child.value = self.labels[self.value].lower()
				print(self.child.value)
		
		#self.child.update()		
			#if self.game.controller.pressed_a == 1:
			#	self.stop()
				#list(self.tDict.values())[self.value]()
				
	def render(self, surface):
	
		if self.visible:
			#self.game.display.blit(self.back, (self.x, self.y))
			display.blit(self.back, (self.x, self.y))
				
			for l, text in enumerate(self.labels): # self.tDict.keys()
				if l == self.value:
					label = text + " <"
				else:
					label = text
				x = self.x + 5 # padding
				y = self.y + 7 * (l+1) + l * self.font.get_height() # 0:15; 1:40; 2:65
				#label_image = self.game.ui_font.render(label, 0, (0xff,0xff,0xff))
				label_image = self.font.render(label, 0, (0xff,0xff,0xff))
				#self.game.display.blit(label_image, (x,y))
				surface.blit(label_image, (x,y))
				
			self.child.render(surface)

def draw_wrapper(pane, surface):

	label = pane.parent.font.render(pane.value.capitalize(), 0, (0xff,0xff,0xff))
	
	x = pane.x + ((pane.w - label.get_width()) / 2)
	y = pane.y + ((pane.h - label.get_height()) / 2)
	
	surface.blit(label, (x,y))
	
def draw_inventory(pane, surface): draw_wrapper(pane, surface)
def draw_status(pane, surface): draw_wrapper(pane, surface)
def draw_gear(pane, surface): draw_wrapper(pane, surface)
def draw_save(pane, surface): draw_wrapper(pane, surface)
			
if __name__ == "__main__":

	pygame.init()
	
	display = pygame.display.set_mode((640,480))
	display.fill((0,0,0xff))
	
	
	func_dict = { "status": draw_status, "inventory": draw_inventory, "gear": draw_gear, "save": draw_save }
	submenu = UI_SubmenuPane("submenu_pane", (140,10), (300,300), func_dict)
	
	labels = [ "Inventory", "Status", "Gear", "Save" ]
	livemenu = UI_LiveMenu("livemenu", (10,10), (120,300), submenu, labels)
	
	while 1:
	
		livemenu.update()
		livemenu.render(display)
		
		pygame.display.flip()
		display.fill((0,0,0xff))
