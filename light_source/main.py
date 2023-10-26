'''main file. felt cute, might delete later.'''

from math import sqrt
# import time
from win32api import GetSystemMetrics
from pygame.locals import K_w,K_a,K_s,K_d
import pygame

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


class Light(pygame.sprite.Sprite):
    '''class of a light emitting object within the program. 
    can be made with differing levels of luminosity, and different sizes.'''
    def __init__(self, luminosity:int, dimensions:tuple) -> None:
        super().__init__()
        self.rect = pygame.Rect((WIDTH, HEIGHT), (dimensions[0], dimensions[1]))

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
        self.screen.blit(t, blit_pos)

    def move(self):
        '''does movement operation for light src'''
        # self.acc = vec(0,0)

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

    def illuminate_area(self):
        '''add illumination (brightness) to surrounding squares based off of light level.
        calulates a value 0 to 1 for each pixel in area using luminosity/distance to pixel'''
        # add illumination (brightness) to surrounding squares based off of light level
        # math for adding light level: light level is a floating point number between 0 and 1.
        # light level will be luminosity/distToPx


        for i in range(self.luminosity):
            surf = pygame.Surface((
                2*self.rect.width*(i+1) + METER,
                2*self.rect.height*(i+1) + METER
            ))
            pygame.draw.circle(
                surf,
                (255,255,200),
                # mod_pixel(),
                (surf.get_width()/2, surf.get_height()/2),
                surf.get_width()/2
            )

            surf.set_alpha(255/(i+1))

            screen.blit(surf, (
                self.rect.center[0]-surf.get_width()/2, self.rect.center[1]-surf.get_height()/2
            ))

        # NOTE: WORKS, SET ASIDE FOR OTHER TESTING
        # for i in range(self.luminosity):
        #     surf = pygame.Surface((
        #         1*self.rect.width + (i+1)*METER, 1*self.rect.height + (i+1)*METER
        #     ))
        #     surf.set_alpha(255/(i+1))
        #     surf.fill((255,255,220))
        #     screen.blit(surf, (
        #         self.rect.center[0]-surf.get_width()/2, self.rect.center[1]-surf.get_height()/2
        #     ))

class Object(): # object to be illuminated - in future
    '''object created for purpose of having color that is increased with light'''
    def __init__(self, location:tuple, dimensions:tuple) -> None:
        pass


bulb = Light(3, (1*METER,1*METER))
print(mod_pixel([255,255,200], (50,50,50)))

RUNNING = True
while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bulb.active = toggle_bool(bulb.active)

    screen.fill((0,0,0))

    if bulb.active:
        bulb.illuminate_area()
    bulb.move()
    # bulb.blit_info(FRAMERATE)

    pygame.draw.rect(screen, bulb.color, bulb.rect)

    pygame.display.flip()
    pygame.display.update()

    clock.tick(FRAMERATE)

pygame.quit()
