#!/usr/bin/env python3


import sys

import pygame


pygame.init()

display = pygame.display.set_mode((100,100))

filename = sys.argv[1]

try:
	image = pygame.image.load(filename)
except:
	print("could not find "+filename)
	pygame.quit()
	exit

newtile = pygame.Surface(image.get_size()).convert()

newtile.blit(image.subsurface((0,0,image.get_width()/2,image.get_height()/2)), (16,16))
newtile.blit(image.subsurface((16,0,image.get_width()/2,image.get_height()/2)), (0,16))
newtile.blit(image.subsurface((0,16,image.get_width()/2,image.get_height()/2)), (16,0))
newtile.blit(image.subsurface((16,16,image.get_width()/2,image.get_height()/2)), (0,0))

display.blit(newtile, (8,8))
pygame.display.flip()

pygame.image.save(newtile, "fc_"+filename)

pygame.time.wait(3000)
