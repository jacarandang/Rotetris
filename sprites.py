import pygame
from pygame.locals import *

from classes import *
from globals import *

from threading import Thread
from time import time, sleep

class BoardSprite(Board, pygame.sprite.Sprite):

	overlay = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		Board.__init__(self)
		
		self.w = BSIZE*BWIDTH
		self.image = pygame.Surface((self.w, self.w)).convert_alpha()
		self.image.fill((0, 0, 0, 0))
		self.rect = self.image.get_rect()
		
	def update(self):
		self.render()
		
	def get_cell_rect(self, row, col):
		return pygame.Rect(col*BWIDTH+1, row*BWIDTH+1, BWIDTH-1, BWIDTH-1)
		
	def render(self):
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				if(self[i][j]): self.image.fill((100, 100, 100), self.get_cell_rect(i, j))
				else:	
					self.image.fill((0, 0, 0, 0), self.get_cell_rect(i, j))
				
		count = 0
		for t in self.tetrimo:
			for j in xrange(t.w):
				for i in xrange(t.h):
					if(t[i][j]):
						self.image.fill(t.color, self.get_cell_rect(t.topleft[0]+i, t.topleft[1]+j))
						if(self.overlay):
							self.image.blit(self.overlay[count], self.get_cell_rect(t.topleft[0]+i, t.topleft[1]+j))
							count+=1

class Button(pygame.sprite.Sprite):

	def __init__(self, image, (x, y), action, selected = False):
		pygame.sprite.Sprite.__init__(self)
		if(selected):
			image = pygame.transform.scale(image, (image.get_width()+20, image.get_height()+20))
		self.bimage = image
		self.image = image.copy()
		self.rect = self.image.get_rect()
		self.action = action

		self.enlarged = False

		self.x = x
		self.y = y
		self.rect.center = self.x, self.y

	def update(self):
		if(self.rect.collidepoint(pygame.mouse.get_pos())):
			if not self.enlarged:
				self.enlarged = True
				self.rect.inflate_ip(20, 20)
				self.image = pygame.transform.scale(self.bimage, (self.rect.size))
		else:
			if self.enlarged:
				self.enlarged = False
				self.rect.inflate_ip(-20, -20)
				self.image = pygame.transform.scale(self.bimage, (self.rect.size))

	def click(self):
		if(self.rect.collidepoint(pygame.mouse.get_pos())):
			self.action()
			return True
		return False

class Timer(pygame.sprite.Sprite):

	def __init__(self, font, (x, y)):
		pygame.sprite.Sprite.__init__(self)

		self.running = False

		self.font = font
		self.btime = 0
		self.image = self.font.render("0:00", False, (0, 0, 0))
		self.rect = self.image.get_rect()
		self.x, self.y = x, y
		self.rect.center = self.x, self.y

	def update(self):
		pass

	def start(self):
		self.running = True
		t = Thread(target = self.count)
		self.btime = time()
		t.start()
		return t

	def count(self):
		while(self.running):
			sleep(1)
			t = time() - self.btime
			tmp = str(int(t/60))+":"
			if(t%60 < 10): tmp += "0"+str(int(t%60))
			else: tmp+=  str(int(t%60))
			self.image = self.font.render(tmp, False, (0, 0, 0))
			self.rect = self.image.get_rect()
			self.rect.center = self.x, self.y

	def stop(self):
		self.running = False

class Text(pygame.sprite.Sprite):

	def __init__(self, font, fxn, (x, y)):
		pygame.sprite.Sprite.__init__(self)
		self.font = font
		self.fxn  = fxn
		self.dt = fxn()
		self.image = self.font.render(str(self.dt), False, (0, 0, 0))
		self.rect = self.image.get_rect()
		self.x, self.y = x, y
		self.rect.center = self.x, self.y

	def update(self):
		if(self.dt != self.fxn()):
			self.dt = self.fxn()
			self.image = self.font.render(str(self.dt), False, (0, 0, 0))
			self.rect = self.image.get_rect()
		self.rect.center = self.x, self.y

class Hold(pygame.sprite.Sprite):

	overlay = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.hold = None
		self.image = pygame.Surface((BWIDTH*4, BWIDTH*4)).convert_alpha()
		self.image.fill((255, 255, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.center = 700, 500

	def update(self):
		pass

	def render(self, layout):
		w = layout[4]
		h = layout[5]
		self.image = pygame.Surface((BWIDTH*w - 1, BWIDTH*h - 1)).convert_alpha()
		self.image.fill((255, 255, 255, 0))
		for i in xrange(4):
			self.image.fill(layout[6], pygame.Rect(layout[i][1]*BWIDTH, layout[i][0]*BWIDTH, BWIDTH-1, BWIDTH - 1))
			if self.overlay is not None:
				self.image.blit(self.overlay[i], pygame.Rect(layout[i][1]*BWIDTH, layout[i][0]*BWIDTH, BWIDTH-1, BWIDTH - 1))
		self.rect = self.image.get_rect()
		self.rect.center = 700, 500