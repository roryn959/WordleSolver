CORRECT = 0
SOMEWHERE = 1
INCORRECT = 2

class Game:
    def __init__(self, answer):
        self.__attempts = 0
        self.__answer = answer

    def getAnswer(self):
        return self.__answer

    def getAttempts(self):
        return self.__attempts
    
    def makeAttempt(self, guess):
        if guess == self.__answer:
            feedback = [CORRECT for i in range(5)]
        else:
            feedback = []
            for n, c in guess:
                if c in self.__answer:
                    if self.__answer[n]==c:
                        feedback.append(CORRECT)
                    else:
                        feedback.append(SOMEWHERE)
                else:
                    feedback.append(INCORRECT)
        self.__attempts += 1
        return feedback