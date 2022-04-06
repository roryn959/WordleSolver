# WordleSolver

Hello! This project uses the Selenium library in Python to open Wordle and complete the day's word.

> To run, navigate to project folder. Run 'controller.py' using Python version 3 or above. For example, 'python3 controller.py'.

**Dependency:** This project uses a Chrome driver to navigate the web - the programme will not run without this. I downloaded mine from <a href="https://chromedriver.chromium.org">here</a>. If you wish to use an alternative web driver, you may edit line 10 of 'view.py' to your choosing.

**Known Bug:** The description of the rules of Wordle are somewhat ambiguous. In which way does the game handle repeated letters? For example, imagine the answer is 'rules' and you guess 'curry'. Should the game mark both 'r's as yellow because they are both contained within the word? Or should the game mark one 'r' as yellow and one as black, since there's only one 'r' in the answer? When developing the logic for my player, unfortunately none of the daily answers contained repeated letters, so I could not test this. As such, I made a guess and it turned out to be wrong. This means if the answer contains repeated letters the program may fail, which you will notice if the program guesses 'aback' several times in a row.
