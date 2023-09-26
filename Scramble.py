import random
import os
import time
import datetime
import words
import json

"""
Guess the Word Game:

-Displays scrambled word. - [DONE]
-Only have 3 chances to guess word. - [DONE]
-Add points to score if guess is correct. - [DONE]
    Extra points if word is guessed on first try. - [DONE]
    Reduce points if user unable to guess the word after 3 attempts. - [DONE]   
-Add ability to shuffle letters. [DONE]
    Set a limit to how many times a word can be shuffled to (3) per attempt. [DONE]
-Add High-Score list which saves/formatted to json(?) file [DONE]
    Show Top scores in menu [WIP]
"""

words = words.words

SHUFF_COUNT = 0  # Keeps track of player's shuffle count - Don't change this.

TIME = datetime.datetime.strftime(datetime.datetime.now(),
                                  "%m/%d/%Y - %H:%M:%S")


def get_word():  # Grabs a random word from 'word' list.
    word = random.choice(words)

    return word


def scramble(word):  # Scrambles a word and returns in list format
    scrambled = []
    scrambled += word
    random.shuffle(scrambled)

    return scrambled


def shuff(word: list):  # Handles word shuffle
    global SHUFF_COUNT

    try:
        while True:
            if SHUFF_COUNT == 3:
                print("You can only shuffle 3 times per attempt.\nMake a guess!")
                break

            if SHUFF_COUNT == 0:
                prompt = input("Would you like to shuffle? (Y)es/(N)o: ").upper()
            else:
                prompt = input("Would you like to shuffle again? (Y)es/(N)o: ").upper()

            if prompt == "Y":
                SHUFF_COUNT += 1
                print("Shuffling...")
                random.shuffle(word)
                time.sleep(0.5)
                print("Shuffled: %s" % word)

            elif prompt == "N":
                SHUFF_COUNT = 0
                break

            else:
                print("Choose Yes/No...")

    except Exception as e:
        print("Something happened...\n %s" % e)


def menu():  # Handles menu choice 1/2 player
    try:
        while True:
            print(f"Welcome to The Word Challenge!",
                  f"\nSelect an option:",
                  f"\n\t[1] Single Player",
                  f"\n\t[2] Versus Mode - Work in Progress...",
                  f"\nIf you would like to save/quit the game; Enter 'exit' or 'quit' for a guess..."
                  )

            gtype = input(f"Choice: ")

            if gtype == str(1):
                player1 = input("Player 1: ")
                os.system('cls')
                break

            elif gtype == str(2):
                print("Still a work in progress...")
                time.sleep(1.5)
                os.system('cls')


            else:
                print("You must choose an option...")

        return player1

    except Exception as e:
        print("Something Happened... %s" % e)


def high_score(player, score):
    try:
        save = {"Name": f"{player}",
                "Score": f"{score}",
                "Date": f"{TIME}"}

        jsave = json.dumps(save)

        with open("high_scores.json", "r") as rs:
            saved = rs.read()
            rs.close()

        with open("high_scores.json", "w") as ws:
            ws.write(f"{saved}\n" + jsave)
            ws.close()

    except Exception as e:
        print("Something Happened...\nPlease contact the developer with this: %s" % e)


def save_exit(player, score):
    try:
        while True:
            print(f"Are you sure you want to Save and Exit?\n",
                  "Your score will be saved in 'high_scores.json' and will be displayed in the menu, in the future.\n",
                  "Choose (Y)es/(N)o...")

            prompt = input("Choice: ").upper()

            if prompt == "Y" or prompt == "YES":
                print(f"Saving...\n Player Name: {player}\n Score: {score}")
                high_score(player, score)
                time.sleep(3)
                print("Exiting...")
                time.sleep(2)
                exit()

            elif prompt == "N" or prompt == "NO":
                break

            else:
                print("Make a choice...")

    except Exception as e:
        print("Something Happened... Error: %s" % e)


def main():
    global SHUFF_COUNT
    p1 = menu()
    p1_chance = 0

    p2_chance = 0
    p2_max = 0

    p1_score = 0
    p2_score = 0

    saved = []
    word = get_word()  # THE WORD
    while True:
        scrambled = scramble(word)

        print("{} Score: {}".format(p1, p1_score))

        print(f"\n\nScrambled Word:\n{scrambled}\n\n")

        # DEBUG (Shows the word)
        # print(word)

        shuff(scrambled)  # Shuffle prompt

        if SHUFF_COUNT >= 2:
            SHUFF_COUNT = 0

        guess = input(f"Guess: ").upper()

        if guess == "EXIT" or guess == "QUIT":
            save_exit(p1, p1_score)

        if p1_chance == 0 and guess == word:  # Guess on first try = More points
            p1_score += 20
            print(f"WOW! You guessed on the first try! +20 points")

        if guess != word:  # Tracks player attempts
            p1_chance += 1
            print(f"Incorrect!\nYou have {3 - p1_chance} guesses left!")
            time.sleep(1.5)
            os.system('cls')

            if p1_chance < 3:
                print("Try Again...\nAttempts Left: {}".format(3 - p1_chance))

            if p1_chance == 3:  # if you use all attempts
                p1_score -= 10
                p1_chance = 0
                print(f"You have used all 3 of your chances to guess the last word. -10 points",
                      f"\nThe word was: {word}")
                word = get_word()

        else:  # Guess word correctly
            p1_chance = 0
            p1_score += 10
            print("CORRECT! +10 points",
                  f"\nScore: {p1_score}")

            words.remove(word)
            saved.clear()
            time.sleep(1)
            os.system('cls')
            word = get_word()


if __name__ == "__main__":
    main()
