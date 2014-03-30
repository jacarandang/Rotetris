import pygame
from pygame.locals import *

from time import time, sleep
from random import *
from os import path

from particle import *
from globals import *
from classes import *
from sprites import *
from mechanics import *

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

def foo():
	pass

class EventQ():

	def __init__(self, board, level, game, holdSp = None):
		self.board = board
		self.board.eq = self
		self.tet = None
		self.alist = []
		self.level = level
		self.game = game
		for i in xrange(4):
			self.alist.append(load_image(D_LIST[i][2], -1))
			self.alist[i].set_alpha(150)
		self.arrow = None
		
		self.hshift =  False
		self.hold  =  None
		self.holdSp = holdSp
		self.pause = False

	def next_tetrimo(self, layout = None):
		self.tet = None
		self.game.speed = self.game.ospeed
		if not layout:
			if(self.level == EASY):
				self.tet = Tetrimo(choice(B_LIST), (self.board.spawn+1, self.board.spawn+1), choice([NORTH, SOUTH]))
			else:	
				self.tet = Tetrimo(choice(B_LIST), (self.board.spawn+1, self.board.spawn+1), choice(D_LIST))
		else:
			if(self.level == EASY):
				self.tet = Tetrimo(layout, (self.board.spawn+1, self.board.spawn+1), choice([NORTH, SOUTH]))
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
			self.hshift = True
			if(self.hold):
				tmp = self.hold
				self.hold = self.tet.ttype
				self.board.remove(self.tet)
				self.next_tetrimo(tmp)
				self.hshift = True
				if(self.holdSp):
					self.holdSp.render(self.hold)

			else:
				self.hold = self.tet.ttype
				self.board.remove(self.tet)
				self.next_tetrimo()
				self.hshift = True
				if(self.holdSp): self.holdSp.render(self.hold)

	def pauseG(self):
		self.pause = True

	def playG(self):
		self.pause = False

