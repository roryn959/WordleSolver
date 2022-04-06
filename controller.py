import player as p
import view as v
import time

def gameLoop(engine, web):
    while True:
        guess = engine.getGuess()
        web.inputWord(guess)
        feedback = web.getFeedback()
        print(feedback)
        
        #Answer found?
        if feedback == [2, 2, 2, 2, 2]:
            break

        engine.giveFeedback(feedback)

        engine.displayInfo()

if __name__ == '__main__':
    engine = p.Player()
    web = v.WebPlayer()

    web.setUp()
    gameLoop(engine, web)

    print('Answer found...')
    time.sleep(10)
    web.tearDown()