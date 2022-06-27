import pygame
from pygame import mixer

pygame.init()

# think of this as your variable library

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)

fps = 60 # frames per second
timer = pygame.time.Clock() # for a music application, this is clearly critical

def draw_grid():
    left_box = pygame.draw.rect(screen, gray, [0, 0, 0, HEIGHT]) # starting coordinates, width, and height

# the main game loop
run = True
while run:
    timer.tick(fps) # this means we execute the code 60 times per second
    screen.fill(black) # the background
    draw_grid()


    # "event handling":
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # this obviously shuts down the app.
            run = False

    pygame.display.flip()
pygame.quit() # this is to catch it if everything else doesn't work (it seems)
