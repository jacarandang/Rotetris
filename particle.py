import pygame
from pygame.locals import *

from random import randint
from time import time
pygame.init()

class Particle(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((9, 9))	.convert()
		self.image.fill((0, 0, 0))
		pygame.draw.circle(self.image, (randint(0, 255), randint(0, 255), randint(0, 255)), (4, 4), 4)
		self.rect = self.image.get_rect()
		self.vx = randint(-10, 10)
		self.vy = randint(-10, 10)
		self.x = 400
		self.y = 300
		self.rect.center = self.x, self.y

	def update(self):
		self.x += self.vx
		self.y += self.vy
		self.rect.center = (self.x, self.y)
		if(self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600):
			self.kill()

class Emitter(pygame.sprite.Group):

	def __init__(self, l, w, scr):
		pygame.sprite.Group.__init__(self)
		self.spawnl = l
		self.spawnw = w
		self.timer = time()
		self.scr = scr

	def update(self):
		pygame.sprite.Group.update(self)
		if(time() - self.timer > .25):
			self.timer = time()
			for i in xrange(50):
				self.add(Particle())
		self.draw(self.scr)

def main():
	pygame.init()
	SCREEN = pygame.display.set_mode((800, 600))
	BG = pygame.Surface(SCREEN.get_size()).convert()
	BG.fill((0, 0, 0))

	e = Emitter(1, 1, SCREEN)
	run = True

	clock = pygame.time.Clock()
	while(run):

		clock.tick(60)

		for event in pygame.event.get():
			if event.type == QUIT:
				run = False

		SCREEN.blit(BG, (0, 0))
		e.update()
		pygame.display.update()

if __name__ == '__main__':
	main()