import pygame
from pygame.locals import *

from time import time
from os import path

from random import *
from sprites import Button

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert_alpha()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

pygame.init()
pygame.display.set_caption("Rotetris")
SCR = pygame.display.set_mode((800, 600))
pygame.font.init()
pygame.key.set_repeat(100, 70)

BG =  load_image("title.png")
#main animation
arrow = load_image("arrow.png")
arrowd = arrow.copy()
arrow_rect = arrow.get_rect()
arrow_rect.center = 209, 150
arrow_timer = time()
arrow_ang = 0
#animation
BGM = pygame.mixer.Sound(path.join('resource', 'music', 'track1.ogg'))
BGM.play(-1)


class MainObjects():

	def __init__(self, default):
		self.group = default
		self.running = True

	def set(self, group):
		self.group = group

	def get(self):
		return self.group

	def stop(self):
		self.running = False

baseoptions = pygame.sprite.Group()
startoptions = pygame.sprite.Group()
creditsoptions = pygame.sprite.Group()
mainobject = MainObjects(baseoptions)

clock = pygame.time.Clock()

#Main Menu
start = load_image('Start.png')
startb = Button(start, (400, 275), lambda: mainobject.set(startoptions))

option = load_image("Options.png")
optionb = Button(option, (400, 350), None)

credit = load_image("Credits.png")
creditb = Button(credit, (400, 425), lambda: mainobject.set(creditsoptions))

exit = load_image("Exit.png")
exitb = Button(exit, (400, 500), lambda: mainobject.stop())

baseoptions.add(startb, optionb, creditb, exitb)
#-------------------------------------
#start menu
easy = load_image("Easy.png")
easyb = Button(easy, (400, 275), None)

normal = load_image("Normal.png")
normalb = Button(normal, (400, 350), None)

hard = load_image("Hard.png")
hardb = Button(hard, (400, 425), None)

insane = load_image("Insane.png")
insaneb = Button(insane, (400, 500), None)

back = load_image("Back.png")
backb = Button(back, (100, 565), lambda: mainobject.set(baseoptions))

startoptions.add(easyb, normalb, hardb, insaneb, backb)
#-------------------------------------
#credits
class _CreditsPg(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("Creditspg.png")
		self.rect = self.image.get_rect()
creditspg = _CreditsPg()

creditsoptions.add(creditspg)
#---------------------------------------

allsprites = pygame.sprite.Group()

while(mainobject.running):
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == QUIT:
			mainobject.stop()
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				mainobject.set(baseoptions)
		elif event.type == MOUSEBUTTONDOWN:
			if event.button == 1:
				for sp in mainobject.get():
					if isinstance(sp, Button):
						sp.click()
						print "Click"

	if(time() - arrow_timer > 1):
		arrow_ang += choice([90, 180, 270])
		arrow_ang %= 360
		arrowd = pygame.transform.rotate(arrow, arrow_ang)	
		arrow_rect = arrowd.get_rect()
		arrow_rect.center = 209, 150
		arrow_timer = time()

	SCR.blit(BG, (0, 0))
	SCR.blit(arrowd, arrow_rect)

	allsprites.update()
	mainobject.get().update()

	allsprites.draw(SCR)
	mainobject.get().draw(SCR)
	pygame.display.update()
	
BGM.stop()
pygame.quit()