import pygame
from pygame.locals import *
from win32api import GetSystemMetrics
import time
import math
from math import sqrt

clock = pygame.time.Clock()
pygame.init()

WIDTH = (GetSystemMetrics(0)//32)*32
HEIGHT = (GetSystemMetrics(1)//32)*28
FRAMERATE = 60
ACC = .2 # m/s^2
FRIC = -0.1

vec = pygame.math.Vector2
font = pygame.font.SysFont("calibri",32)
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


meter = 32

def isOdd(num):
    if num % 2 != 0:
        return True
    else:
        return False
    
def toggleBool(bool):
    if bool == False:
        return True
    if bool == True:
        return False


def distToPx(px1:tuple, px2:tuple):
    # |x2-x1|^2 + |y2-y1|^2 = distance to center point
    # if (x2,y2) is a point in area of light source
    # using distance formula to
    dist = sqrt( abs( px2[0]-px1[0] )**2 +  abs( px2[1]-px1[1] )**2 )
    return dist


class Light(pygame.sprite.Sprite):
    def __init__(self, luminosity, dimensions:tuple) -> None:
        super().__init__()
        self.luminosity = luminosity
        self.active = False

        self.pos = vec((WIDTH/2, HEIGHT/2))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.rect = pygame.Rect(self.pos.x,self.pos.y, dimensions[0], dimensions[1])
        self.vel = vec(0,0)

    def move(self):
        self.accel = vec(0,0)

        if abs(self.vel.x) > 0.3:
            self.moving = True
        else:
            self.moving = False

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_w]:
            self.accel.y = -ACC
        if pressed_keys[K_a]:
            self.accel.x = -ACC
        if pressed_keys[K_s]:
            self.accel.y = ACC
        if pressed_keys[K_d]:
            self.accel.x = ACC
            self.direction = 'RIGHT'
        if not pressed_keys[K_a] or not pressed_keys[K_d]:
            self.direction = None

        self.acc += self.vel * FRIC
        self.vel += self.accel
        self.pos += self.vel

        if self.pos.x > WIDTH + self.rect.width: # Right wall detection
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width: # Left wall detection
            self.pos.x = WIDTH + self.rect.width/2
        if self.pos.y > HEIGHT + self.rect.height: # Bottom wall detection
            self.pos.y = 0 - self.rect.height/2
        if self.pos.y < 0 - self.rect.height: # Top wall detection
            self.pos.y = HEIGHT + self.rect.height/2

        self.rect.topleft = self.pos
   
    
    def illuminate_area(self):
        # add illumination (brightness) to surrounding squares based off of light level
        # math for adding light level: light level is an integer. light level will be
        # luminosity/distToPx
        light_area = (self.luminosity*meter,self.luminosity*meter)
        for x in light_area[0]:
            for y in light_area[1]:
                light_level = distToPx(self.location, (x,y))/self.luminosity
                screen.get_at

class Object(): # object to be illuminated - in future
    def __init__(self, location:tuple, width) -> None:
        pass


bulb = Light(3, (1*meter,1*meter))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggleBool(bulb.active)
            if event.key == pygame.K_w:
                bulb.vel = 5
    screen.blit(bulb.rect, bulb.pos)
            

pygame.quit()