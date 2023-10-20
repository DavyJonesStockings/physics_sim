import pygame
import time


meter = 32 # 1 meter is 32 pixels


class Particle(pygame.sprite.Sprite):
    def __init__(self, color:str, x:int, y:int, width:int, height:int) -> None:
        super().__init__()
        self.color = color
        self.location = [x,y]
        self.rect = pygame.Rect(self.location[0],self.location[1], width, height)

        # 1 newton (N) is 1 kg(m/s^2). essentially, 1 N is the force required to
        # cause 1 kg to accelerate at a rate of 1 m/s^2.
        # if an object weighing 2 kg has an acceleration of 4 m/s^2, that means that
        # the object was propelled by 8 newtons of force.

        # kg * m/s^2 = N
        # thus, acceleration can be solved for given the mass of an object and force applied.
        # m/s^2 = N/kg
        # length/time^2 = force/mass

        self.mass = 20 # in kg
        self.force_counter = 0
        self.gravity = 9.8*meter
        self.vel = 0
        self.start_time = time.time()
    
    def set_settings(self, FRAMERATE, WINDOW_SIZE, font, screen):
        
        self.FRAMERATE = FRAMERATE
        self.WINDOW_SIZE = WINDOW_SIZE
        self.font = font
        self.screen = screen

    def move(self, dt, force): # returns a list [x,y]

        # changing x position based on TIME
        # y changes with respect to time (t), x changes with time (t)

        # t = time.time() - self.start_time # time in seconds since start of move
        # x = t*(meter*4) # every second translates to 4 grid squares
        # if t > 6:
        #     x = 6*(meter*4) 
        # self.location[0] = x
        # self.location[0] = self.WINDOW_SIZE[0]//2

        # ENERGY LOSS
        self.vel = self.apply_gravity(dt, self.vel)
        # GROUND DETECTION
        self.location[1] = self.location[1] + self.vel * dt # update location
        self.bounce()

        # LOCATION UPDATE
        self.rect.bottomleft = self.location # set rect to calculated location

    def apply_force(self, dt, force):
        # calculate acceleration
        self.accel = (force/self.mass) * dt # force(kg*m/s^2) / mass(kg) = acceleration(m/s^2)
        # apply acceleration to velocity
        self.vel -= self.accel * dt
        self.force_counter += 1

    def apply_gravity(self, dt, velocity):
        # using framerate to calculate gravity from initial value
        # self.gravity = 9.8 meters/frame during initialization
        # if gravity should 9.8 meters per second (32*9.8 pixels), how many
        # pixels should the ball be moved per frame?
        grav = self.gravity/self.FRAMERATE
        velocity += grav * dt
        return velocity
    
    def bounce(self):

        if self.location[1] > self.WINDOW_SIZE[1]:
            self.location[1] = self.WINDOW_SIZE[1]
            self.vel = -self.vel

        if self.location[0] + self.rect.width > self.WINDOW_SIZE[0]:
            self.location[0] = self.WINDOW_SIZE[0] - self.rect.width

        # TO DO - create functions for separate losses of energy upon impact
        # sound, friction, air resistance, gravity

    def blit_time(self, timer, blit_pos):
        if timer == True:
            t = self.font.render(str(time.time() - self.start_time), True, (255,255,255))
        else: 
            t = self.font.render("0.000", True, (255,255,255))
        self.screen.blit(t, blit_pos)
    
    def blit_info(self, info, blit_pos):
        t = self.font.render(str(info), True, (255,255,255))
        self.screen.blit(t, blit_pos)

    def reset(self, dt, force):
        self.location[1] = self.WINDOW_SIZE[1]-(9.8*meter)
        self.vel = 0 
        self.start_time = time.time()
        self.apply_force(dt, force)

    def draw_grid(self):
        for x in range(0, self.WINDOW_SIZE[0], meter):
            for y in range(0, self.WINDOW_SIZE[1], meter):
                rect = pygame.Rect(x, y, meter, meter)
                pygame.draw.rect(self.screen, (255,255,255), rect, 1)
