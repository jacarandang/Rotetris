import pygame
from pygame.locals import *

from time import time
from os import path

from random import *

from sprites import Button
# from sample import *
#TEST
test = False
#TEST

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert_alpha()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

pygame.init()
SCR = pygame.display.set_mode((800, 600))
BG =  load_image("title.png")
#main animation
arrow = load_image("arrow.png")
arrowd = arrow.copy()
arrow_rect = arrow.get_rect()
arrow_rect.center = 209, 150
arrow_timer = time()
arrow_ang = 0
#animation

def testf(*args):
	print "print click"

start = load_image('Start.png')
startb = Button(start, (400, 300), testf)

option = load_image("Options.png")
optionb = Button(option, (400, 375), testf)

exit = load_image("Exit.png")
exitb = Button(exit, (400, 450), testf)

baseoptions = pygame.sprite.Group()
baseoptions.add(startb, optionb, exitb)

allsprites = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True

while(running):
	clock.tick(60)

	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	if(time() - arrow_timer > 1 and not test):
		arrow_ang += choice([90, 180, 270])
		arrow_ang %= 360
		arrowd = pygame.transform.rotate(arrow, arrow_ang)	
		arrow_rect = arrowd.get_rect()
		arrow_rect.center = 209, 150
		arrow_timer = time()
	elif(test):
		arrow_ang -= 1
		arrow_ang %= 360
		arrowd = pygame.transform.rotate(arrow, arrow_ang)	
		arrow_rect = arrowd.get_rect()
		arrow_rect.center = 209, 150
		arrow_timer = time()

	SCR.blit(BG, (0, 0))
	SCR.blit(arrowd, arrow_rect)

	allsprites.update()
	baseoptions.update()
	allsprites.draw(SCR)

	baseoptions.draw(SCR)
	pygame.display.update()
	