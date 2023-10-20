import pygame
from win32api import GetSystemMetrics
import time
from particle import Particle
from particle import meter

clock = pygame.time.Clock()
pygame.init()

WINDOW_SIZE = ((GetSystemMetrics(0)//32)*32, (GetSystemMetrics(1)//32)*28)
FRAMERATE = 60

font = pygame.font.SysFont("calibri",32)
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)

# location func = (-16(t)(t))+([start_velocity](t))+[starty]
# velocity func = (-32(t))+[start_velocity]
# acceleration func = -32


particle1 = Particle((255,0,0), WINDOW_SIZE[0]//2 - 2*meter, WINDOW_SIZE[1]-(9.8*meter), meter/4, meter/4)
particle1.set_settings(FRAMERATE, WINDOW_SIZE, font, screen)
# color: red
# starting x: half of window width minus 2 meters
# startin y: 10 meters
# width: 0.25 meters
# height: 0.25 meters
particle2 = Particle((0,0,255), WINDOW_SIZE[0]//2 + 2*meter, WINDOW_SIZE[1]-(9.8*meter), meter/4, meter/4)
particle2.set_settings(FRAMERATE, WINDOW_SIZE, font, screen)
# color: blue
# starting x: half of window width plus 2 meters
# startin y: 10 meters
# width: 0.25 meters
# height: 0.25 meters
particle1.mass = 1
particle2.mass = 1


running = True
begin_move = False
timer_state = False
force = 0

last_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                begin_move = True
                timer_state = True
                particle1.reset(dt, force)
                particle2.reset(dt, force)

    dt = time.time() - last_time
    dt *= 23 # physics will act as though the program is running at this framerate if you removed dt from calculations
    last_time = time.time()

    screen.fill((0,0,0))
    # draw_grid()
    if begin_move == True:
        particle1.move(dt, force)
        particle2.move(dt, force)
    # time since start of graph
    particle1.blit_time(timer_state, (2*meter, 2*meter))
    particle2.blit_time(timer_state, (WINDOW_SIZE[0]-10*meter, 2*meter))
    # f gravity
    particle1.blit_info(f'F gravity: {particle1.gravity/meter} m/s^2', (2*meter, 4*meter))
    particle2.blit_info(f'F gravity: {particle2.gravity/meter} m/s^2', (WINDOW_SIZE[0]-10*meter, 4*meter))
    # f accel
    particle1.blit_info(f'F acceleration: {particle1.accel}', (2*meter, 6*meter))
    screen.blit(font.render(str(FRAMERATE) + ' fps', True, (255,255,255)), (WINDOW_SIZE[0]//2, 2*meter))

    pygame.draw.rect(screen, particle1.color, particle1.rect)
    pygame.draw.rect(screen, particle2.color, particle2.rect)

    pygame.display.flip()

    clock.tick(FRAMERATE)

pygame.quit()