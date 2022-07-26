from cProfile import label
import pygame
from pygame import mixer

pygame.init()

# think of this as your variable library

WIDTH = 1400
HEIGHT = 800

black = (0, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 32)
medium_font = pygame.font.Font('freesansbold.ttf', 24)

fps = 60 # frames per second
timer = pygame.time.Clock() # for a music application, this is clearly critical
beats = 8  # this is how many note intervals we'll have extending to the right.
instruments = 6  # we'll use this to check how many rows there are.
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]  # iterating over the beats to create a full list of negative 1s, to record what has already been clicked
                                        # in this case, you don't need to name a variable upfront (what the ...)
                                        # hard to follow his reasoning on this set of steps ... 
bpm = 240
playing = True
active_length = 0  # not understanding this one at the moment ...
active_beat = 0
beat_changed = True # still not clear on this one. You would want this to be active as soon as the app loads.


# load in sounds (will make .WAV files later)
hi_hat = mixer.Sound('hi_hat.WAV')
snare  = mixer.Sound('snare.WAV')
kick   = mixer.Sound('kick.WAV')
crash  = mixer.Sound('crash.WAV')
clap   = mixer.Sound('clap.WAV')
tom    = mixer.Sound('tom.WAV')  # note that this required a double backslash
pygame.mixer.set_num_channels(instruments * 3)  # apparently, this helps with sounds that extend beyond one frame (I think)
                                                # this increases the number of channels
def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:  # you'll check where the active beat is at each row [i], but what he mans by '1' is unclear.
            if i == 0:
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2:
                kick.play()
            if i == 3:
                crash.play()
            if i == 4:
                clap.play()
            if i == 5:
                tom.play()


def draw_grid(clicks, beat):
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
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green  # meaning, it's active (hopefully explained later).

            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200)// beats) + 205, (j * 100) + 5, ((WIDTH - 200)//beats) - 10, ((HEIGHT - 200)//instruments) - 10], 0, 5)  # '+ 205' is its staritng point
                                                    # it's 'i' because it's populating one column at a time and will shift over one whole step. Unclear why it's 200, though.
                                                    # up to 205, is just the x starting position
                                                    # still don't understand the WIDTH - 200 element.
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200)// beats) + 200, (j * 100), ((WIDTH - 200)//beats), ((HEIGHT - 200)//instruments)], 5, 5)  # '+ 205' is its staritng point
            
            # it seems that this is the staritng condition for the boxes
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200)// beats) + 200, (j * 100), ((WIDTH - 200)//beats), ((HEIGHT - 200)//instruments)], 2, 5)  # '+ 205' is its staritng point
            
            boxes.append((rect, (i, j)))  # we're getting the coordinates but then also need to return the entire box for collision detection elsewhere.

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200)//beats) + 200, 0, ((WIDTH - 200)//beats), instruments * 100], 5, 3)  # this will show what beat we're currenlty on (a good idea)

    return boxes # ... here's where we actually make that return (mentioned above).

# the main game loop
run = True
while run:
    timer.tick(fps) # this means we execute the code 60 times per second
    screen.fill(black) # the background
    boxes = draw_grid(clicked, active_beat)  # this is how we make 'boxes' available. Passing in 'clicked' helps us see what has been done before.
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_text = label_font.render("Play/Pause", True, white)
    screen.blit(play_text, (70, HEIGHT - 130))
    if playing:
        play_text2 = medium_font.render('Playing', True, dark_gray)
    else:
        play_text2 = medium_font.render('Paused', True, dark_gray)
    screen.blit(play_text2, (70, HEIGHT - 100))

    # bpm material to show changes
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (370, HEIGHT - 100))

    if beat_changed:  # this runs only when the beat changes. 
        play_notes()
        beat_changed == False  # as soon as it starts to play, we change it to False



    # "event handling":
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # this obviously shuts down the app.
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:  # don't understand this one.
            for i in range(len(boxes)):  # every time we update the beats, the whole thing has to be scalable and thus checkable.
                if boxes[i][0].collidepoint(event.pos):  # the '0' referecnes the rectangle we stored in the box, where I represents the tuple.
                    coords = boxes[i][1]
                                # we can use this Pygame function to see if the mouse collided with a rectangle (huh ...?!?)
                                # it does this by determining where our mouse was when we clicked.
                                # didn't understand his explanation on coords, other than it's a temporary variable that tracks if something has been clicked.
                    clicked[coords[1]][coords[0]] *= -1
                    # when clicked, it will multiply the existing -1 by itself, resulting in a positive 1.
                    # we can use that resulting list to draw the active cells on the screen.
        if event.type == pygame.MOUSEBUTTONUP: 
            if play_pause.collidepoint(event.pos): # if you press the button and it's plyaing, you then need playing to turn False (turn off)
                if playing: 
                    playing = False  # turns it off
                elif not playing:
                    playing = True   # turns it on

    beat_length = 3600//bpm  # this while loop will run 3600 per minute (!!) 3600 is actually fps * 60. 

    if playing:
        if active_length < beat_length: # how long has the beat we're currently on beeen active?
            active_length += 1  # this helps us track what beat we are currently on. Then we add one to it for every time we're not at beat length.
                                # did not explain the use/justification for the above if statements. 
                                # active_length might be what it is, and beat_length might be what it should be. 
        else:
            active_length = 0  # setting this to 0 stops it from adding 1 (meaning, you've reached the beat that you want.)
            # he talks about an "active cycle" or going on to the next step: what he means to say is where a beat is in a measure.
            if active_beat < beats - 1:
                active_beat += 1  # ... telling you to go to the next beat in the measure (seems like he's using 8/4 time)
                                    # if active is not less than, then you shoudl turn over to the next 8/4 measure.
                beat_changed = True  # an "on/off" variable that we will leave as a default to True.
            else:
                active_beat = 1 # meaning, you would start over in the measure.
                beat_changed = True  # still True becaues you have turned over to a new measure.

    pygame.display.flip()

pygame.quit() # this is to catch it if everything else doesn't work (it seems)
