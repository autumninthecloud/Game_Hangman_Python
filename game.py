import random
import json
import string
import sys
import time
import wordlist as wl
import hangmanviz as hgv

# Creating variables for shorthand

savefile = "game_data.json"
# Formatting variable for shorthand

linebanner = "\n========================================\n"
# Ascii statement for game outcome

win_statement = """

          _
         (_)
__      ___ _ __  _ __   ___ _ __
\ \ /\ / / | '_ \| '_ \ / _ \ '__|
 \ V  V /| | | | | | | |  __/ |
  \_/\_/ |_|_| |_|_| |_|\___|_|

"""

loss_statement = """
  __ _  __ _ _ __ ___   ___    _____   _____ _ __
 / _` |/ _` | '_ ` _ \ / _ \  / _ \ \ / / _ \ '__|
| (_| | (_| | | | | | |  __/ | (_) \ V /  __/ |
 \__, |\__,_|_| |_| |_|\___|  \___/ \_/ \___|_|
  __/ |
 |___/

"""


# First class - identifies word for guessing based on user input
class gameword:
    """Retrieves the word based on user inputs"""
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.gameword = False

    def getWord(self):
        """A function to randomly select a word from the wordlist dictionary
        based on the difficulty selected from the user at the command line."""
        if self.gameword:
            return self.gameword
        if difficulty == 'easy':
            self.gameword = random.choice(list(wl.easy.keys()))
        else:
            self.gameword = random.choice(list(wl.hard.keys()))
        return self.gameword


# Second class - logic for the game including functions
class hangman:
    """Class to iterate through guesses with user."""
    def __init__(self, gameword, difficulty, hint, name):
        self.gameword = gameword
        self.difficulty = difficulty
        self.hint = hint
        self.name = name
        self.guesses = list()
        self.guesscounter = 0
        self.correctguesses = list()
        self.scoreboard = Scoreboard(self)
        self.inncorrectguesscounter = 0
        self.setGuessesRemaining()
        while True:
            if not self.guessesremaining:
                print("\n### Sorry, better luck next time - GAME OVER!")
                print(loss_statement)
                self.scoreboard.complete(status="loss")
                break
            elif len(self.gameword) - len(self.correctguesses) == 0:
                print("\n### Congrats, you've won! Check out the scoreboard!")
                print(win_statement)
                self.scoreboard.complete(status="win")
                break
            self.showVisual()
            self.getGuess()
            if not self.validateGuess():
                self.hint.promptHint(self)
            self.setGuessesRemaining()
        return None

    def getGuess(self):
        """ A function to iterate through guesses and display number of
         remaining guesses available.
         """
        while True:
            if self.guesscounter > 1:
                print(
                    "Number of incorrect guesses"
                    " remaining: %i" % self.guessesremaining)
            self.guess = input(
                "\nWhat is your guess (#%i)? > " % self.guesscounter)
            print("\n"*50)

            if len(self.guess) != 1:
                print("Sorry - invalid guess length - try again.\n")
            elif self.guess not in string.ascii_letters:
                print("Sorry - invalid guess character - try again.\n")
            elif self.guess in self.guesses:
                print("Sorry - you've already tried that guess - try again.\n")
            else:
                self.guess = self.guess.lower()
                self.guesses.append(self.guess)
                break

        print("Guess #%i: %s" % (self.guesscounter, self.guess))
        return None

    def validateGuess(self):
        """ A function to validate guesses for matching in the game word."""
        if self.guess in self.gameword:
            for i in range(self.gameword.count(self.guess)):
                self.correctguesses.append(self.guess)
            print(
                "\nCongrats! - Your guess of \"%s\" was correct. That letter"
                " is in position number %i."
                % (self.guess, self.gameword.index(self.guess)+1))
            return True
        else:
            self.inncorrectguesscounter += 1
            print("\nSorry - Your guess was incorrect. Try again!")
            return False

    def setGuessesRemaining(self):
        """ A function to keep track of total number of guesses."""
        self.guesscounter += 1
        self.guessesremaining = (6
                                 - self.inncorrectguesscounter)
        return self.guessesremaining

    def showVisual(self):
        """ A function to print the hangman visual as guesses are made."""
        print(linebanner)
        print(hgv.board[self.inncorrectguesscounter])

        line = ""
        for c in self.gameword:
            if c in self.guesses:
                line += c.upper()
            else:
                line += "_"
            line += " "

        print("Game Word >> ", line)
        print(linebanner)
        return None


