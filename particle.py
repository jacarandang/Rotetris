import pygame
from pygame.locals import *

from random import randint
from time import time
pygame.init()

class Particle(pygame.sprite.Sprite):

	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)	
		self.image = pygame.Surface((10, 10)).convert()
		self.image.fill((0, 0, 0))
		pygame.draw.circle(self.image, (randint(0, 255), randint(0, 255), randint(0, 255)), (5, 5), 5)
		self.rect = self.image.get_rect()
		self.vx = randint(-5, 5)
		self.vy = randint(-5, 5)
		self.x = x
		self.y = y
		self.rect.center = self.x, self.y

	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.vy += -.1
		self.vx += .1
		self.rect.center = (self.x, self.y)
		if(self.x < 0 or self.x > 1024 or self.y < 0 or self.y > 768):
			self.kill()

class Emitter(pygame.sprite.Group):

	def __init__(self, (x, y), (l, w), scr):
		pygame.sprite.Group.__init__(self)
		self.x = x
		self.y = y
		self.spawnl = l
		self.spawnw = w
		self.timer = time()
		self.scr = scr

	def update(self):
		pygame.sprite.Group.update(self)
		self.draw(self.scr)

	def emit(self, n):
		for i in xrange(n):
				self.add(Particle(randint(self.x, self.x+self.spawnl), randint(self.y, self.y+self.spawnw)))
def main():
	pygame.init()
	SCREEN = pygame.display.set_mode((1024, 768))
	BG = pygame.Surface(SCREEN.get_size()).convert()
	BG.fill((0, 0, 0))

	e = Emitter((512, 384), (100, 10), SCREEN)
	run = True

	sprite = pygame.Surface((100, 10)).convert()
	sprite.fill((100, 100, 100))
	rect= sprite.get_rect()
	rect.topleft = 512, 384

	clock = pygame.time.Clock()
	while(run):

		clock.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			if event.type == KEYDOWN:
				if event.key == K_SPACE:
					e.emit(200)

		SCREEN.blit(BG, (0, 0))
		e.update()
		SCREEN.blit(sprite, rect)
		pygame.display.update()

if __name__ == '__main__':
	main(); pygame.quit()
