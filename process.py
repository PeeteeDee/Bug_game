import pygame, os, sys, classes, random
from pygame.locals import *
pygame.init()

def process(bug,FPS,total_frames):
  #PROCESSING
  for event in pygame.event.get():
    if event.type==QUIT:
      pygame.quit()
      print "\nBye"
      sys.exit(0)
    if event.type==KEYDOWN:
      if event.key==pygame.K_e:
        classes.BugProjectile.fire = not classes.BugProjectile.fire

  keys=pygame.key.get_pressed()
  #move bug with a/d
  
  #horizontal movement
  if keys[pygame.K_d]:
    classes.Bug.going_right=True
    bug.image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", "bug.png")).convert_alpha()
    bug.velx=5
  elif keys[pygame.K_a]:
    classes.Bug.going_right=False
    bug.image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", "bugflipped.png")).convert_alpha()
    bug.velx= -5

  else:
    bug.velx=0

  #vertical movement
  if keys[pygame.K_w]:
    bug.jumping=True

  if keys[pygame.K_SPACE]:
    #p=projectile
    def direction():
      if classes.Bug.going_right:
        p.velx=8
      else:
        p.image=pygame.transform.flip(p.image, True, False)
        p.velx= -8
    if (classes.BugProjectile.fire):    
      p=classes.BugProjectile(bug.rect.x, bug.rect.y, True, "fire.png")
      direction()
    else:
      p=classes.BugProjectile(bug.rect.x, bug.rect.y, False, "frost.png")
      direction()





  spawn(FPS,total_frames)
  collisions()

  #PROCESSING

def spawn(FPS,total_frames):
  four_seconds=FPS*4
  if total_frames % four_seconds==0:
    
    #50/50 chance of spawning left/right
    r=random.randint(1,2)
    x=1
    if r==2:
      x=640-40

    classes.Fly(r*100,130,"fly.png")

def collisions():  
  for fly in classes.Fly.List:
    projectiles=pygame.sprite.spritecollide(fly,classes.BugProjectile.List, True)

    for projectile in projectiles:
      #THE FLY IS DEAD
      fly.velx=0
      fly.health=0
      if projectile.if_this_variable_is_true_then_fire:
        fly.image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", "burnt_fly.png")).convert_alpha()

      else:
        if fly.velx>0:
          fly.image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", "frozen_fly.png")).convert_alpha()
        else:
          fly.image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", "frozen_fly.png")).convert_alpha()
          fly.image=pygame.transform.flip(fly.image, True, False)
      
      projectile.rect.x=2* -projectile.rect.width
      projectile.destroy()


  ##pygame.sprite.groupcollide(group1,group2, kill1,kill2)
  ##pygame.sprite.spritecollide(obj,G1,dokill)      use this one