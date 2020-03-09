from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bookcrawler.util import Singleton


class SeleniumDriver:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

        except Exception as error:
            raise error


class Selenium(SeleniumDriver, metaclass=Singleton):
    pass
