#! 
import os
import time
import random
import string

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

# Is user input a letter in alphabet?
def is_valid(letter):
    alphabet = string.ascii_lowercase
    if letter in alphabet:
        return True
    return False

# Is user input a letter correct or wrong?
def is_correct(letter,word):
    if letter in word.lower():
        return True
    return False

# Return a word with letters replaced by _ based on user's guess
def covered_word(word, correct):
    out = ""
    for i in word:
        if i.lower() in correct: # lower or upper case does not matter so make both i and correct lower
            out = out + " " + i
        else:
            out = out + " _"
    return out

def game_main():
    word = get_word()
    correct = set()
    incorrect = set()
    lives = 10
    wrongs = 10 - lives

    end = False
    trial = 0

    while not end:
        # Print Prgress
        print(covered_word(word, correct))
        print("Trial number: ", trial)
        print("Lives: ", lives)

        letter = input('I guess this letter: ').lower()

        # Process user input
        if is_valid(letter):
            # Guess is already made
            if letter in correct or letter in incorrect:
                print("You guessed that already!")
            # Guess is correct
            elif is_correct(letter,word):
                trial += 1
                correct.add(letter.lower())
            # Guess is wrong
            else:
                trial += 1
                incorrect.add(letter)
                lives -= 1
        else:
            print("I think you have a typo!")

        # When out of lives or guess all letters
        if lives <= 0 or not "_" in covered_word(word, correct):
            end = True

        os.system("cls")

    # Result
    if lives > 0:
        print(covered_word(word, correct))
        print("You win!")
    else: 
        print("You loses!")

    input('Hit any key to Exit')
                   
game_main()