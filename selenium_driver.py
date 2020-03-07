from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from util import Singleton


class SeleniumDriver:
    def __init__(self):
        try:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())

        except Exception as error:
            raise error


class Selenium(SeleniumDriver, metaclass=Singleton):
    pass
