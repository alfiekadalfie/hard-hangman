import random, sys, winsound
 
class Hangman():
    
    def __init__(self, word):
        self.word = word
        self.tries = 6
        self.lettersguessed = []
        self.guess = self.createGuess(self.word)
    
    def show_hangman(self, tries):
        stages = [
            """        
               _____
               |   |
               |   O
               |  \|/
               |  / \\
               | /   \\
            """
            ,
            """
               _____
               |   |
               |   O
               |  \|/
               |  /
               | /
            """
            ,
            """
               _____
               |   |
               |   O
               |  \|/
               |
               |
            """
            ,
            """
               _____
               |   |
               |   O
               |  \|
               |
               |
            """
            ,
            """
               _____
               |   |
               |   O
               |   |
               |
               |
            """
            ,
            """
               _____
               |   |
               |   O
               |
               |
               |
            """
            ,
            """
               _____
               |   |
               |
               |
               |
               |
            """
        ]

        return stages[tries]
    
    #in case of spaces in word
    def createGuess(self, word):
        formGuess = ""

        for i in word:
            if i==" ":
                formGuess += " "
            else:
                formGuess += "_"
        
        return formGuess
    
    #checks if letter has not been guessed yet; will be used in check method
    def guessLetter(self, guess):
        print(guess)

        if self.tries == 1:
            letter = input("\nGuess a letter. You have 1 life remaining. ").lower()
        else:
            letter = input("\nGuess a letter. You have " + str(self.tries) + " lives remaining. ").lower()

        #needs to be valid letter to continue
        if letter.isalpha() and len(letter) == 1:
            while letter.lower() in self.lettersguessed:
                letter = input("\nThat letter was already guessed. Guess another letter: ").lower()
            
            self.lettersguessed.append(letter.lower())
        else:
            print("\nNot a valid letter.\n")
            print(self.show_hangman(self.tries))
            self.guessLetter(guess)
    
    #checks if letter is in word
    def check(self, letter):
        if letter in self.word:

            #beep when letter is in word
            winsound.Beep(frequency=1000, duration=100)

            found = list(self.guess)
                
            i=0
            while i<len(self.word):
                if letter.lower() == self.word[i]:
                    found[i] = letter.upper()
                i+=1
            
            newguess = ""
            for i in found:
                newguess += i
            
            #guess attribute is modified with capital letters if letters are found
            self.guess = newguess
            
        else:
                
            print("\nThat letter is not in the word.")
            self.tries-=1
    
    #asks to restart the game or not
    def gameover(self):

        #print final result
        print("\n"+self.guess)  

        if self.tries==0:
            tryagain = input("\nOh no, you lost! The word was " + self.word.upper() + ". Would you like to play again? Enter yes or no: ").lower()

            if tryagain == "yes":
                main()
            
        elif "_" not in self.guess:
            if self.tries == 1:
                tryagain = input("\nYay, you guessed the word with 1 life remaining! The word was " + self.word.upper() + ". Would you like to play again? Enter yes or no: ").lower()
            else:
                tryagain = input("\nYay, you guessed the word with " + str(self.tries) + " lives remaining! The word was " + self.word.upper() + ". Would you like to play again? Enter yes or no: ").lower()

            if tryagain == "yes":
                main()
        
        sys.exit("\nAlright. Play again next time!")


#(might develop a scoreboard system to keep track of how much in a row) one letter is missing
#if that letter is guessed, it counts as a no-show (tries-=1)
#same constructor, just modified methods to go along with hard hangman
class HardHangman(Hangman):

    def __init__(self, word):
        self.poison = word[random.randint(0, len(word)-1)]

        super().__init__(word)
        self.guess = self.createHardGuess(word)
        

    def createHardGuess(self, word):
        formGuess = ""

        for i in word:
            if i==" ":
                formGuess += " "
            elif i==self.poison:
                formGuess += "|"
            else:
                formGuess += "_"
        
        return formGuess
    
    #checks if letter is in word
    def check(self, letter):

        if letter in self.word:
            if letter == self.poison:
                print("\nThat letter is not in the word.")
                self.tries-=1
            else:

                #beep when letter is in word
                winsound.Beep(frequency=1000, duration=100)

                found = list(self.guess)

                i=0
                while i<len(self.word):
                    if letter.lower() == self.word[i]:
                        found[i] = letter.upper()
                    i+=1
            
                newguess = ""
                for i in found:
                    newguess += i
            
                #guess attribute is modified with capital letters if letters are found
                self.guess = newguess
            
        else:
                
            print("\nThat letter is not in the word.")
            self.tries-=1

#plays hangman
def main():
    hard = input("Do you want to play hard hangman? Enter yes or no: ").lower()

    #reads words from a file and picks one; can assume will always be lowercase letters only
    words = []

    with open("hangmanwords.txt") as f:
        while f.readline() != "":
            words.append(f.readline().rstrip("\n"))

    #select random word from word list
    word = words[random.randint(0, len(words)-1)]

    if hard == "no":
        x = Hangman(word)
    
        print(x.show_hangman(x.tries))
        print("Letters guessed: " + str(x.lettersguessed))

        while x.tries and "_" in x.guess:
            x.guessLetter(x.guess)
    
            letter = x.lettersguessed[len(x.lettersguessed)-1]

            x.check(letter)

            print(x.show_hangman(x.tries))
            print("Letters guessed: " + str(x.lettersguessed))
    
    elif hard == "yes":
        x = HardHangman(word)

        print(x.show_hangman(x.tries))
        print("Letters guessed: " + str(x.lettersguessed))

        while x.tries and "_" in x.guess:
            x.guessLetter(x.guess)
    
            letter = x.lettersguessed[len(x.lettersguessed)-1]

            x.check(letter)

            print(x.show_hangman(x.tries))
            print("Letters guessed: " + str(x.lettersguessed))
    
    x.gameover()

#main()