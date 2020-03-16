# -*- coding: UTF-8 -*-
import logging
from unidecode import unidecode

from bookcrawler.file_handler.csv_handler import export_book_to_csv
from bookcrawler.models.model import Book, Publisher
from selenium.webdriver.chrome.webdriver import WebDriver

from bookcrawler.selenium_driver import SeleniumDriver
from bookcrawler.util import background, close_current_tab, open_new_tab


class BookScrapper(object):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def extract_books_by_publishers(self, publishers_url):
        publishers = self.__extract_publishers(publishers_url)
        for publisher in publishers:
            try:
                books = self.__scrape_books_by_publishers(publisher)
                export_book_to_csv(books=books, file_name="fidibo")
            except:
                pass

    def __extract_publishers(self, publishers_url):
        self.driver.get(publishers_url)
        logging.info('extracting publishers started')
        publishers_body = self.driver.find_element_by_tag_name("article")
        publishers_link = publishers_body.find_elements_by_xpath(".//a[@href]")
        publishers = []
        for link in publishers_link:
            publisher = Publisher()
            publisher.name = link.text
            publisher.url = link.get_attribute("href")
            publishers.append(publisher)
            logging.info(publisher.name)

        logging.info('extracting publishers finished')
        return publishers

    def __scrape_books_by_publishers(self, publisher):
        pages_count = self.__extract_pages_count(url=publisher.url)
        list_books = []
        driver = SeleniumDriver().chrome_driver(without_browser=False)
        for page_number in range(1, pages_count + 1):
            page_url = publisher.url + "?page=" + str(page_number)
            driver.get(page_url)
            books = driver.find_elements_by_class_name("book")
            logging.info('extracting publishers started')
            for book in books:
                book_instance = Book()
                book_instance.title = book.find_element_by_class_name("title").text
                book_instance.url = book.find_element_by_xpath(".//a[@href]").get_attribute("href")
                book_instance.author = book.find_element_by_class_name("author").text
                book_instance.publisher = publisher.name
                book_instance.price = self.__scrape_price_by_book_details(book_instance.url)
                list_books.append(book_instance)
                logging.info(book_instance.title)
            logging.info('extracting publishers finished')
        return list_books

    def __scrape_price_by_book_details(self, page_url):
        try:
            open_new_tab(self.driver)
            self.driver.get(page_url)
            section = self.driver.find_element_by_class_name("section-1")
            container = section.find_element_by_class_name("container")
            book_price = container.find_elements_by_class_name("book-price")[1].text
            close_current_tab(self.driver)
            return book_price
        except Exception as error:
            close_current_tab(self.driver)
            print(error.args)
            book_price = "0"
        return book_price

    def __extract_pages_count(self, url):
        page_without_pagination_count = 1
        try:
            self.driver.get(url)
            pages = self.driver.find_element_by_class_name("pagination")
            standard_format = unidecode(pages.text)
            pages_list = list(standard_format.split(" "))
            numbers = []
            for item in pages_list:
                for subitem in item.split():
                    if subitem.isdigit():
                        numbers.append(subitem)
            numbers = list(map(int, numbers))
            return numbers[-1]
        except Exception as e:
            return page_without_pagination_count
