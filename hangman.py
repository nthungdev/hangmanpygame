import time
import random
import string
import pygame
import my_color

pygame.init()

# resolution
screen_w = 1280
screen_h = 960

# Surface
screen = pygame.display.set_mode((screen_w,screen_h))

# Title
pygame.display.set_caption('Hangman')

# The game's clock
clock = pygame.time.Clock()

# Game Properties
streak = 0
score = 0
lives = 9

# Set streak to 0
def reset():
    global streak
    global score
    global lives
    streak = 0
    score = 0
    lives = 9

def setLives(n):
    global lives
    lives = n
    print("I was called")

# Return the elapsed time in seconds has passed since start is marked
def elapsed_time(start, dif):
    dif_int = int((pygame.time.get_ticks()-start)/1000)
    if dif_int != dif:
        return dif_int
    else:
        return 0

# Start a countdown for bonus points. Return the elapsed time since started the stage
def countdown(start, dif):
    passed = elapsed_time(start, dif)
    time = 30 - passed
    if time <= 0:
        return 0
    else:
        return time

# Return a random word from txt file list of academic words
def get_word():
    # Get a random line number
    words = open('resources/words.txt','r')
    file = words.read()
    lines = file.count("\n") + 1
    random.seed()
    picked_word = random.randrange(0,lines)
    words.close()

    # Get the word at the random line
    words = open('resources/words.txt','r')
    word = ""
    count = 0
    for line in words:
        if count == picked_word:
            word = line
        count += 1
    words.close()
    return word.strip()

# Is user input a name in alphabet?
def is_valid(name):
    alphabet = string.ascii_lowercase
    if name in alphabet:
        return True
    return False

# Is user input a name correct or wrong?
def is_correct(name,word):
    if name in word.lower():
        return True
    return False

# Return a word with letters replaced by _(s)
def covered_word(word, correct):
    out = ""
    for i in word:
        if i.lower() in correct: # lower or upper case does not matter so make both i and correct lower
            out = out + i
        else:
            out = out + "_"
    return out

# Print a word with letters replaced by _(s)
def print_covered_word(word, correct):
    cword = covered_word(word, correct)
    space = 35
    word_l = len(cword)
    center_x = screen_w / 2
    begin_x = center_x - space*(word_l/2) - (word_l//2)
    begin_y = 600

    for i in range(word_l):
        print_text1(screen, cword[i], 'resources/fonts/tahoma.ttf', 45, my_color.white, (begin_x + i*(space)), begin_y)

# Print which letters are guessed
def print_letter_tracking(correct, incorrect):
    pygame.draw.rect(screen, my_color.green, (screen_w/8*6, (screen_h/36*27), screen_w/8*2, screen_h/36*6))

    correct_list = list(correct)
    correct_list.sort()
    print_text2(screen, 'CORRECT LETTERS', 'freesansbold.ttf', 25, my_color.black, screen_w/8*6, (screen_h/36*27))
    for i in range(len(correct)):
        font = pygame.font.Font('freesansbold.ttf', 25)
        text_surface = font.render(correct_list[i], True, my_color.black)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = (screen_w/8*6 + i*30), (screen_h/36*28)
        screen.blit(text_surface,text_rect)

    incorrect_list = list(incorrect)
    incorrect_list.sort()
    print_text2(screen, 'INCORRECT LETTERS', 'freesansbold.ttf', 25, my_color.black, screen_w/8*6, (screen_h/36*30))
    for i in range(len(incorrect)):
        font = pygame.font.Font('freesansbold.ttf',25)
        text_surface = font.render(incorrect_list[i], True, my_color.black)
        text_rect = text_surface.get_rect()
        text_rect.x, text_rect.y = (screen_w/8*6 + i*30), (screen_h/36*31)
        screen.blit(text_surface,text_rect)

# Print a rectangle clickable button
def botton(smg, smgc, x, y, w, h, ic, ac, action=None):
    global state
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == 'start':
                reset()
                play_loop()

            elif action == 'pause':
                paused()

            elif action == 'unpause':
                unpause()

            elif action == 'continue':
                setLives(9)
                play_loop()

            elif action == 'menu':
                menu_loop()

            elif action == 'quit':
                pygame.quit()
                quit()

            elif action == 'end':
                reset()
                end_loop()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))
    print_text1(screen, smg, 'freesansbold.ttf', int(h*0.4), smgc, (2*(x)+w)/2, (2*(y)+h)/2)

