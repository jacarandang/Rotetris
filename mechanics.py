import pygame
from pygame.locals import *

from threading import Thread

class RandomEvents(Thread):

	def __init__(self, eq, board, screen):
		Thread.__init__(self)
		self.eq = eq
		self.board = board
		self.screen = screen

	def run(self):
		for i in xrange(100):
			print str(i) + " " + self.name + "\n"

	def doge(self):
		pass
		
r1 = RandomEvents(None, None)
r2 = RandomEvents(None, None)
r3 = RandomEvents(None, None)

r1.start()
r2.start()
r3.start()