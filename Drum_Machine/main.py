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
beats = 8  # this is how many note intervals we'll have extending to the right.
instruments = 6  # we'll use this to check how many rows there are.


def draw_grid():
    left_box = pygame.draw.rect(screen, gray, [0, 0, 300, HEIGHT - 200], 5)   # x and y starting coordinates, width, and height
                                                                        # "5" clarifies how wide we want the edges to be.
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 3)
                                                                        # it will start at 200 above the bottom of the screen
                                                                        # pygame grid stops at top left
    boxes = []  # this might be for individual tracks
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, white, )
                # second term above is an anti-alias (smooth borders for lines)
    screen.blit(hi_hat_text, (30, 30))  # draws it on the screen, with the coordinates.
    
    snare_text = label_font.render('Snare', True, white, )
    screen.blit(snare_text, (30, 130))
    
    bass_drum_text = label_font.render('Bass Drum', True, white, )
    screen.blit(bass_drum_text, (30, 230))
    
    crash_cymbal_text = label_font.render('Crash Cymbal', True, white, )
    screen.blit(crash_cymbal_text, (30, 330))

    clap_text = label_font.render('Clap', True, white, )
    screen.blit(clap_text, (30, 430))

    floor_tom_text = label_font.render('Floor Tom', True, white, )
    screen.blit(floor_tom_text, (30, 530))

    # to draw lines between items:
    for i in range(instruments): # remember that you just need the 'stop' here
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (299,(i * 100) + 100), 5)     # basically, each line would build 100 way from the previous
                                                                # because there is a zero index, you need to gvie it a "boost" of 100 from the starting position
                                                                # (200) is the width of each line
                                                                # for the overall width of the bar is 250
                                                                # the width of the line is 5

    for i in range(beats):
        for j in range (instruments):  # when fully expressed, this will give us our complete grid.
            rect = pygame.draw.rect(screen, gray, [i * (WIDTH - 200)// beats])
                                                    # unsure of why it's 'i' and not just instruments 

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
