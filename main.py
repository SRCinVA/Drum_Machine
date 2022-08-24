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
active_list = [1 for _ in range(instruments)] # somehow, this makes the the default channels on, but any can be turned off by clicking
bpm = 240
playing = True
active_length = 0  # not understanding this one at the moment ...
active_beat = 0
beat_changed = True # still not clear on this one. You would want this to be active as soon as the app loads.
save_menu = False  # this will be False at the beginning
load_menu = False  # also False at the beginning
saved_beats = [] # takes on the beats you have saved
# file = open("saved_beats.txt", 'r')  # storage for the beats; it will start out as 'read'. Seems like there's no DB involved.
# for line in file:  # each line in the file will be all the info needed for one beat.
#    saved_beats.append(line)
beat_name = ''
typing = False

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
        if clicked[i][active_beat] == 1 and active_list[i] == 1:  # you'll check where the active beat is at each row [i], but what he mans by '1' is unclear.
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
        # you don't even need an else statement. If either condition fails, then that instrument simply won't play.

def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 210, HEIGHT - 200], 5)   # x and y starting coordinates, width, and height
                                                                        # "5" clarifies how wide we want the edges to be.
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 200, WIDTH, 200], 3)
                                                                        # it will start at 200 above the bottom of the screen
                                                                        # pygame grid stops at top left
    boxes = []  # this might be for individual tracks
    colors = [gray, white, gray]
    hi_hat_text = label_font.render('Hi Hat', True, colors[actives[0]]) # if it's in 'actives,' each track will be white (a 1 in the list); if inactive, it will be gray (a -1 in the 'colors' list).
                                                                        # second term above is an anti-alias (smooth borders for lines)
                                                                        # don't know why he distinguishes 'actives' and 'active_list'
                                                                        # it goes through the index of each instrument (0-5) to change the color.
    screen.blit(hi_hat_text, (30, 30))  # draws it on the screen, with the coordinates.
    
    snare_text = label_font.render('Snare', True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    
    bass_drum_text = label_font.render('Bass Drum', True, colors[actives[2]])
    screen.blit(bass_drum_text, (30, 230))
    
    crash_text = label_font.render('Crash', True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))

    clap_text = label_font.render('Clap', True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))

    floor_tom_text = label_font.render('Floor Tom', True, colors[actives[5]])
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
                if actives[j] == 1:   # it's 'j' because we're checking the instrument (see the code directly above)
                    color = green  # meaning, it's active (hopefully explained later).
                elif actives[j] == -1:  # you could just do 'else' here instead.
                    color = dark_gray

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

def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])   # it will be a full "secondary screen" with no rouding or edges.
    menu_text = label_font.render('SAVE MENU: Enter a name for current beat', True, white)
    saving_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.75, 400, 100], 0, 5)
    saving_text = label_font.render('Save beat', True, white)
    screen.blit(saving_text, (WIDTH // 2 - 75, HEIGHT * 0.75 + 30))
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5) # this turns the black field to a dark gray as soon as you start typing
    entry_rectangle = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5) # this will create a large empty rectangle (to entter information?)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, entry_rectangle # return the saving button because we need to check if there is a collision outside the function. 
                                            # also need to return entry_rect to see if we've typed into it or not
    
