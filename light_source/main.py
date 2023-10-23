import pygame
from win32api import GetSystemMetrics
import time
import math
from math import sqrt

clock = pygame.time.Clock()
pygame.init()

WINDOW_SIZE = ((GetSystemMetrics(0)//32)*32, (GetSystemMetrics(1)//32)*28)
FRAMERATE = 60

font = pygame.font.SysFont("calibri",32)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)


meter = 32

def isOdd(num):
    if num % 2 != 0:
        return True
    else:
        return False

def distToPx(px1:tuple, px2:tuple):
    # |x2-x1|^2 + |y2-y1|^2 = distance to center point
    # if (x2,y2) is a point in area of light source
    # using distance formula to
    dist = sqrt( abs( px2[0]-px1[0] )**2 +  abs( px2[1]-px1[1] )**2 )
    return dist

class Light():
    def __init__(self, luminosity, x, y) -> None:
        self.luminosity = luminosity
        self.location = (x,y)

    def illuminate_area(self):
        # add illumination (brightness) to surrounding squares based off of light level
        # math for adding light level: light level is an integer. light level will be
        # luminosity/distToPx
        light_area = (self.luminosity*meter,self.luminosity*meter)
        for x in light_area[0]:
            for y in light_area[1]:
                light_level = distToPx(self.location, (x,y))/self.luminosity
                screen.get_at

class Object():
    pass


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

pygame.quit()