from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class WebPlayer:
    def __init__(self):
        self.__page_open = False
        self.__driver = webdriver.Chrome()
        self.__letter_positions = {'q':(1, 1), 'w':(1, 2), 'e':(1, 3), 'r':(1, 4), 't':(1, 5), 'y':(1, 6), 'u':(1, 7), 'i':(1, 8), 'o':(1, 9), 'p':(1, 10), 'a':(2, 2), 's':(2, 3), 'd':(2, 4), 'f':(2, 5), 'g':(2, 6), 'h':(2, 7), 'j':(2, 8), 'k':(2, 9), 'l':(2, 10), 'z':(3, 2), 'x':(3, 3), 'c':(3, 4), 'v':(3, 5), 'b':(3, 6), 'n':(3, 7), 'm':(3, 8)}
        self.__lastRow = 0

    def __startDriver(self):
        if not self.__page_open:
            self.__driver.get("https://www.nytimes.com/games/wordle/index.html")
            self.__page_open = True
            self.__findElements()

        else:
            raise ValueError('Page is already open!')

    def __getShadowElement(self, parent):
        return self.__driver.execute_script('return arguments[0].shadowRoot', parent)

    def __findElements(self):
        game_app = self.__driver.find_element(By.XPATH, '/html/body/game-app')
        game_app_shadow = self.__getShadowElement(game_app)

        game_theme_manager = game_app_shadow.find_element(By.CSS_SELECTOR, 'game-theme-manager')
        self.__game_div = game_theme_manager.find_element(By.CSS_SELECTOR, '#game')

        game_modal = self.__game_div.find_element(By.CSS_SELECTOR, '#game > game-modal')

        game_help = game_modal.find_element(By.CSS_SELECTOR, '#game > game-modal > game-help')
        game_help_shadow = self.__getShadowElement(game_help)

        self.__game_help_instructions_div = game_help_shadow.find_element(By.CSS_SELECTOR, 'section > div')

        game_keyboard = self.__game_div.find_element(By.CSS_SELECTOR, '#game > game-keyboard')
        game_keyboard_shadow = self.__getShadowElement(game_keyboard)

        self.__keyboard_div = game_keyboard_shadow.find_element(By.CSS_SELECTOR, '#keyboard')
        self.__enter_key = self.__keyboard_div.find_element(By.CSS_SELECTOR, '#keyboard > div:nth-child(3) > button:nth-child(1)')

    def __getBoardRow(self, n):
        return self.__game_div.find_element(By.CSS_SELECTOR, f'#board > game-row:nth-child({n})')

    def __rejectCookies(self):
        rejectButton = self.__driver.find_element(By.CSS_SELECTOR, 'button#pz-gdpr-btn-reject')
        rejectButton.click()

        print('Implicit wait for snackbar...')
        time.sleep(10)
        print('Snackbar should be gone.')

    def __closeHelp(self):
        self.__game_help_instructions_div.click()

    def __inputLetter(self, c):
        position = self.__letter_positions[c]
        self.__keyboard_div.find_element(By.CSS_SELECTOR, f'#keyboard > div:nth-child({position[0]}) > button:nth-child({position[1]})').click()
    
    def __pressEnter(self):
        self.__enter_key.click()

    def inputWord(self, word):
        print('Inputting', word)
        for c in word:
            self.__inputLetter(c)
        self.__pressEnter()
        self.__lastRow += 1

        print('Waiting for answer results...')
        time.sleep(3)

    def getFeedback(self):
        lastRow = self.__getBoardRow(self.__lastRow)
        row_shadow = self.__getShadowElement(lastRow)

        feedback = []
        for i in range(1, 6):
            tile = row_shadow.find_element(By.CSS_SELECTOR, f'div > game-tile:nth-child({i})')
            result = tile.get_attribute('evaluation')

            #CORRECT = 2, SOMEWHERE = 1, INCORRECT = 0
            if result == 'correct':
                feedback.append(2)
            elif result == 'present':
                feedback.append(1)
            elif result == 'absent':
                feedback.append(0)
            else:
                raise ValueError('Unrecognised board tile evaluation.')
        return feedback

    def setUp(self):
        self.__startDriver()
        self.__rejectCookies()
        self.__closeHelp()
    
    def tearDown(self):
        self.__driver.quit()
        self.__page_open = False