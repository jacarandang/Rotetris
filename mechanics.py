import pygame
from pygame.locals import *

from threading import Thread
from time import *

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

class RandomEvents(Thread):

	def __init__(self, eq, board, screen):
		Thread.__init__(self)
		self.eq = eq
		self.board = board
		self.screen = screen
		self.doge_img = load_image("doge.png")

	def run(self):
		pass

	def doge(self):
		self.screen.blit(self.doge_img, (0, 0))
		pygame.display.update()
		sleep(.75)
		
		
r1 = RandomEvents(None, None)
r2 = RandomEvents(None, None)
r3 = RandomEvents(None, None)

r1.start()
r2.start()
r3.start()