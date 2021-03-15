# Game_Hangman_Python
A simple game of hangman coded in Python showcasing Object Oriented Programming (OOP). 
This is from a project for my MS in Data Science at UC Berkeley for W200 -  Introduction to Data Science Programming. Have fun!

Run the game from your command line in pyhthon, 'game.py.'

### Instructions

1.	The program is designed to be run from the terminal. Players will call the main program (‘game.py’) after initiating python.
2.	The user will be asked to enter their name and then select a level of difficulty:
    a.	Name = Any combination of letters or characters accepted
    b.	Difficulty = input options: 
      i.	‘easy’ = words have a length of 7 letters
      ii.	‘hard’ = words have a length of 9 letters
3.	The user will then be asked to confirm the entered information is correct otherwise the program exits. 
4.	The player will then begin guessing letters one at a time. 
    a.	If letters are correct, the player receives a message indicating this as well as where the letter belongs in the word. The letter is also displayed within the word.
    b.	If the letter guessed is incorrect, the player is given a message indicating this.
      i.	If a player guesses incorrectly in series, the program prompts a question to the player to determine if they would like a hint. 
        o Easy setting – hint prompt is generated after 2 incorrect guesses
        o	Hard setting – hint prompt is generated after 3 incorrect guesses
        o	If the player denies the hint, it will prompt again after each incorrect guess until the game ends or the user accepts the hint. 
c.	If a player guesses a letter they have already guessed, a message arises indicated this. The total number of guesses remaining are not affected.
5.	If the player enters 7 incorrect guesses, the player loses. Otherwise, the player wins by guessing the word.
