#

import pygame

class UIInventory(object):

	def __init__(self, uid, engine, loc, size):
	
		self.uid = uid
		self.engine = engine
		self.x, self.y = loc
		self.w, self.h = size
		
		self.back = pygame.Surface((self.w, self.h)).convert_alpha()
		self.back.fill((0,0,0,127))
	
		self.visible = False
	
		self.value = 0
		self.selValue = 0
		self.selected = False
		
		print("UIInventory initialized")
	
	def normalize_cursor(self):
	
		inv = self.engine.playerCharacter.inventory
		count = 0
		while inv[count] == None and count < 7:
			count += 1
		self.value = count
	
	def start(self):
	
		self.selected = False
		self.normalize_cursor()
		
		self.engine.uiQueue.append(self)
		self.engine.controlFocus = self
		self.visible = True
				
	def stop(self):
	
		self.visible = False
		self.engine.ui_pop() # change this to self.engine.ui_pop()
		
	def is_empty(self):
	
		for i in range(8):
			if self.engine.playerCharacter.inventory[i] != None:
				return False
		return True
	
	def update(self):
	
		if self.visible and self.engine.controlFocus == self:
			yAxis = self.engine.keyListener.controls["yAxis_A"]
			
			aButton = self.engine.keyListener.controls["A"]
			bButton = self.engine.keyListener.controls["B"]
			
			if yAxis != 0:
				inv = self.engine.playerCharacter.inventory
				if not self.selected:
					self.value = (self.value + yAxis) % 8
					while inv[self.value] == None:
						self.value = (self.value + yAxis) % 8
					
				if self.selected:
					self.selValue = (self.selValue + yAxis) % 8
			
			if aButton == 1:
				if self.is_empty():
					self.stop()
					return
					
				if self.selected:
					if self.value == self.selValue:
						#print("Item is doing a thing")
						inv = self.engine.playerCharacter.inventory
						item, quantity = inv[self.value]
						item.effect()
						if item.consumable: inv[self.value][1] -= 1
						if item.consumable and inv[self.value][1] == 0:
							inv[self.value] = None
							self.normalize_cursor()
						self.selected = False
						return
					elif self.value != self.selValue:
						inv = self.engine.playerCharacter.inventory
						a = {}
						a[self.selValue] = inv[self.value]
						a[self.value] = inv[self.selValue]
						for i in a.keys():
							inv[i] = a[i]
						self.value = self.selValue
						self.selected = False
						return
						
				if not self.selected:
					self.selected = True
					self.selValue = self.value
				
			elif bButton == 1:
				if not self.selected:
					self.stop()
					return
				if self.selected:
					self.selected = False
				
	def render(self):
	
		if self.visible:
			self.engine.canvas.blit(self.back, (self.x, self.y))
		
			inv = self.engine.playerCharacter.inventory
			for i in range(8):
				label = ""
				if inv[i] != None:
					label += inv[i][0].label
					if inv[i][1] > 1:	label += " " + str(inv[i][1])
					if i == self.value:	label += " <"
				if self.selected and i == self.selValue:
						label = label + "<"
				if label != "":
					x = self.x + 5 # padding
					y = self.y + 5 * (i+1) + i * self.engine.uiTheme["font"].get_height() # 0:15; 1:40; 2:65
					txtImg = self.engine.uiTheme["font"].render(label, 0, (0xff,0xff,0xff))
					self.engine.canvas.blit(txtImg, (x,y))
