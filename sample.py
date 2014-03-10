import pygame
from pygame.locals import *

from time import time, sleep

from random import *
#CONSTANTS AND GLOBALS
BSIZE = 16
BWIDTH = 37

B_L	 = ((0, 0), (1, 0), (2, 0), (2, 1), 2, 3, (255, 0, 0))
B_RL = ((0, 1), (1, 1), (2, 1), (2, 0), 2, 3, (0, 255, 0))
B_S  = ((0, 0), (1, 0), (1, 1), (2, 1), 2, 3, (0, 0, 255))
B_RS = ((0, 1), (1, 1), (1, 0), (2, 0), 2, 3, (255, 255, 0))
B_ST = ((0, 0), (1, 0), (2, 0), (3, 0), 1, 4, (255, 0, 255))
B_SQ = ((0, 0), (1, 1), (1, 0), (0, 1), 2, 2, (0, 255, 255))
B_LIST = [B_L, B_RL, B_S, B_RS, B_ST, B_SQ]

FPS = 60

NORTH = (-1, 0, "up.png")
SOUTH = (1, 0, "down.png")
WEST  = (0, -1, "left.png")
EAST  = (0, 1, "right.png")
D_LIST = [NORTH, EAST, SOUTH, WEST]
#END

pygame.init()
pygame.font.init()
pygame.key.set_repeat(100, 70)

SCREEN = pygame.display.set_mode((800, 600))
BG = pygame.Surface(SCREEN.get_size()).convert()
BG.fill((100, 100, 100))
FONT = pygame.font.Font(None, 30)

def load_image(file, colorkey = None):
	surf = pygame.image.load(file).convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

class Board():

	def __init__(self):
		self.board = []
		for i in xrange(BSIZE):
			self.board.append([None]*BSIZE)
		
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				self.board[i][j] = 0
		
		self.tetrimo = []
		self.eq = None
		self.spawn = (BSIZE - 4)/2
	def __getitem__(self, idx):
		return self.board[idx]
		
	def add_tetrimo(self, tetrimo):
		self.tetrimo.append(tetrimo)
		
	def move(self, dirc = None):
		for t in self.tetrimo:
			dir = t.direction
			if dirc is not None:
				dir = dirc
			ni = t.topleft[0] + dir[0]
			nj = t.topleft[1] + dir[1]
			if(ni >= 0 and nj >= 0 and ni+t.h <= BSIZE and nj+t.w <= BSIZE):
				valid = True
				for i in xrange(t.h):
					for j in xrange(t.w):
						if(t[i][j] and self[ni+i][nj+j]):
							valid = False
					if not valid: break
				if valid:
					t.topleft = (ni, nj)
				else:
					if dirc is None:	
						self.place(t)
						self.tetrimo.remove(t)
			else:
				if dirc is None:
					self.place(t)
					self.tetrimo.remove(t)
	
	def drop(self):
		tet = self.tetrimo[0]
		while(tet == self.tetrimo[0]):
			self.move()
			
	def place(self, t):
		for i in xrange(t.h):
			for j in xrange(t.w):
				if(t[i][j]):
					self[t.topleft[0]+i][t.topleft[1]+j] = 1
		self.eq.next_tetrimo()
		self.line_clear()
	
	def is_over(self):
		for i in xrange(4):
			for j in xrange(4):
				if(self[self.spawn+i][self.spawn+j]):
					return True
		return False
	
	def line_clear(self):
		for i in xrange(((BSIZE-4)/2) - 1, -1, -1):
			lc = True
			for j in xrange(BSIZE):
				if not self[i][j]:
					lc = False
					break
			if lc:
				for j in xrange(i, ((BSIZE-4)/2) - 1):
					for k in xrange(BSIZE):
						self[j][k] = self[j+1][k]
				for j in xrange(BSIZE):
					self[((BSIZE-4)/2)-1][j] = 0

		for i in xrange(((BSIZE-4)/2) - 1, -1, -1):
			lc = True
			for j in xrange(BSIZE):
				if not self[j][i]:
					lc = False
					break
			if lc:
				for j in xrange(i, ((BSIZE-4)/2) - 1):
					for k in xrange(BSIZE):
						self[k][j] = self[k][j+1]
				for j in xrange(BSIZE):
					self[j][((BSIZE-4)/2)-1] = 0

		for i in xrange(((BSIZE+4)/2) , BSIZE):
			lc = True
			for j in xrange(BSIZE):
				if not self[i][j]:
					lc = False
					break
			if lc:
				for j in xrange(i, ((BSIZE+4)/2) + 1, -1):
					for k in xrange(BSIZE):
						self[j][k] = self[j-1][k]
				for j in xrange(BSIZE):
					self[((BSIZE+4)/2)][j] = 0

		for i in xrange(((BSIZE+4)/2) , BSIZE):
			lc = True
			for j in xrange(BSIZE):
				if not self[j][i]:
					lc = False
					break
			if lc:
				for j in xrange(i, ((BSIZE+4)/2) + 1, -1):
					for k in xrange(BSIZE):
						self[k][j] = self[k][j-1]
				for j in xrange(BSIZE):
					self[j][((BSIZE+4)/2)] = 0

	def rotateL(self):
		narr = []
		for i in xrange(BSIZE):
			narr.append([None]*BSIZE)
			
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[i][j] = 0
		
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[BSIZE-1-j][i] = self[i][j]
				
		self.board = narr
		
	def rotateR(self):
		narr = []
		for i in xrange(BSIZE):
			narr.append([None]*BSIZE)
			
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[i][j] = 0
		
		for i in xrange(BSIZE):
			for j in xrange(BSIZE):
				narr[j][BSIZE-1-i] = self[i][j]
				
		self.board = narr
		
	def rotate_tetrimo_L(self):
		pass
		
	def rotate_tetrimo_R(self):
		pass
		