def draw_load_menu():
    pygame.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render('Load MENU: Select a beat to load', True, white) # notice that the next 5 lines were poached from the save menu.
    loading_btn = pygame.draw.rect(screen, gray, [WIDTH // 2 - 200, HEIGHT * 0.87, 400, 100], 0, 5)
    loading_text = label_font.render('Load beat', True, white)
    screen.blit(loading_text, (WIDTH // 2 - 75, HEIGHT * 0.87 + 30))
    delete_btn = pygame.draw.rect(screen, gray, [(WIDTH//2) - 500, HEIGHT * .87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete beat', True, white)
    screen.blit(delete_text, ((WIDTH//2) - 485, HEIGHT * .87 + 30))
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    # exit_button = rect.Rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)  
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    loaded_rectangle = pygame.draw.rect(screen, gray, [190, 90, 1000, 600], 5, 5)
    for beat in range(len(saved_beats)): # to recover a saved beat, you have to index through the string (seems bizarrely inefficient to do it this way ...)
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f'{beats + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].index('name: ') + 6 # this line and the next are what you need to pull out of the data in the text file.
            name_index_end = saved_beats[beat].index(',  beats:')
            name_text = medium_font.render(saved_beats[beat][name_index_start:name_index_end], True, white) # first go the beat (first index) then pull out the indexed characters from that string. Put those strings together, and they will add up to the name of the saved beat.
            screen.blit(name_text, (240, 100 + beat * 50))  # puzzled by what these multplications mean ... 
        if 0 <= index < len(saved_beats) and beat == index: # beats failed to load, but this is how you would select them.
            beat_index_end = saved_beats[beat].index(', bpm:')
            loaded_beats = int(saved_beats[beat][name_index_end + 8: beat_index_end])
    return exit_btn, loading_btn, delete_btn, loaded_rectangle

# the main game loop
run = True
while run:
    timer.tick(fps) # this means we execute the code 60 times per second
    screen.fill(black) # the background
    
    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)  # no idea what exit button has to do with it. Also have to pass a few things into save_menu().
    if load_menu:
        exit_button = draw_load_menu()

    boxes = draw_grid(clicked, active_beat, active_list)  # this is how we make 'boxes' available. Passing in 'clicked' helps us see what has been done before.
    
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
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 218, 100], 5, 5)
    bpm_text = medium_font.render('Beats Per Minute', True, white)
    screen.blit(bpm_text, (308, HEIGHT - 130))
    bpm_text2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text2, (375, HEIGHT - 100))
    bpm_add_rect = pygame.draw.rect(screen, gray, [520, HEIGHT - 150, 48, 48], 0, 5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [520, HEIGHT - 100, 48, 48], 0, 5)
    add_text = medium_font.render("+1", True, white)
    sub_text = medium_font.render("-1", True, white)
    screen.blit(add_text, (530, HEIGHT - 140))
    screen.blit(sub_text, (530, HEIGHT - 90))

    # beats material
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 218, 100], 5, 5)
    beats_text = medium_font.render('Beats in Loop', True, white)
    screen.blit(beats_text, (628, HEIGHT - 130))
    beats_text2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text2, (695, HEIGHT - 100))
    beats_add_rect = pygame.draw.rect(screen, gray, [820, HEIGHT - 150, 48, 48], 0, 5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [820, HEIGHT - 100, 48, 48], 0, 5)
    add_text2 = medium_font.render("+1", True, white)
    sub_text2 = medium_font.render("-1", True, white)
    screen.blit(add_text2, (830, HEIGHT - 140))
    screen.blit(sub_text2, (830, HEIGHT - 90))

    # instrument rectangles (to control the channels)
    instrument_rects = []
    for i in range(instruments):
        rect = pygame.rect.Rect((0, i * 100), (200, 100))  # defining a rectangle but NOT putting it on the screen.
                                                # this one only needs (1.)  x and y starting position (for 'y', it goes down 100 at a time and always stays on the left) and (2.) the button size
        instrument_rects.append(rect)  # basically, we're sticking that new rectangle to the end of the instument_rects list
        
    # save and load functionality
    save_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 150, 218, 48], 0, 5)
    save_text = label_font.render('Save Beat', True, white)
    screen.blit(save_text, (928, HEIGHT - 140))
    load_button = pygame.draw.rect(screen, gray, [900, HEIGHT - 100, 218, 48], 0, 5)
    load_text = label_font.render('Load Beat', True, white)
    screen.blit(load_text, (928, HEIGHT - 90))

    # clear board functionality
    clear_button = pygame.draw.rect(screen, gray, [1200, HEIGHT - 150, 218, 100], 0, 5)
    clear_text = label_font.render('Clear Board', True, white)
    screen.blit(clear_text, (1228, HEIGHT - 120))

    # save and load menus
    if save_menu:
        exit_button, saving_button, entry_rectangle = draw_save_menu(beat_name, typing)  # no idea what exit button has to do with it
    if load_menu:
        exit_button, loading_button, delete_button, loaded_rectangle = draw_load_menu()


    if beat_changed:  # this runs only when the beat changes. 
        play_notes()
        beat_changed == False  # as soon as it starts to play, we change it to False

    # "event handling":
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # this obviously shuts down the app.
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and not save_menu and not load_menu:  # don't understand excluding save and load here ...
            for i in range(len(boxes)):  # every time we update the beats, the whole thing has to be scalable and thus checkable.
                if boxes[i][0].collidepoint(event.pos):  # the '0' referecnes the rectangle we stored in the box, where I represents the tuple.
                    coords = boxes[i][1]
                                # we can use this Pygame function to see if the mouse collided with a rectangle (huh ...?!?)
                                # it does this by determining where our mouse was when we clicked.
                                # didn't understand his explanation on coords, other than it's a temporary variable that tracks if something has been clicked.
                    clicked[coords[1]][coords[0]] *= -1
                    # when clicked, it will multiply the existing -1 by itself, resulting in a positive 1.
                    # we can use that resulting list to draw the active cells on the screen.
        
        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu: # same as above ... 
            if play_pause.collidepoint(event.pos): # if you press the button and it's plyaing, you then need playing to turn False (turn off)
                if playing: 
                    playing = False  # turns it off
                elif not playing:
                    playing = True   # turns it on
            
            # to change BPM
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 1
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 1                
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)   # adds another item to the end of the 'clicked' list
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1      
                for i in range(len(clicked)):
                    clicked[i].pop(-1)  # pulls off the last item on the 'clicked' list
            # to clear the board
            elif clear_button.collidepoint(event.pos):  # this resets everything back to what it was at the beginning--empty.
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            
            # to check if any of those instrument buttons have been clicked:
            for i in range(len(instrument_rects)): # this will check every instrument rectangle that we define
                if instrument_rects[i].collidepoint(event.pos): # ... to check if any instrument in there was clicked
                    active_list[i] *= -1    # whatever was just clicked on the active list at "i"
                                            # not sure about -1 here ...
        elif event.type == pygame.MOUSEBUTTONUP: # same as above ... 
            if exit_button.collidepoint(event.pos):  # this lets us both enter and exit a menu
                save_menu = False
                load_menu = False
                playing = True  # he says to do this so that it won't pause (?)
                beat_name = '' # reset beat name to an empty string
                typing = False # if you're closing it down, then you're clearly not typing.
            
            elif entry_rectangle.collidepoint(event.pos):  # not sure why, but if you click on the entry rectangle, then we want to switch the state of your typing to its opposite
                if typing:
                    typing = False
                elif not typing: # 'else' would not be effective here
                    typing = True
        
            elif saving_button.collidepoint(event.pos):
                file = open('saved_file.txt', 'w')
                saved_beats.append(f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')  # start it with a new line
                                                                                        # notice that this is writing down each of the characteristics of the beat
                for i in range(len(saved_beats)): # appending each piece of the above info to the existing saves_beats list
                    file.write(str(saved_beats[i]))
                file.close() # saves it outside the file
                save_menu = False # takes you out of save_menu, and sets everything back to default (doesn't really explain this)
                typing = False
                beat_name = ''

        if event.type == pygame.TEXTINPUT and typing:  # this may cover the action of how you actually enter text into that field.
            beat_name += event.text  # this turns what you enter into that field into the beat's name. Without the '+=', the field can't be added to. 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame. K_BACKSPACE and len(beat_name) > 0 and typing:  # to check if the backspace key was pressed and to confirm that there actually is a beatname (possibly)
                beat_name = beat_name[:-1] # this will grab the entire string right up to the most recent character, enabling us to rename the beat.
        # with the five lines above, the entry rectangle can determine if we are actively typing or not.

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
                active_beat = 0 # meaning, you would start over in the measure at the beginning.
                beat_changed = True  # still True becaues you have turned over to a new measure.

    pygame.display.flip()

pygame.quit() # this is to catch it if everything else doesn't work (it seems)
