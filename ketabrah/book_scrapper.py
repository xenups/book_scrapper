# -*- coding: UTF-8 -*-
from bookcrawler.models.model import Book, Publisher, Category
from selenium.webdriver.chrome.webdriver import WebDriver
from bookcrawler.file_handler.csv_handler import export_book_to_csv


class BookScrapper(object):
    def __init__(self, url, driver: WebDriver):
        self.driver = driver
        self.url = url

    def extract_by_category(self):
        categories = self.__scrape_categories_link()
        print(categories)
        for category in categories:
            export_book_to_csv(self.__scrape_books_by_category(category))

    def extract_by_publishers(self):
        publishers = self.__scrape_publishers_link()
        print(publishers)
        for publisher in publishers:
            export_book_to_csv(self.__scrape_books_by_publishers(publisher))

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
                        book_instance.author = book.find_element_by_class_name("authors").text
                        book_instance.price = book.find_element_by_class_name("price").text
                        book_instance.category = category.title
                        list_books.append(book_instance)
                        print(book_instance.title)
                except Exception as e:
                    pass
                page_index = page_index + 1
            except Exception as e:
                return list_books

    @staticmethod
    def __generate_url(url, page_index):
        _url = url + "/page-" + str(page_index)
        return _url

    def __scrape_categories_link(self):
        categories = []
        self.driver.get(self.url)
        menu_items = self.driver.find_element_by_class_name("cr-menu")
        items = menu_items.find_elements_by_class_name("crm-item")
        for item in items:
            url = item.find_element_by_xpath(".//a[@href]").get_attribute("href")
            if "book-category" in url:
                category = Category()
                category.url = url
                print(item.text)
                category.title = item.text
                categories.append(category)
        return categories

    def __scrape_publishers_link(self):
        publishers_url = "https://www.ketabrah.ir/page/publishers"
        self.driver.get(publishers_url)
        publishers_list_element = self.driver.find_element_by_class_name("publishers-list")
        publisher_blocks_elements = publishers_list_element.find_elements_by_class_name("publisher-block")
        list_publishers = []
        for publisher_block in publisher_blocks_elements:
            publisher = Publisher()
            publisher.url = publisher_block.get_attribute("href")
            publisher.name = publisher_block.find_element_by_class_name("publisher-block-name").text
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
                        book_instance.author = book.find_element_by_class_name("authors").text
                        book_instance.price = book.find_element_by_class_name("price").text
                        book_instance.publisher = publisher.name
                        list_books.append(book_instance)
                        print(book_instance.title)
                except Exception as e:
                    pass
                page_index = page_index + 1
            except Exception as e:
                return list_books
