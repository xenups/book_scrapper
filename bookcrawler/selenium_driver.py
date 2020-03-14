from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class SeleniumDriver:

    def chrome_driver(self, optimized_mode=True, without_browser=True):
        chrome_options = webdriver.ChromeOptions()

        if without_browser:
            chrome_options.add_argument('headless')
        if optimized_mode:
            prefs = {"profile.managed_default_content_settings.images": 2,
                     "profile.default_content_setting_values.notifications": 2,
                     "profile.managed_default_content_settings.stylesheets": 2,
                     "profile.managed_default_content_settings.cookies": 2,
                     "profile.managed_default_content_settings.javascript": 1,
                     "profile.managed_default_content_settings.plugins": 1,
                     "profile.managed_default_content_settings.popups": 2,
                     "profile.managed_default_content_settings.geolocation": 2,
                     "profile.managed_default_content_settings.media_stream": 2,
                     }

            chrome_options.add_experimental_option("prefs", prefs)
        web_driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        return web_driver
