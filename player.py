import string

CORRECT = 2
SOMEWHERE = 1
INCORRECT = 0

ALPHABET = list(string.ascii_lowercase)

def loadWordList():
    f = open('dictionary.txt', 'r')
    content = f.readlines()

    words = []
    for item in content:
        words.append(item[:-1])
    f.close()

    return words

class Player:
    def __init__(self):
        #Main wordlist
        self.__wordList = loadWordList()

        #List of words which we still think it could be
        self.__possibleWords = self.__wordList.copy()

        #Dictionary to store values of each char in each position
        self.__charScores = [ {key : 0 for key in ALPHABET} for i in range(5)]

        self.__firstGuess = True

    def getPossibleWords(self):
        return self.__possibleWords

    def __calculateCharScores(self):
        self.__charScores = [ {key : 0 for key in ALPHABET} for i in range(5)]

        #Foreach word in all words
        for word in self.__possibleWords:

            #Foreach character in word
            addedLetters = [] #For letters which could be anywhere, we only want to add the score once
            for n, c in enumerate(word):

                #If letter not added everywhere yet
                if c not in addedLetters:
                    #Add value to each position in scores
                    for position in self.__charScores:
                        position[c] += 5
                
                #Extra value for exact position
                self.__charScores[n][c] += 10

    def getGuess(self):
        if self.__firstGuess:
            self.__currentGuess = 'crude'
            self.__firstGuess = False
            return self.__currentGuess

        self.__calculateCharScores()

        bestWord = None
        bestScore = -100

        for word in self.__wordList:
            score = 0
            for n, c in enumerate(word):
                score += self.__charScores[n][c]
            
            if score>bestScore:
                bestScore = score
                bestWord = word

        self.__currentGuess = bestWord
        return self.__currentGuess

    def giveFeedback(self, feedback):
        print(f'\nbefore feedback: {len(self.__possibleWords)} possible words')
        print('taking feedback. most recent guess:', self.__currentGuess)
        print(f'feedback: {feedback}')
        #Feedback is in 5-long list of CORRECT, SOMEWHERE, INCORRECT
        impossibles = []

        for position, outcome in enumerate(feedback):
            c = self.__currentGuess[position]
            if outcome == CORRECT:
                for word in self.__possibleWords:
                    if word[position] != c:
                        impossibles.append(word)
            elif outcome == SOMEWHERE:
                for word in self.__possibleWords:
                    if c in word:
                        if word[position] == c:
                            impossibles.append(word)
                    else:
                        impossibles.append(word)
            elif outcome == INCORRECT:
                for word in self.__possibleWords:
                    if c in word:
                        impossibles.append(word)
            else:
                raise ValueError(f'Unrecognised outcome {outcome}')
            
        newPossibleWords = []
        for word in self.__possibleWords:
            if not word in impossibles:
                newPossibleWords.append(word)
            
        self.__possibleWords = newPossibleWords
        print(f'after feedback: {len(self.__possibleWords)} possible words\n')

    def displayInfo(self):
        print(f'Most recent guess: {self.__currentGuess}')
        print(f'Possible words: {self.__possibleWords}')


def getFeedback(answer, guess):
    feedback = []
    for n, c in enumerate(guess):
        if c in answer:
            if answer[n] == c:
                feedback.append(CORRECT)
            else:
                feedback.append(SOMEWHERE)
        else:
            feedback.append(INCORRECT)
    return feedback

def testPlayer(answer):
    player = Player()
    run = True
    while run:
        guess = player.getGuess()

        if guess == answer:
            print(f'Answer guessed correctly: {guess}')
            run = False
            break

        print(f'Guess: {guess}')

        feedback = getFeedback(answer, guess)

        player.giveFeedback(feedback)

if __name__ == "__main__":
    testPlayer('other')
