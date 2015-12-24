import pygame, sys, time
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hello World!')

pygame.mixer.music.load('silver_will.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1, 0.0)

soundObj = pygame.mixer.Sound('Combatknife_slash.ogg')

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONDOWN:
			soundObj.play()
	pygame.display.update()