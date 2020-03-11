# -*- coding: UTF-8 -*-
import logging
import sys
from unidecode import unidecode

from bookcrawler.file_handler.csv_handler import export_book_to_csv
from bookcrawler.models.model import Book, Publisher
from selenium.webdriver.chrome.webdriver import WebDriver


class BookScrapper(object):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def extract_books_by_publishers(self, publishers_url):
        publishers = self.__extract_publishers(publishers_url)
        for publisher in publishers:
            books = self.__scrape_books_by_publishers(publisher)
            export_book_to_csv(books=books)

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

        for page_number in range(1, pages_count + 1):
            page_url = publisher.url + "?page=" + str(page_number)
            self.driver.get(page_url)
            books = self.driver.find_elements_by_class_name("book")
            logging.info('extracting publishers started')
            for book in books:
                book_instance = Book()
                book_instance.title = book.find_element_by_class_name("title").text
                book_instance.author = book.find_element_by_class_name("author").text
                book_instance.publisher = publisher.name
                list_books.append(book_instance)
                logging.info(book_instance.title)
            logging.info('extracting publishers finished')
        return list_books

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