# Third class = hint generator!
class hintGenerator:
    """A class to generate hints for guesses"""

    def __init__(self, gameword, difficulty):
        self.difficulty = difficulty
        self.gameword = gameword
        self.hint = self.getHint()

    def getHint(self):
        """ A function to retrieve a hint value from the corresponding key
        (game word) based on difficulty selected."""
        if self.difficulty == "easy":
            self.hint = wl.easy[self.gameword]
        elif self.difficulty == "hard":
            self.hint = wl.hard[self.gameword]
        return self.hint

    def promptHint(self, hangman):
        """ A function to ask the player if they would like a hint."""
        if hangman.inncorrectguesscounter >= 2 and self.hint:
            while True:
                r = input("\nWould you like a hint? [Y\\N] > ").upper()
                if r == "Y":
                    print("\n\nYour hint is: %s\n\n" % self.hint)
                    self.hint = False
                    time.sleep(4)
                    break
                else:
                    print("\n\nOk, I'll ask again later.\n\n")
                    time.sleep(1)
                    break

    def IncorrectGuessAction(self):
        """A funtion that monitors internally the number of incorrect
        guesses, prompts the user if they would like a hint if a threshold is
        met based on difficulty, if yes, calls getHint().
        """

        if self.difficulty == 'easy' and hangman.getGuess() == 2:
            print(
                "You've guessed incorrectly 2 times in a row."
                "Would you like a hint?")
            "run getHint()"
        if self.difficulty == 'hard' and guesscounter == 2:
            print("You've guessed incorrectly 3 times in a row."
                  "Would you like a hint?")
            "run getHint()"
        return getHint(self.difficulty, self.gameword)


# Fourth class - the scoreboard!
class Scoreboard():
    def __init__(self, hangman):
        self.hangman = hangman
        self.scoredata = False
        self.playerRecordID = False

    def printScoreboard(self):
        """ A function to print the scoreboard."""
        if not self.scoredata:
            self.loadScores()

        print(linebanner)
        print("### GAME SCOREBOARD ###")
        for r in self.scoredata['players']:
            print(
                "name: %s\tWins: %i\t\tLosses: %i\tTotal Games: %i"
                % (r['name'], r['wins'], r['losses'], r['wins']+r['losses']))
        print(linebanner)
        return None

    def loadScores(self):
        """ A function to load the json file with scores."""
        with open(savefile, 'r') as outfile:
            self.scoredata = json.load(outfile)

    def saveScores(self, status):
        """ A function to save scores to the scoreboard."""
        if not self.scoredata:
            self.loadScores()

        for i in range(len(self.scoredata['players'])):
            if self.scoredata['players'][i]['name'] == self.hangman.name:
                self.playerRecordID = i

        if self.playerRecordID:
            if status == "win":
                self.scoredata['players'][self.playerRecordID]['wins'] += 1
            else:
                self.scoredata['players'][self.playerRecordID]['losses'] += 1
        else:
            if status == "win":
                self.scoredata['players'].append(
                    {"name": self.hangman.name, "wins": 1, "losses": 0})
            else:
                self.scoredata['players'].append(
                    {"name": self.hangman.name, "wins": 0, "losses": 1})

        with open(savefile, 'w') as outfile:
            json.dump(self.scoredata, outfile)

        return None

    def complete(self, status):
        self.saveScores(status)
        self.printScoreboard()


class gameEngine():
    """A function to run our hangman game.
    Takes the user inputs and runs the program.
    """
    def __init__(self, name, difficulty):
        self.name = name
        self.difficulty = difficulty
        print(linebanner)
        print("Please confirm your inputs below:")
        print("\tName:\t\t%s" % self.name)
        print("\tDifficulty:\t%s" % self.difficulty)
        print(linebanner)
        confirmation = input("[Yes = Y or No = N] >>").upper()
        if confirmation == "Y":
            print("\n\n\t\tLet's Play!\n\n")
            time.sleep(0.1)
        else:
            print("\nExiting Game..")
            sys.exit()
        return None

    def run(self):
        self.gameword = gameword(self.difficulty).getWord()
        self.hint = hintGenerator(self.gameword, self.difficulty)
        # print("=====>>  ", self.gameword) # Activated in demo mode only
        hangman(self.gameword, self.difficulty, self.hint, self.name)


if __name__ == "__main__":
    try:
        # User Inputs
        name = input("Welcome to Hangman! Please enter your name: ").upper()
        while True:
            difficulty = input("Please choose level of difficulty:"
                               " easy or hard? ")
            if difficulty not in ["easy", "hard"]:
                print("Please enter either - case sensitive: easy OR hard")
            else:
                break

        g = gameEngine(name, difficulty)
        g.run()
    except:
        print("Sorry, Game Error - Please Restart =]")
