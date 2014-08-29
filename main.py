import pygame, sys, os, time
from pygame.locals import *
from classes import *
from process import process
pygame.init()

#https://www.youtube.com/watch?v=4BHQJOVWo20
#Purpongie "python game development tutorial - 18 - frost balls"

width=640
height=360
screen=pygame.display.set_mode([width,height],0,32)

#graphic variables
img_bug=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", "bug.png")).convert_alpha()
background=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", "forest.jpg")).convert_alpha()

#time variables
clock=pygame.time.Clock()
FPS=24
total_frames=0

#game variables
bug=Bug(0,height-40,"bug.png")
fly=Fly(40,100, "fly.png")

# --------- MAIN PROGRAM LOOP ---------

while True:
  #PROCESS
  process(bug, FPS, total_frames)
  #PROCESS

  #LOGIC-movement/methods
  bug.motion(width, height)
  Fly.update_all(width, height)
  BugProjectile.movement()
  total_frames+=1
  #LOGIC
  
  #DRAW
  screen.blit(background, (0,0))
  BaseClass.allSprites.draw(screen)
  BugProjectile.List.draw(screen)
  pygame.display.flip()
  #DRAW

  clock.tick(FPS)