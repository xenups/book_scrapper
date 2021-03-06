﻿# -*- coding: UTF-8 -*-
import logging

from bookcrawler.models.model import Book, Publisher, Category
from bookcrawler.file_handler.csv_handler import CSVHandler
from bookcrawler.selenium_driver import SeleniumDriver

CATEGORY_URL = "https://www.ketabrah.ir/book-category/%DA%A9%D8%AA%D8%A7%D8%A8%E2%80%8C%D9%87%D8%A7%DB%8C-%D8%AD%D9%82%D9%88%D9%82/"
PUBLISHERS_URL = "https://www.ketabrah.ir/page/publishers"


class BookScrapper(object):
    def __init__(self, without_browser=False, optimized_mode=True):
        self.driver = SeleniumDriver().chrome_driver(without_browser=without_browser, optimized_mode=optimized_mode)
        logging.info("initializing finished")
        self.csv_handler = CSVHandler()

    def extract_books_by_category(self):
        logging.info("extract_books_by_category started")
        categories = self.__scrape_categories_link(category_url=CATEGORY_URL)
        out_put_file = ""
        for category in categories:
            out_put_file = self.csv_handler.export_book_to_csv(self.__scrape_books_by_category(category),
                                                               file_name="ketabrah")
        return out_put_file

    def extract_books_by_publishers(self):
        logging.info("extract_books_by_publisher started")
        publishers = self.__scrape_publishers_link(publishers_url=PUBLISHERS_URL)
        out_put_file = ""
        # for test
        # publishers = publishers[-2:]
        for publisher in publishers:
            out_put_file = self.csv_handler.export_book_to_csv(self.__scrape_books_by_publishers(publisher),
                                                               file_name="ketabrah")
        return out_put_file

    def __scrape_books_by_category(self, category):
        list_books = []
        page_index = 1
        while True:
            url = self.__generate_url(category.url, page_index)
            self.driver.get(url)
            try:
                books_list_element = self.driver.find_element_by_class_name("book-list")
                books_list_element = books_list_element.find_elements_by_class_name("item")
                try:
                    for book in books_list_element:
                        book_instance = Book()
                        book_instance.title = book.find_element_by_class_name("title").text
                        logging.info(book_instance.title)
                        book_instance.author = book.find_element_by_class_name("authors").text
                        book_instance.price = book.find_element_by_class_name("price").text
                        book_instance.category = category.title
                        list_books.append(book_instance)
                except Exception as e:
                    pass
                page_index = page_index + 1
            except Exception as e:
                return list_books

    @staticmethod
    def __generate_url(url, page_index):
        _url = url + "/page-" + str(page_index)
        return _url

    def __scrape_categories_link(self, category_url):
        categories = []
        self.driver.get(url=category_url)
        menu_items = self.driver.find_element_by_class_name("cr-menu")
        items = menu_items.find_elements_by_class_name("crm-item")
        for item in items:
            category_url = item.find_element_by_xpath(".//a[@href]").get_attribute("href")
            if "book-category" in category_url:
                category = Category()
                category.url = category_url
                logging.info(item.text)
                category.title = item.text
                categories.append(category)
        return categories

    def __scrape_publishers_link(self, publishers_url):
        self.driver.get(publishers_url)
        publishers_list_element = self.driver.find_element_by_class_name("publishers-list")
        publisher_blocks_elements = publishers_list_element.find_elements_by_class_name("publisher-block")
        list_publishers = []
        for publisher_block in publisher_blocks_elements:
            publisher = Publisher()
            publisher.url = publisher_block.get_attribute("href")
            publisher.name = publisher_block.find_element_by_class_name("publisher-block-name").text
            logging.info(publisher.name)
            list_publishers.append(publisher)
        return list_publishers

    def __scrape_books_by_publishers(self, publisher):
        list_books = []
        page_index = 1
        while True:
            url = self.__generate_url(publisher.url, page_index)
            self.driver.get(url)
            try:
                books_list_element = self.driver.find_element_by_class_name("book-list")
                books_list_element = books_list_element.find_elements_by_class_name("item")
                try:
                    for book in books_list_element:
                        book_instance = Book()
                        book_instance.title = book.find_element_by_class_name("title").text
                        logging.info(book_instance.title)
                        book_instance.author = book.find_element_by_class_name("authors").text
                        book_instance.price = book.find_element_by_class_name("price").text
                        book_instance.publisher = publisher.name
                        list_books.append(book_instance)
                except Exception as e:
                    pass
                page_index = page_index + 1
            except Exception as e:
                return list_books