class Game():

	def __init__(self, level, screen):
		self.level = level
		self.screen = screen

		self.bg = load_image("Board.png")
		self.bgm = pygame.mixer.Sound(path.join("resource", "music", "dubstep.ogg"))
		self.bgm.play(-1)
		self.bgm.set_volume(settings["volume"])

		o = load_image("overlay.png").convert()
		o = pygame.transform.scale(o, (BWIDTH - 1, BWIDTH - 1))
		o.set_alpha(100)
		BoardSprite.overlay = [o, o.copy(), o.copy(), o.copy()]
		Hold.overlay = [o.copy(), o.copy(), o.copy(), o.copy()]

		self.allsprite = pygame.sprite.Group()
		self.board = BoardSprite()
		self.allsprite.add(self.board)
		self.speed = 1.00
		self.ospeed = 1.00

		self.font = pygame.font.Font(path.join("resource", "font", "arro_terminal.ttf"), 30)
		self.tsprite = Timer(self.font, (700, 115))
		self.lcsprite = Text(self.font, lambda: self.board.lineclears, (700, 260))		#lineclear
		self.mdsprite = Text(self.font, lambda: MODETEXT[self.level], (700, 330))		#level
		self.spsprite = Text(self.font, lambda: self.speed, (700, 375))					#speed
		self.hssprite = Text(self.font, lambda: settings["highscore"][self.level], (700, 185))
		self.allsprite.add(self.tsprite, self.lcsprite, self.mdsprite, self.spsprite, self.hssprite)

		self.holdSprite = Hold()
		self.allsprite.add(self.holdSprite)

		self.eq = EventQ(self.board, level, self, self.holdSprite)
		self.eq.next_tetrimo()

		self.mechanics = RandomEvents(self, self.eq, self.board, self.screen)

		self.clock = pygame.time.Clock()
		if(self.level == EXTREME):
			self.speed *= 2
			self.ospeed *= 2
		self.running = True
		self.quit = False

		self.timer = time()

	def start(self):
		tthread = self.tsprite.start()
		if(self.level > EASY): mthread = self.mechanics.start()

		while(self.running and not self.quit):
			self.clock.tick(FPS)

			if(time() - self.timer >= 1/self.speed):
				self.timer = time()
				self.board.move()

			self.event()

			if(self.board.is_over()):
				self.running = False

			self.allsprite.update()
		
			while(self.eq.pause):
				pass

			self.screen.blit(self.bg, (0, 0))
			self.allsprite.draw(self.screen)
			self.screen.blit(self.eq.arrow, (50, 35))
			pygame.display.update()

		self.tsprite.stop()
		self.mechanics.stop()
		tthread.join()
		if(self.level > EASY): mthread.join()
		if(self.board.is_over()):
			self.gameover()
			if self.board.lineclears > settings["highscore"][self.level]:
				settings["highscore"][self.level] = self.board.lineclears
				save_settings()
		self.bgm.stop()

	def event(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.running = False
				self.quit = True
			elif event.type == KEYDOWN or event.type == KEYUP:
				self.keydown(event)

	def pause(self):
		bg = load_image("Pausepg.png")
		olay = pygame.Surface((800, 600)).convert_alpha()
		olay.fill((0, 0, 0, 120))

		resume = pygame.image.load(path.join("resource", "Start.png")).convert_alpha()
		resumeb = Button(resume, (400, 250), foo)

		quit = pygame.image.load(path.join("resource", "Quit.png")).convert_alpha()
		quitb = Button(quit, (400, 350), foo)

		tsprite = pygame.sprite.Group()
		tsprite.add(resumeb, quitb)

		while(True):
			for event in pygame.event.get():
				if event.type == QUIT:
					self.quit = True
					return
				elif event.type == KEYDOWN:
					if event.key == K_p or event.key == K_ESCAPE:
						return
				elif event.type == MOUSEBUTTONDOWN:
					for sprite in tsprite:
						c = sprite.click()
						if(c and sprite == resumeb):
							return
						elif c and sprite == quitb:
							self.quit = True
							return
			tsprite.update()

			self.screen.blit(bg, (0, 0))
			self.screen.blit(olay, (0, 0))
			tsprite.draw(self.screen)
			pygame.display.flip()
	
	def keydown(self, event):
		if(settings["control"] == 1):
			if(event.type == KEYDOWN):
				if event.key == K_UP:
					self.eq.board.rotate_tetrimo_L()
				elif event.key == K_DOWN:
					self.speed = self.ospeed*4.50
				elif event.key == K_LEFT:
					self.eq.move_left()
				elif event.key == K_RIGHT:
					self.eq.move_right()
			elif event.type == KEYUP:
				if event.key == K_DOWN:
					self.speed = self.ospeed
		else:
			if(event.type == KEYDOWN):
				if event.key == K_UP:
					if self.eq.tet.direction == NORTH:
						self.speed = self.ospeed*4.50
					elif self.eq.tet.direction == SOUTH:
						self.eq.board.rotate_tetrimo_L()
					elif self.eq.tet.direction == WEST:
						self.eq.move_left()
					else:
						self.eq.move_right()
				elif event.key == K_DOWN:
					if self.eq.tet.direction == NORTH:
						self.eq.board.rotate_tetrimo_L()
					elif self.eq.tet.direction == SOUTH:
						self.speed = self.ospeed*4.50
					elif self.eq.tet.direction == WEST:
						self.eq.move_right()
					else:
						self.eq.move_left()
				elif event.key == K_LEFT:
					if self.eq.tet.direction == NORTH:
						self.eq.move_right()
					elif self.eq.tet.direction == SOUTH:
						self.eq.move_left()
					elif self.eq.tet.direction == WEST:
						self.speed = self.ospeed*4.50
					else:
						self.eq.board.rotate_tetrimo_L()
				elif event.key == K_RIGHT:
					if self.eq.tet.direction == NORTH:
						self.eq.move_left()
					elif self.eq.tet.direction == SOUTH:
						self.eq.move_right()
					elif self.eq.tet.direction == WEST:
						self.eq.board.rotate_tetrimo_L()
					else:
						self.speed = self.ospeed*4.50
			elif event.type == KEYUP:
				if event.key == K_UP and self.eq.tet.direction == NORTH:
					self.speed = self.ospeed
				elif event.key == K_DOWN and self.eq.tet.direction == SOUTH:
					self.speed = self.ospeed
				elif event.key == K_LEFT and self.eq.tet.direction == WEST:
					self.speed = self.ospeed
				elif event.key == K_RIGHT and self.eq.tet.direction == EAST:
					self.speed = self.ospeed
		if event.type == KEYDOWN:
			if event.key == K_p or event.key == K_ESCAPE:
				self.pause()
				self.speed = self.ospeed
			elif event.key == K_LSHIFT:
				self.eq.shift()
				self.speed = self.ospeed
			elif event.key == K_SPACE:
				self.board.drop()
				self.speed = self.ospeed
			elif event.key == K_z:
				self.eq.board.rotate_tetrimo_L()
			elif event.key == K_x:
				self.eq.board.rotate_tetrimo_R()

	def gameover(self):
		img = load_image("gameover.png")
		rect = img.get_rect()
		self.screen.blit(img, (0, 0))
		pygame.display.update()
		sleep(3)
