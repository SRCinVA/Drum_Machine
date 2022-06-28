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
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 200], 5)   # x and y starting coordinates, width, and height
                                                                        # "5" clarifies how wide we want the edges to be.
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 5 )
                                                                        # it will start at 200 above the bottom of the screen
                                                                        # pygame grid stops at top left
    boxes = []  # this might be for individual tracks
    colors = [gray, white, gray]

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