class Tetrimo():

	def __init__(self, type, topleft, direction):
		self.layout = []
		for i in xrange(4):
			self.layout.append([None]*4)
		
		for i in xrange(4):
			for j in xrange(4):
				self.layout[i][j] = 0
				
		for i in xrange(4):
			self.layout[type[i][0]][type[i][1]] = 1
		
		self.w = type[4]
		self.h = type[5]
		self.color = type[6]
		self.topleft = topleft
		self.direction = direction
		
	def rotateL(self):	#checking
		narr = []
		for i in xrange(4):
			narr.append([None]*4)
			
		for i in xrange(4):
			for j in xrange(4):
				narr[i][j] = 0
		
		for i in xrange(self.h):
			for j in xrange(self.w):
				narr[self.w-1-j][i] = self[i][j]
				
		self.layout = narr
		self.w, self.h = self.h, self.w
		
	def rotateR(self):	#checking
		narr = []
		for i in xrange(4):
			narr.append([None]*4)
			
		for i in xrange(4):
			for j in xrange(4):
				narr[i][j] = 0
		
		for i in xrange(self.h):
			for j in xrange(self.w):
				narr[j][self.h-1-i] = self[i][j]
				
		self.layout = narr
		self.w, self.h = self.h, self.w
		
	def __getitem__(self, idx):
		return self.layout[idx]
		
class BoardSprite(Board, pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		Board.__init__(self)
		
		self.w = BSIZE*BWIDTH
		self.image = pygame.Surface((self.w, self.w))
		for i in xrange(BSIZE):
			pygame.draw.line(self.image, (255, 255, 255), (i*BWIDTH, 0), (i*BWIDTH, self.w))
			pygame.draw.line(self.image, (250, 250, 250), (0, i*BWIDTH), (self.w, i*BWIDTH))
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
				
		for t in self.tetrimo:
			for j in xrange(t.w):
				for i in xrange(t.h):
					if(t[i][j]): self.image.fill(t.color, self.get_cell_rect(t.topleft[0]+i, t.topleft[1]+j))
				
class EventQ():

	def __init__(self, board):
		self.board = board
		self.board.eq = self
		self.tet = None
		self.tdir = None
		self.alist = []
		for i in xrange(4):
			self.alist.append(load_image(D_LIST[i][2], -1))
			self.alist[i].set_alpha(125)
		self.arrow = None
		
	def next_tetrimo(self):
		self.tet = Tetrimo(choice(B_LIST), (self.board.spawn, self.board.spawn), choice(D_LIST))
		self.board.add_tetrimo(self.tet)
		self.tdir = FONT.render(self.tet.direction[2], False, (255, 0, 0))
		self.arrow = self.alist[D_LIST.index(self.tet.direction)]

	def move_left(self):
		self.board.move(D_LIST[(D_LIST.index(self.tet.direction) + 1)%4])

	def move_right(self):
		self.board.move(D_LIST[D_LIST.index(self.tet.direction) - 1])

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
		# if(randint(0, 100) <= 2):
			# print "rotate"
			# choice([board.rotateL, board.rotateR])()
	
	if(board.is_over()):
		running = False
	
	for event in pygame.event.get():
		if event.type == QUIT:
			running = False
		if event.type == KEYDOWN:
			if event.key == K_UP:
				eq.tet.rotateL()
			elif event.key == K_DOWN:
				eq.tet.rotateR()
			elif event.key == K_LEFT:
				eq.move_left()
			elif event.key == K_RIGHT:
				eq.move_right()
			elif event.key == K_SPACE:
				board.drop()
	allsprite.update()
			
	SCREEN.blit(BG, (0, 0))
	allsprite.draw(SCREEN)
	SCREEN.blit(eq.tdir, (650, 50))
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