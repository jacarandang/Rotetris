import pygame
from pygame.locals import *

from time import time, sleep
from random import *
from os import path

from particle import *
from globals import *
from classes import *
from sprites import *

pygame.init()
pygame.font.init()
pygame.key.set_repeat(100, 70)

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

SCREEN = pygame.display.set_mode((800, 600))
BG = load_image('Board.png')
FONT = pygame.font.Font(None, 30)

class EventQ():

	def __init__(self, board, level):
		self.board = board
		self.board.eq = self
		self.tet = None
		self.alist = []
		self.level = level
		for i in xrange(4):
			self.alist.append(load_image(D_LIST[i][2], -1))
			self.alist[i].set_alpha(150)
		self.arrow = None
		
		self.hshift =  False
		self.hold  =  None

	def next_tetrimo(self, layout = None):
		self.tet = None
		if not layout:
			self.tet = Tetrimo(choice(B_LIST), (self.board.spawn+1, self.board.spawn+1), choice(D_LIST))
		else:
			self.tet = Tetrimo(layout, (self.board.spawn+1, self.board.spawn+1), choice(D_LIST))
		self.board.add_tetrimo(self.tet)
		self.arrow = self.alist[D_LIST.index(self.tet.direction)]
		self.hshift = False

	def move_left(self):
		self.board.move(D_LIST[(D_LIST.index(self.tet.direction) + 1)%4])

	def move_right(self):
		self.board.move(D_LIST[D_LIST.index(self.tet.direction) - 1])

	def shift(self):
		if not self.hshift:
			print "shifting"
			self.hshift = True
			if(self.hold):
				tmp = self.hold
				self.hold = self.tet.ttype
				self.board.remove(self.tet)
				self.next_tetrimo(tmp)
				self.hshift = True

			else:
				self.hold = self.tet.ttype
				self.board.remove(self.tet)
				self.next_tetrimo()
				self.hshift = True

class Game():

	def __init__(self, level, screen):
		self.level = level
		self.screen = screen

		self.allsprite = pygame.sprite.Group()
		self.board = BoardSprite()
		self.allsprite.add(self.board)

		self.font = pygame.font.Font(None, 30)
		self.tsprite = Timer(self.font, (700, 115))
		self.allsprite.add(self.tsprite)

		self.eq = EventQ(self.board, level)
		self.eq.next_tetrimo()

		self.clock = pygame.time.Clock()
		self.speed = 1.00
		self.running = True

		self.timer = time()

	def start(self):
		self.tsprite.start()
		while(self.running):
			self.clock.tick(FPS)

			if(time() - self.timer >= 1/self.speed):
				print "drop"
				self.timer = time()
				self.board.move()

			self.event()

			if(self.board.is_over()):
				self.running = False

			self.allsprite.update()
			
			self.screen.blit(BG, (0, 0))
			self.allsprite.draw(self.screen)
			self.screen.blit(self.eq.arrow, (50, 35))
			pygame.display.update()
		self.tsprite.stop()

	def event(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.running = False
			elif event.type == KEYDOWN or event.type == KEYUP:
				self.keydown(event)

	def pause(self):
		while(True):
			for event in pygame.event.get():
				if event.type == QUIT:
					return
				elif event.type == KEYDOWN:
					if event.key == K_p:
						return
	
	def keydown(self, event):
		if(self.level == HARD or self.level == EXTREME): pass
		else:
			pass
		if(event.type == KEYDOWN):
			if event.key == K_UP:
				self.eq.tet.rotateL()
			elif event.key == K_DOWN:
				self.speed = 4.50
			elif event.key == K_LEFT:
				self.eq.move_left()
			elif event.key == K_RIGHT:
				self.eq.move_right()
			elif event.key == K_SPACE:
				self.board.drop()
			elif event.key == K_p:
				self.pause()
			elif event.key == K_LSHIFT:
				self.eq.shift()
		elif event.type == KEYUP:
			if event.key == K_DOWN:
				self.speed = 1


o = load_image("overlay.png").convert()
o = pygame.transform.scale(o, (BWIDTH - 1, BWIDTH - 1))
o.set_alpha(100)
BoardSprite.overlay = [o, o.copy(), o.copy(), o.copy()]
	
g = Game(EASY, SCREEN)
g.start()

sleep(1)
img = FONT.render("GAME OVER!", False, (255, 255, 0))
rect = img.get_rect()
SCREEN.blit(BG, (0, 0))
rect.center = (400, 300)
SCREEN.blit(img, rect)
pygame.display.update()
sleep(3)
	
pygame.quit()
