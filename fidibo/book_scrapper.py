﻿# -*- coding: UTF-8 -*-
from unidecode import unidecode
from book import Book


class BookScrapper(object):
    def __init__(self, url, driver):
        self.driver = driver
        self.url = url

    def extract_books(self):
        pages_count = self.__extract_pages_count(url=self.url)
        print(pages_count)
        list_books = []

        for page_number in range(1, pages_count + 1):
            page_url = self.url + "?page=" + str(page_number)
            self.driver.get(page_url)
            books = self.driver.find_elements_by_class_name("book")
            for book in books:
                book_instance = Book()
                book_instance.title = book.find_element_by_class_name("title").text
                book_instance.author = book.find_element_by_class_name("author").text
                list_books.append(book_instance)
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
                    if (subitem.isdigit()):
                        numbers.append(subitem)
            numbers = list(map(int, numbers))
            return numbers[-1]
        except Exception as e:
            return page_without_pagination_count
