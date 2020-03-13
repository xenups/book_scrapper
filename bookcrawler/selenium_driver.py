from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bookcrawler.util import Singleton


class SeleniumDriver:
    @staticmethod
    def chrome_driver(hide_image=True, without_browser=True):
        chrome_options = webdriver.ChromeOptions()
        if without_browser:
            chrome_options.add_argument('headless')
        if hide_image:
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
        web_driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        return web_driver