# Print text position by center coor
def print_text1(surface, text, font, size, color, centerx, centery):
    font = pygame.font.Font(font,size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = ((centerx),(centery))
    surface.blit(text_surface,text_rect)

# Print text position by top left corner
def print_text2(surface, text, font, size, color, x, y):
    font = pygame.font.Font(font,size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.x, text_rect.y = x, y
    surface.blit(text_surface,text_rect)

# Set pause to false
def unpause():
    global pause
    global start_time
    global pause_start
    pause = False
    pause_end = pygame.time.get_ticks()
    start_time = start_time + pause_end - pause_start

# Pause the Game with another screen
def paused():
    global pause
    global pause_start
    pause = True
    pause_start = pygame.time.get_ticks()
    screen.fill(my_color.black)
    print_text1(screen, 'PAUSED', 'resources/fonts/arial.ttf', 150, my_color.white, screen_w/2, 300)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        botton('RESUME', my_color.black, (screen_w/2-75), (screen_h*1/2+50), 150, 50, my_color.green, my_color.dark_green,'unpause')
        botton('QUIT', my_color.black,screen_w/2-75, screen_h*1/2+100, 150, 50, my_color.red, my_color.dark_red,'quit')

        pygame.display.update()
        clock.tick(60)

# Menu UI
def menu_loop():
    intro = True
    screen.fill(my_color.black)
    print_text1(screen, 'HANGMAN', 'resources/fonts/arial.ttf', 150, my_color.white, screen_w/2, 300)

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        botton('START', my_color.black, (screen_w/2-75), (screen_h*1/2+50), 150, 50, my_color.green, my_color.dark_green,'start')
        botton('QUIT', my_color.black,screen_w/2-75, screen_h*1/2+100, 150, 50, my_color.red, my_color.dark_red,'quit')

        pygame.display.update()
        clock.tick(60)

# Playing U
def play_loop():
    global word
    global lives
    global score
    global streak
    global dif
    global start_time
    word = get_word()
    correct = set()
    incorrect = set()
    wrongs = 0
    msg_end = 0
    dif = 0
    start_time = pygame.time.get_ticks()

    while True:
        # Show Prgress
        background = pygame.image.load('resources/pictures/' + str(wrongs) + '.png')
        screen.blit(background,(0,0))
        print_covered_word(word, correct)
        botton('SCORES: '+str(score), my_color.black, 0, 150, 150, 50, my_color.green, my_color.dark_green)
        botton('STREAKS: '+str(streak), my_color.black, 0, 200, 150, 50, my_color.green, my_color.dark_green)
        botton('LIVES: '+str(lives), my_color.black, 0, 250, 150, 50, my_color.green, my_color.dark_green)
        botton('BONUS: '+str(countdown(start_time, dif)), my_color.black, 0, 300, 150, 50, my_color.green, my_color.dark_green)

        print_letter_tracking(correct, incorrect)

        for event in pygame.event.get():
            # Handle non-keyboard input
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle keyboard input
            if pygame.key.get_focused():
                press = pygame.key.get_pressed()
                for i in range(0,len(press)):
                    if press[i]==1:
                        name = pygame.key.name(i)

                        # Process keyboard input
                        if is_valid(name):

                            # Guess is already made
                            if name in correct or name in incorrect:
                                guess_result = (1,0,0)
                                msg_end = int(time.localtime().tm_sec + 2)

                            # Guess is correct
                            elif is_correct(name,word):
                                correct.add(name.lower())
                                guess_result = (0,1,0)
                                msg_end = int(time.localtime().tm_sec + 2)
                                score += 5

                            # Guess is wrong
                            else:
                                incorrect.add(name)
                                lives -= 1
                                wrongs += 1
                                guess_result = (0,0,1)
                                msg_end = int(time.localtime().tm_sec + 2)

        # Print message for current guess
        if time.localtime().tm_sec < msg_end:
            if guess_result[0] == 1:
                print_text1(screen, "You guessed " + str(name) + " already!", 'freesansbold.ttf', 20, my_color.white, screen_w/2, screen_h/4*3)
            elif guess_result[1] == 1:
                print_text1(screen, "Good guess!", 'freesansbold.ttf', 20, my_color.white, screen_w/2, screen_h/4*3)
            elif guess_result[2] == 1:
                print_text1(screen, "Try another letter :(", 'freesansbold.ttf', 20, my_color.white, screen_w/2, screen_h/4*3)

        # All letters are guessed
        if not "_" in covered_word(word, correct):
            streak += 1
            score += 20 + countdown(start_time, dif)

            end_loop()

        # Out of lives
        if lives == 0:
            #reset()
            end_loop()

        # UI Bottons
        botton('MENU', my_color.black, 0, screen_h-50, 150, 50, my_color.green, my_color.dark_green,'menu')
        botton('PAUSE', my_color.black, screen_w/2 - int(150/2), screen_h-50, 150, 50, my_color.green, my_color.dark_green,'pause')
        botton('RETRY', my_color.black, screen_w-150, screen_h-50, 150, 50, my_color.green, my_color.dark_green,'start')

        # Keep track of frames
        pygame.display.update()
        clock.tick(60)

# Finished Game Screen
def end_loop():
    background = pygame.image.load('resources/pictures/0.png')
    screen.blit(background,(0,0))
    print_covered_word(word, word.lower())
    print_text1(screen, 'GAME OVER', 'resources/fonts/arial.ttf', 120, my_color.white, screen_w/2, 325)
    if lives == 0:
        print_text1(screen, "YOU LOSE", 'resources/fonts/arial.ttf', 120, my_color.dark_red, screen_w/2, 500)
    else:
        print_text1(screen, "YOU WIN", "resources/fonts/arial.ttf", 120, my_color.dark_red, screen_w/2, 500)

    # UI Bottons
    botton('SCORES: '+str(score), my_color.black, 0, 150, 150, 50, my_color.green, my_color.dark_green)
    botton('STREAKS: '+str(streak), my_color.black, 0, 200, 150, 50, my_color.green, my_color.dark_green)
    botton('LIVES: '+str(lives), my_color.black, 0, 250, 150, 50, my_color.green, my_color.dark_green)
    botton('BONUS: '+str(countdown(start_time, dif)), my_color.black, 0, 300, 150, 50, my_color.green, my_color.dark_green)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if lives == 0:
            botton('PLAY AGAIN', my_color.black, (screen_w/2-75), (screen_h*1/2+200), 150, 50, my_color.green, my_color.dark_green,'start')
        else:
            botton('CONTINUE', my_color.black, (screen_w/2-75), (screen_h*1/2+200), 150, 50, my_color.green, my_color.dark_green,'continue')
        botton('MAIN MENU', my_color.black,screen_w/2-75, screen_h*1/2+250, 150, 50, my_color.light_blue, my_color.dark_blue,'menu')
        botton('QUIT', my_color.black,screen_w/2-75, screen_h*1/2+300, 150, 50, my_color.red, my_color.dark_red,'quit')
        pygame.display.update()
        clock.tick(60)

menu_loop()

pygame.quit()
quit()
