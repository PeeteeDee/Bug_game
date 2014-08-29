import pygame, os, math
from random import randint

class BaseClass(pygame.sprite.Sprite):

  allSprites=pygame.sprite.Group()
  def __init__(self, x, y, image_string):
    
    pygame.sprite.Sprite.__init__(self)
    BaseClass.allSprites.add(self)

    self.image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", image_string)).convert_alpha()
    
    self.rect=self.image.get_rect()
    self.rect.x=x
    self.rect.y=y
    
    #movement variables
    
    self.jumping, self.go_down= False,False

  def destroy(self, ClassName):

    #sends in class name, takes class.List and removes target
    ClassName.List.remove(self)#stops collison detection for fly
    BaseClass.allSprites.remove(self)#stops game from rendering a fly
    del self

class Bug(BaseClass):
  List=pygame.sprite.Group()
  going_right=True
  def __init__(self, x, y, image_string):
    
    BaseClass.__init__(self, x,y, image_string)
    Bug.List.add(self)
    self.velx, self.vely=3,5

  def motion(self, SCREENWIDTH, SCREENHEIGHT):
    #CALLS __jump() AT END

    #checks for bug being in valid area
    #horizontal
    predicted_location=self.rect.x+self.velx
    if predicted_location <0:
      self.velx=0
    elif predicted_location+self.rect.width>SCREENWIDTH:
      self.velx=0

    self.rect.x+=self.velx
    
    self.__jump(SCREENHEIGHT)

  def __jump(self, SCREENHEIGHT):
    max_jump=75

    if self.jumping:
      #determines jumping
      if self.rect.y<max_jump:
        self.go_down=True
      #moves bug verticaly
      if self.go_down:
        self.rect.y+=self.vely
        #checks if move is valid
        predicted_location=self.rect.y+self.vely
        if predicted_location+self.rect.height>SCREENHEIGHT:
          self.jumping=False
          self.go_down=False

      else:
        self.rect.y-=self.vely

class Fly(BaseClass):
  List=pygame.sprite.Group()
  def __init__(self, x, y, image_string):
    BaseClass.__init__(self, x, y, image_string)
    Fly.List.add(self)
    self.health=100
    self.half_health=self.health/2.0
    self.velx=randint(1,4)
    self.vely=2
    self.amplitude, self.period=randint(20,140), randint(4,5)/100.0

  @staticmethod
  def update_all(width,height):

    for fly in Fly.List:
      
      #drops fly to ground "kills fly"
      if fly.health<=0:
        if fly.rect.y+fly.rect.height<height:
          fly.rect.y+=fly.vely

      else:
        fly.fly(width)#keeps fly going


  def fly(self, SCREENWIDTH):

    if self.rect.x+self.rect.width>SCREENWIDTH or self.rect.x<0:
      #image, flip on x_axis,  flip on y_axis
      self.image=pygame.transform.flip(self.image, True,False)
      self.velx=-self.velx

    self.rect.x+=self.velx


    # a * sin(bx+c)+y
    self.rect.y=self.amplitude*math.sin(self.period*self.rect.x)+140
    #a=max_height, b=period, x=x_pos, c=shift, y=y_pos
  
  #@staticmethod
  #def movement(width):
  #  for fly in Fly.List:
  #    fly.fly(width)

class BugProjectile(pygame.sprite.Sprite):
  
  List=pygame.sprite.Group()
  normal_list=[]
  fire = True

  def __init__(self, x, y, if_this_variable_is_true_then_fire, image_string):

    pygame.sprite.Sprite.__init__(self)
    self.image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)),"src", image_string)).convert_alpha()

    self.rect=self.image.get_rect()
    self.rect.x=x
    self.rect.y=y
    self.if_this_variable_is_true_then_fire=if_this_variable_is_true_then_fire

    try:
      #self means the current bug
      last_element=BugProjectile.normal_list[-1]
      difference=abs(self.rect.x-last_element.rect.x)

      #wait for projectile to be this far away
      distance_to_wait=0
      if difference<self.rect.width+distance_to_wait:
        return

    except Exception:
      pass


    BugProjectile.normal_list.append(self)
    BugProjectile.List.add(self)
    self.velx=None

  @staticmethod
  def movement():
    for projectile in BugProjectile.List:
      projectile.rect.x+=projectile.velx

  def destroy(self):
    BugProjectile.List.remove(self)
    BugProjectile.normal_list.remove(self)
    del self