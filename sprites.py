import pygame
from pygame.locals import *

from classes import *

class BoardSprite(Board, pygame.sprite.Sprite):

	overlay = None

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		Board.__init__(self)
		
		self.w = BSIZE*BWIDTH
		self.image = pygame.Surface((self.w, self.w))
		for i in xrange(BSIZE):
			pygame.draw.line(self.image, (255, 255, 255, 255), (i*BWIDTH, 0), (i*BWIDTH, self.w))
			pygame.draw.line(self.image, (255, 255, 255, 255), (0, i*BWIDTH), (self.w, i*BWIDTH))
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
					if(i >= self.spawn and i < self.spawn+4 and j >= self.spawn and j < self.spawn+4	):
						self.image.fill((100, 50, 50), self.get_cell_rect(i, j))
					else:
						self.image.fill((0, 0, 0), self.get_cell_rect(i, j))
				
		count = 0
		for t in self.tetrimo:
			for j in xrange(t.w):
				for i in xrange(t.h):
					if(t[i][j]):
						self.image.fill(t.color, self.get_cell_rect(t.topleft[0]+i, t.topleft[1]+j))
						if(self.overlay):
							self.image.blit(self.overlay[count], self.get_cell_rect(t.topleft[0]+i, t.topleft[1]+j))
							count+=1