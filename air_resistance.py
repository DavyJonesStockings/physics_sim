import pygame
from win32api import GetSystemMetrics
import time
from pygame import math
from particle import Particle
clock = pygame.time.Clock()

pygame.init()

meter = 32 # 1 meter is 32 pixels
WINDOW_SIZE = (1024, 512)
FRAMERATE = 60

font = pygame.font.SysFont("calibri",32)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

particle = Particle((255,0,0), WINDOW_SIZE[0]//2 + 2*meter, WINDOW_SIZE[1]-(9.8*meter), meter/4, meter/4)

# use traits to find other attributes
vector = pygame.Vector2(2,4)
print(vector)