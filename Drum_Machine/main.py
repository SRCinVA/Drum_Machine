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
boxes = []
clicked = [[-1]]  # creating a full list of negative 1s, to record what has been clicked (what the ...)

def draw_grid():
    left_box = pygame.draw.rect(screen, gray, [0, 0, 210, HEIGHT - 200], 5)   # x and y starting coordinates, width, and height
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
    
    crash_text = label_font.render('Crash', True, white, )
    screen.blit(crash_text, (30, 330))

    clap_text = label_font.render('Clap', True, white, )
    screen.blit(clap_text, (30, 430))

    floor_tom_text = label_font.render('Floor Tom', True, white, )
    screen.blit(floor_tom_text, (30, 530))

    # to draw lines between items:
    for i in range(instruments): # remember that you just need the 'stop' here
        pygame.draw.line(screen, gray, (0, (i * 100) + 100), (250,(i * 100) + 100), 5)     # basically, each line would build 100 way from the previous
                                                                # because there is a zero index, you need to gvie it a "boost" of 100 from the starting position
                                                                # (200) is the width of each line
                                                                # for the overall width of the bar is 250
                                                                # the width of the line is 5

    for i in range(beats):
        for j in range (instruments):  # when fully expressed, this will give us our complete grid.
            rect = pygame.draw.rect(screen, gray, [i * ((WIDTH - 200)// beats) + 205, (j * 100), ((WIDTH - 200)//beats), ((HEIGHT - 200)//instruments)], 5, 5)  # '+ 205' is its staritng point
                                                    # it's 'i' because it's populating one column at a time and will shift over one whole step. Unclear why it's 200, though.
                                                    # up to 205, is just the x starting position
                                                    # still don't understand the WIDTH - 200 element.
            boxes.append((rect, (i, j)))  # we're getting the coordinates but then also need to return the entire box for collision detection elsewhere.

    return boxes # ... here's where we actually make that return (mentioned above).



# the main game loop
run = True
while run:
    timer.tick(fps) # this means we execute the code 60 times per second
    screen.fill(black) # the background
    boxes = draw_grid()  # this is how we make 'boxes' available.

    # "event handling":
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # this obviously shuts down the app.
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # don't understand this one.
            for i in range(len(boxes)):  # every time we update the beats, the whole thing has to be scalable and thus checkable.
                if boxes[i][0].colliderect(event.pos):  # the '0' referecnes the rectangle we stored in the box, where I represents the tuple.
                    coords = boxes[i][1]
                                # we can use this Pygame function to see if the mouse collided with a rectangle (huh ...?!?)
                                # it does this by determining where our mouse was when we clicked.
                                # didn't understand his explanation on coords, other than it's a temporary variable that tracks if something has been clicked.
                    clicked[coords[i]][coords[0]]
    pygame.display.flip()

pygame.quit() # this is to catch it if everything else doesn't work (it seems)
