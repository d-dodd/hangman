import random
import re
import sys
import fileinput

words_file = open("spelling_words.txt", encoding="utf-8")
words = words_file.read()
words_list = re.findall(r'\w+', words)

with open("player_scores.txt") as f:
    lines = f.readlines()
lines = [x.strip() for x in lines]
      

print("Welcome to hangman!")
print("You're guy is dead after 10 wrong guesses!")
print("\nHOW SCORING WORKS")
print(" + If you WIN, you get 1 point for every guess you had left.")
print(" + If you LOSE, you lose a point for the number of correct guesses it would've taken to win.")
print("    - For example, if you lose with this still left (the word is \"Mississippi\"):")
print("            M _ s s _ s s _ _ _ _")
print("       you would lose 2 points, because it would've taken 2 correct guesses to win ")
print("       (it would've taken you guessing \"i\" and \"p\".)")



class HangmanGame(object):

    def __init__(self):

        self.the_word = random.choice(words_list)

        self.word_length = len(self.the_word)

        self.wrong_guesses = []
        self.right_guesses = []

        self.vowels_not_guessed = ["a", "e", "i", "o", "u", "y"]
        self.consonants_not_guessed = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]

        self.letters_left = []
        for letter in self.the_word:
            if letter.lower() not in self.letters_left:
                self.letters_left.append(letter.lower())

        self.game_status = []
        num = self.word_length
        while num > 0:
            self.game_status.append("_")
            num -= 1

        
        self.players_scores = {}
        for entry in lines:
            comma = entry.find(",")
            name = entry[0:comma]
            score = int(entry[comma+2:len(entry)])
            self.players_scores[name] = score  
        
        self.avatar_name = ""
        self.running_score = 0
        
        self.num_wrong = 0


    def played_before(self):
        ans1 = input("\nDo you have a permanent avatar for this game on this computer? (Y/n) ")
        if ans1[0].lower() != "y":
            ans2 = input("Would you like to create one to play this game with? ")
            if ans2[0].lower() == "y":
                self.get_name()
            else:
                name = ""
                self.name_and_score(name)
                self.game_initialize()
        else:
            self.what_name()

            
    def what_name(self):
        ans3 = input("What's its name? ")
        if ans3 in self.players_scores:
            print("\nWelcome back, {}!\n".format(ans3))
            self.name_and_score(ans3)
            self.game_initialize()
        else:
            print("We don't have any record of that name. That means we're going to have to go through this rigamorole again, man.\n Make sure you get the spelling right, and, like, also pay attention to capitalization.")
            self.played_before()


    def get_name(self):
        ans1 = input("What name would you like your avatar to have? (Think hard about it. You'll never be able to change its name!) ")
        ans2 = input("\nOK. So you're saying you want its name to be \"{}\". You sure you want this name for all eternity? (Y/n) ".format(ans1))
        if ans2[0].lower() != "y":
            print("Alrighty then! Let's try this thing again!")
            self.get_name()
        else:
            if ans1 not in self.players_scores:
                print("\nOK, you've made your decision. No looking back, dude! \n\n\nBut Jesus said to him, \"No one, having put his hand to the plow, and looking back, is fit for the kingdom of God.\" (Luke 9:62)\n\n\n")
                self.players_scores[ans1] = 0
                self.name_and_score(ans1)
                self.game_initialize()
            else:
                ans3 = input("Actually, that name is already taken. \nIf you forgot that you DO have a permanent avatar, type \"X\". Otherwise, just hit RETURN. ")
                if ans3.lower() != "x":
                    self.get_name()
                else:
                    self.played_before()


    def name_and_score(self, name):
        self.avatar_name = name
        if name == "":
            self.running_score = 0
        else:
            self.running_score = self.players_scores[name]
            
    def game_initialize(self):
        print(self.avatar_name)
        print("YOUR SCORE: "+str(self.running_score))
        self.next_move()

    def next_move(self):
        print("Number of guesses left: "+str(format(10-self.num_wrong)))
        print("WRONG GUESSES:")
        if self.num_wrong > 0:
            for letter in self.wrong_guesses:
                print(" "+letter, end="")
        print("\nVOWELS YOU HAVEN'T USED:")
        for letter in self.vowels_not_guessed:
            print(" "+letter, end="")
        print("\nCONSONANTS YOU HAVEN'T USED:")
        for letter in self.consonants_not_guessed:
            print(" "+letter, end="")
        print("\n")
        for item in self.game_status:
              print(item+" ", end="")
        guess = input("\nGuess a letter! ")
        self.check_guess(guess)


    def check_guess(self, letter):
        if letter.isalpha()==False or len(letter)!=1:
            print("Please guess a LETTER and make sure it's EXACTLY 1 letter!")
        else:
            if letter.lower() in self.wrong_guesses or letter.lower() in self.right_guesses:
                print("You already guessed that one!")
            elif letter.lower() in self.the_word.lower():
                print("\nYes, that letter is in the word.")
                self.right_answer(letter)
            elif letter.lower() not in self.the_word.lower():
                print("\nNo, that letter isn't in the word.")
                self.wrong_answer(letter)
        self.next_move()


    def right_answer(self, guess):
        i = 0
        guess = guess.lower()
        for letter in self.the_word:
            if guess == letter.lower():
                self.game_status[i] == letter
            i += 1
        self.right_guesses.append(guess)
        self.update_game_status(guess)
        self.update_not_guessed(guess)
        if self.won():
            print("Congratulations, you just won! The word was \"{}\".".format(self.the_word))
            print("Your win earned you {} points.".format(10-self.num_wrong))
            self.recalibrate_score()
            self.play_again()


    def wrong_answer(self, guess):
        guess = guess.lower()
        self.num_wrong += 1
        if self.lost():
            print("Sorry, that was your 10th wrong answer, so you lost. The word was actually \"{}\".".format(self.the_word))
            lost = self.points_lost()
            print("There were {} letters left to guess, so your loss cost you {} points.".format(lost, lost))
            self.recalibrate_score()
            self.play_again()
        else:
            self.wrong_guesses.append(guess)
            self.update_not_guessed(guess)


    def update_game_status(self, guess):
       i = 0
       while i < self.word_length:
            if self.the_word[i].lower()==guess:
                self.game_status[i] = self.the_word[i]
                i += 1
            else:
                i += 1


    def won(self):
        for item in self.game_status:
            if item == "_":
                return False
        return True


    def lost(self):
        if self.num_wrong < 10:
            return False
        else:
            return True


    def play_again(self):
        ans = input("\nWant to play again? (Y/n) ")
        if ans[0].lower() == "y":
            print("Awesome!\n")
            self.reset_class_variables()
            self.game_initialize()
        else:
            print("FINAL SCORE: "+str(self.running_score))
            print("\nFine, be that way! I didn't want to play with you either!\n")
            #self.rewrite_player_file(self.avatar_name, self.running_score)
            sys.exit()


    def reset_class_variables(self):
        self.vowels_not_guessed = ["a", "e", "i", "o", "u", "y"]
        self.consonants_not_guessed = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "z"]
        self.the_word = random.choice(words_list)
        self.word_length = len(self.the_word)
        self.wrong_guesses = []
        self.right_guesses = []
        self.letters_left = []
        for letter in self.the_word:
            if letter.lower() not in self.letters_left:
                self.letters_left.append(letter.lower())
        self.game_status = []
        num = self.word_length
        while num > 0:
            self.game_status.append("_")
            num -= 1
        self.num_wrong = 0


    def update_not_guessed(self, guess):
        if guess in self.vowels_not_guessed:
            self.vowels_not_guessed.remove(guess)
        else:
            self.consonants_not_guessed.remove(guess)


    def recalibrate_score(self):
        if self.won():
            self.running_score += (10-self.num_wrong)
            if self.avatar_name != "":
                self.players_scores[self.avatar_name] = self.running_score
        else:
            self.running_score -= self.points_lost()
            if self.avatar_name != "":
                self.players_scores[self.avatar_name] = self.running_score
        self.rewrite_player_file()


    def points_lost(self):          
        guesses_left = ""
        i = 0
        while i < len(self.game_status):
            if self.game_status[i] == "_":
                if self.the_word[i] not in guesses_left:
                    guesses_left += self.the_word[i]
            i += 1
        return len(guesses_left)


    def rewrite_player_file(self):
        f = open("player_scores.txt", 'w')
        temp_list = []
        for item in self.players_scores:
            temp_list.append(item+", "+str(self.players_scores[item])+"\n")
        i = 0
        while i<len(temp_list):
            f.write(temp_list[i])
            i += 1
        f.close()


    
if __name__ == '__main__':
    game = HangmanGame()
    game.played_before()
