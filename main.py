import pygame
from pygame.locals import *

from time import time
from os import path

def load_image(file, colorkey = None):
	surf = pygame.image.load(path.join('resource', file)).convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = surf.get_at((0,0))
		surf.set_colorkey(colorkey, RLEACCEL)
	return surf

pygame.init()
SCR = pygame.display.set_mode((800, 600))
BG =  load_image("title.png")

arrow = load_image("arrow.png")
arrowd = arrow.copy()
arrow_timer = time()
arrow_ang = 0

clock = pygame.time.Clock()
running = True
while(running):

	for event in pygame.event.get():
		if event.type == QUIT:
			running = False

	if(time() - arrow_timer > 1):
		arrow_ang += 90
		arrow_ang %= 360
		arrowd = pygame.transform.rotate(arrow, arrow_ang)
		arrow_timer = time()

	SCR.blit(BG, (0, 0))
	SCR.blit(arrowd, (175, 107))
	pygame.display.update()

	