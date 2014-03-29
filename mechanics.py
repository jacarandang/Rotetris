import pygame
from pygame.locals import *

from os import path
from threading import Thread
from time import *
from random import randint, choice

from globals import *

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

class RandomEvents():

	def __init__(self, game, eq, board, screen):
		self.game = game
		self.eq = eq
		self.board = board
		self.screen = screen
		self.doge_img = load_image("doge.png")
		self.running = False

		self.bark = pygame.mixer.music.load(path.join("resource", "music", "bark.ogg"))
		self.events = [self.speed_up, self.speed_down, self.doge, self.board_rotate]
		self.chance = 40
		if(self.game.level == NORMAL): self.chance = 10
		elif(self.game.level == HARD): self.chance = 25
		elif(self.game.level == EXTREME):
			self.events.append(self.tetrimo_rotate)
		self.timer = 0

	def run(self):
		while(self.running):
			sleep(1)
			if(time() - self.timer > 10):
				n = randint(1, 100)
				if(n <= self.chance):
					choice(self.events)()
				self.timer = time()

	def stop(self):
		self.running = False

	def start(self):
		self.running = True
		t = Thread(target = self.run)
		self.timer = time()
		t.start()
		return t

	def doge(self):
		self.eq.pauseG()
		self.screen.blit(self.doge_img, (0, 0))
		pygame.mixer.music.play()
		pygame.display.update()
		sleep(1)
		self.eq.playG()

	def tetrimo_rotate(self):
		choice([self.eq.tet.rotateL, self.eq.tet.rotateL])()

	def board_rotate(self):
		choice([self.board.rotateL, self.board.rotateR])()

	def speed_up(self):
		self.game.ospeed *= 2.00
		self.game.speed = self.game.ospeed
		sleep(5)
		self.game.ospeed /= 2.00
		self.game.speed = self.game.ospeed

	def speed_down(self):
		self.game.ospeed /= 2.00
		self.game.speed = self.game.ospeed
		sleep(5)
		self.game.ospeed *= 2.00
		self.game.speed = self.game.ospeed