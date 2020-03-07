from selenium_driver import webdriver
from book import Publisher
from selenium_driver import ChromeDriverManager


class PublisherScrapper(object):
    def __init__(self, url):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)

        main_page = driver.find_elements_by_class_name("main")
        # columns = driver.find_element_by_class_name("list-unstyled col-sm-4")
        for column in main_page:
            print('hi')
            link = column.get_attribute("href")
            print(link)
            publishers = []
            for publish in main_page:
                publisher = Publisher()

                col = publish.find_elements_by_tag_name("ul")
                for c in col:
                    nashr = c.find_element_by_tag_name("li").text
                    print(nashr)

                publishers.append(publisher)
            print((publishers.__len__()))
