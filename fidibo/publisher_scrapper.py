from selenium_driver import webdriver
from book import Publisher


class PublisherScrapper(object):
    def __init__(self, url, driver):
        self.driver = driver
        self.url = url

    def extract_publishers(self):
        self.driver.get(self.url)

        publishers_body = self.driver.find_element_by_tag_name("article")
        publishers_link = publishers_body.find_elements_by_xpath(".//a[@href]")
        publishers = []
        for link in publishers_link:
            publisher = Publisher()
            publisher.name = link.text
            publisher.link = link.get_attribute("href")
            publishers.append(publisher)
        return publishers
