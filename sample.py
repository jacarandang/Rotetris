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


		
def pause():
	while(True):
		for event in pygame.event.get():
			if event.type == QUIT:
				return
			elif event.type == KEYDOWN:
				if event.key == K_p:
					return
				
class EventQ():

	def __init__(self, board):
		self.board = board
		self.board.eq = self
		self.tet = None
		self.alist = []
		for i in xrange(4):
			self.alist.append(load_image(D_LIST[i][2], -1))
			self.alist[i].set_alpha(125)
		self.arrow = None
		
	def next_tetrimo(self):
		self.tet = Tetrimo(choice(B_LIST), (self.board.spawn+1, self.board.spawn+1), choice(D_LIST))
		self.board.add_tetrimo(self.tet)
		self.arrow = self.alist[D_LIST.index(self.tet.direction)]

	def move_left(self):
		self.board.move(D_LIST[(D_LIST.index(self.tet.direction) + 1)%4])

	def move_right(self):
		self.board.move(D_LIST[D_LIST.index(self.tet.direction) - 1])


class Game():

	def __init__(self, level, screen):
		self.level = level
		self.screen = screen

		self.allsprite = pygame.sprite.Group()
		self.board = BoardSprite()
		self.allsprite.add(self.board)

		self.eq = EventQ()
		eq.next_tetrimo()

		self.clock = pygame.time.Clock()
		self.speed = 1.00
		self.running = True

		self.timer = time()

	def start(self):
		while(self.running):
			self.clock.tick(FPS)

			if(self.timer - time() >= 1/self.speed):
				self.timer = time()
				self.board.move()

			self.event()

	def event(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.running = False
			elif event.type == KEYDOWN:
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
		pass

o = load_image("overlay.jpg").convert()
o = pygame.transform.scale(o, (BWIDTH, BWIDTH))
o.set_alpha(100)
BoardSprite.overlay = [o, o.copy(), o.copy(), o.copy()]
		
allsprite = pygame.sprite.Group()
board = BoardSprite()
allsprite.add(board)

eq = EventQ(board)
eq.next_tetrimo()

clock = pygame.time.Clock()	
speed = 1.00
timer = time()
running = True

while(running):
	clock.tick(60)
	if(time() - timer >= 1/speed):
		timer = time()
		board.move()
		# if(randint(0, 100) <= 50):
			# print "rotate"
			# choice([board.rotateL, board.rotateR])()
	
	if(board.is_over()):
		running = False
	
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		elif event.type == KEYDOWN:
			if event.key == K_UP:
				eq.tet.rotateL()
			elif event.key == K_DOWN:
				speed = 4.50
			elif event.key == K_LEFT:
				eq.move_left()
			elif event.key == K_RIGHT:
				eq.move_right()
			elif event.key == K_SPACE:
				board.drop()
			elif event.key == K_p:
				pause()
		elif event.type == KEYUP:
			if event.key == K_DOWN:
				speed = 1

	allsprite.update()
			
	SCREEN.blit(BG, (0, 0))
	allsprite.draw(SCREEN)
	SCREEN.blit(eq.arrow, (50, 35))
	pygame.display.update()
	
sleep(1)
if board.is_over():
	print "..."
	img = FONT.render("GAME OVER!", False, (255, 255, 0))
	rect = img.get_rect()
	SCREEN.blit(BG, (0, 0))
	rect.center = (400, 300)
	SCREEN.blit(img, rect)
	pygame.display.update()
	sleep(3)
	
pygame.quit()
