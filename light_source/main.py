'''main file. felt cute, might delete later.'''

from math import sqrt
# import time
from functools import wraps
from win32api import GetSystemMetrics
from pygame.locals import K_w,K_a,K_s,K_d
import pygame
from gradients import draw_circle

clock = pygame.time.Clock()
pygame.init()

WIDTH = (GetSystemMetrics(0)//32)*28
HEIGHT = (GetSystemMetrics(1)//32)*28
FRAMERATE = 60
SPEED = 4 # m/s^2
# FRIC = -0.1

vec = pygame.math.Vector2
font = pygame.font.SysFont("calibri",32)
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


METER = 32

def is_odd(num:int):
    '''returns whether or not the int is an odd number'''
    if num % 2 != 0:
        return True
    return False
def toggle_bool(boolean:bool):
    '''toggles inputted boolean. True -> False, False -> True'''
    if boolean is False:
        return True
    return False


def dist_to_px(px1:tuple, px2:tuple):
    '''returns distance between two points passed in as parameters'''
    # |x2-x1|^2 + |y2-y1|^2 = distance to center point
    # if (x2,y2) is a point in area of light source
    # using distance formula to
    dist = sqrt( abs( px2[0]-px1[0] )**2 +  abs( px2[1]-px1[1] )**2 )
    return dist
def mod_pixel(px:list, mod:tuple):
    '''modifies inputting pixel at pos (x,y) by specified amount mod (r,g,b)'''
    # adds mod value to pixel. if modded value exceeds 255, value is set to 255.
    px[0] = min(255, px[0]+mod[0]) # red
    px[1] = min(255, px[1]+mod[1]) # green
    px[2] = min(255, px[2]+mod[2]) # blue
    return tuple(px)

def memoize(func):
    '''memoization decorator to optimize functions.
    function must return a value for memoization to work.'''
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper


class Light(pygame.sprite.Sprite):
    '''class of a light emitting object within the program. 
    can be made with differing levels of luminosity, and different sizes.'''
    def __init__(self, luminosity:int, dimensions:tuple) -> None:
        super().__init__()
        self.rect = pygame.Rect((WIDTH, HEIGHT), (dimensions[0], dimensions[1]))
        self.font = pygame.font.SysFont("calibri",32)

        self.luminosity = luminosity
        self.active = False
        self.color = (255,255,255)

        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        # self.acc = vec(0,0)

        self.vel = vec(0,0)

    def blit_info(self, info, blit_pos):
        '''blits any inputted value at any given position'''
        t = self.font.render(str(info), True, (255,255,255))
        screen.blit(t, blit_pos)

    def move(self):
        '''does movement operation for light src'''

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_w]:
            self.vel.y = -SPEED
        elif pressed_keys[K_s]:
            self.vel.y = SPEED
        else:
            self.vel.y = 0

        if pressed_keys[K_a]:
            self.vel.x = -SPEED
        elif pressed_keys[K_d]:
            self.vel.x = SPEED
        else:
            self.vel.x = 0


        if self.vel.x!=0 or self.vel.y!=0:
            self.vel.scale_to_length(SPEED)

        self.pos += self.vel

        if self.pos.x > WIDTH + self.rect.width: # Right wall detection
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width: # Left wall detection
            self.pos.x = WIDTH + self.rect.width/2
        if self.pos.y > HEIGHT + self.rect.height: # Bottom wall detection
            self.pos.y = 0 - self.rect.height/2
        if self.pos.y < 0 - self.rect.height: # Top wall detection
            self.pos.y = HEIGHT + self.rect.height/2

        self.rect.midbottom = self.pos

    @memoize
    def illuminate_area(self) -> pygame.Surface:
        '''add illumination (brightness) to surrounding squares based off of light level.
        calulates a value 0 to 1 for each pixel in area using luminosity/distance to pixel'''

        surf = pygame.Surface((
            3*self.luminosity*METER,
            3*self.luminosity*METER
        ))
        draw_circle(
            surf,
            (surf.get_width()/2, surf.get_height()/2),
            (surf.get_width()/2+self.luminosity*METER,
                surf.get_height()/2+self.luminosity*METER),
            (255,255,210,255),
            (255,255,150,0),
            Afunc= lambda x : x**(2/3)
        )

        return surf

class Object(pygame.sprite.Sprite): # object to be illuminated - in future
    '''object created for purpose of having color that is increased with light'''
    def __init__(self, dimensions:tuple) -> None:
        super().__init__()
        self.rect = pygame.Rect((WIDTH, HEIGHT), (dimensions[0], dimensions[1]))
        self.font = pygame.font.SysFont("calibri",32)

        self.color = (255,0,0)

        self.pos = vec(2*METER, 2*METER)

    def update(self):
        pass


bulb = Light(8, (1*METER,1*METER))
obj = Object((3*METER,3*METER))
print(mod_pixel([255,255,200], (50,50,50)))


# last_time = time.time()
RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bulb.active = toggle_bool(bulb.active)
            if event.key == pygame.K_j:
                bulb.luminosity += 1
            if event.key == pygame.K_k:
                bulb.luminosity -= 1

    # dt = time.time() - last_time
    # dt *= 23
    # last_time = time.time()

    screen.fill((0,0,0))

    if bulb.active:
        circle = bulb.illuminate_area()
        # print(circle)
        screen.blit(
            circle, (
                bulb.rect.centerx - circle.get_width()/2,
                bulb.rect.centery - circle.get_height()/2
            )
        )
    bulb.move()

    pygame.draw.rect(screen, bulb.color, bulb.rect)

    pygame.display.flip()
    pygame.display.update()

    clock.tick(FRAMERATE)

pygame.quit()
