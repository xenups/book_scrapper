# -*- coding: UTF-8 -*-
import logging
import threading
from threading import Thread
from unidecode import unidecode
from bookcrawler.models.model import Book, Publisher
from bookcrawler.selenium_driver import SeleniumDriver
from selenium.webdriver.chrome.webdriver import WebDriver
from bookcrawler.file_handler.csv_handler import CSVHandler
from bookcrawler.util import close_current_tab, open_new_tab, split_to_sublist


class BookScrapper(object):
    def __init__(self, without_browser=True, optimized_mode=True):
        self.without_browser = without_browser
        self.optimized_mode = optimized_mode
        self.csv_handler = CSVHandler()

    def multi_book_extractor_by_publishers_url(self, publishers_url, number_of_extractor=2):
        thread = Thread()
        __publishers = self.__scrape_publishers(publishers_url)

        __split_publishers_list = split_to_sublist(the_list=__publishers, number_of_sublist=number_of_extractor)

        for publishers in __split_publishers_list:
            thread = Thread(target=self.__extract_books_by_publishers, args=(publishers,))
            thread.daemon = True
            thread.start()
        thread.join()

    def __extract_books_by_publishers(self, publishers):
        driver = SeleniumDriver().chrome_driver(without_browser=self.without_browser,
                                                optimized_mode=self.optimized_mode)
        for publisher in publishers:
            books = self.__scrape_books_by_publishers(publisher, driver)
            thread_indent = threading.get_ident()
            self.csv_handler.export_book_to_csv(books=books, file_name="books " + str(thread_indent))

    def __scrape_publishers(self, publishers_url):
        driver = SeleniumDriver().chrome_driver(without_browser=self.without_browser,
                                                optimized_mode=self.optimized_mode)
        driver.get(publishers_url)
        logging.info('extracting publishers started')
        publishers_body = driver.find_element_by_tag_name("article")
        publishers_link = publishers_body.find_elements_by_xpath(".//a[@href]")
        publishers = []
        for link in publishers_link:
            publisher = Publisher()
            publisher.name = link.text
            publisher.url = link.get_attribute("href")
            publishers.append(publisher)
            logging.info(publisher.name)

        logging.info('extracting publishers finished')
        driver.close()
        return publishers

    def __scrape_books_by_publishers(self, publisher, driver: WebDriver):
        pages_count = self.__scrape_pages_count(url=publisher.url, driver=driver)
        list_books = []
        for page_number in range(1, pages_count + 1):
            logging.info(page_number)
            page_url = publisher.url + "?page=" + str(page_number)
            logging.info(page_url)
            driver.get(page_url)
            books = driver.find_elements_by_class_name("book")
            for book in books:
                book_instance = Book()
                book_instance.title = book.find_element_by_class_name("title").text
                book_instance.url = book.find_element_by_xpath(".//a[@href]").get_attribute("href")
                book_instance.author = book.find_element_by_class_name("author").text
                book_instance.publisher = publisher.name
                book_instance.price = self.__scrape_price_by_book_details(book_instance.url, driver)
                list_books.append(book_instance)
                logging.info(book_instance.title)
        return list_books

    def __scrape_price_by_book_details(self, page_url, driver: WebDriver):
        try:
            open_new_tab(driver)
            driver.get(page_url)
            section = driver.find_element_by_class_name("section-1")
            container = section.find_element_by_class_name("container")
            book_price = container.find_elements_by_class_name("book-price")[1].text
            close_current_tab(driver)
            return book_price
        except Exception as error:
            close_current_tab(driver)
            book_price = "0"
        return book_price

    def __scrape_pages_count(self, url, driver: WebDriver):
        page_without_pagination_count = 1
        try:
            driver.get(url)
            pages = driver.find_element_by_class_name("pagination")
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
