import json
import os
import time
from time import sleep

import ijson
import requests
from furl import furl
from urllib.parse import unquote

from bookcrawler.file_handler.csv_handler import export_book_to_csv
from bookcrawler.models.model import Book
from taghche.models.model import Pagination

JSON_FILE_PATH = "./taghche/data/taghche.json"
TEMPLATE_URL = "https://get.taaghche.com/v2/everything?filters={%22list%22:[{%22value%22:31,%22type%22:1},{%22type%22:3,%22value%22:-106},{%22type%22:21,%22value%22:0},{%22type%22:50,%22value%22:0}],%22refId%22:%22ff27bfa7-2166-46bf-9b2f-221ab9f18e7d.1%22}&offset=0-0-0-15&order=7"
HOST = "https://get.taaghche.com/v2/everything"
INITIAL_OFFSET = "0-0-0-5000"


class BookScrapper(object):
    def __init__(self, category_id):
        self.category_id = category_id

        self.__remove_json_file()
        self.url = self.__generate_url_by_category(category_id=category_id, offset=INITIAL_OFFSET)

    def extract_books(self):
        export_book_to_csv(self.__get_books_from_api(self.url))
        __pagination = self.__get_next_offset_from_json()

        if __pagination.hasMore:
            self.url = self.__generate_url_by_category(self.category_id, offset=__pagination.offset)
            self.extract_books()

    @staticmethod
    def __generate_url_by_category(category_id, offset):
        unquote_url = furl(unquote(TEMPLATE_URL))
        filters = json.loads(unquote_url.query.params["filters"])
        filters["list"][0]["value"] = category_id
        category_filter = json.dumps(filters)
        url = furl(unquote(HOST)).add(args={'filters': category_filter, 'offset': offset})
        return url

    def __get_books_from_api(self, url):
        print("api called")
        r = requests.get(url)
        print(url)
        r.encoding = 'UTF-8'
        self.__save_json_to_file(r.json(), JSON_FILE_PATH)

        with open(JSON_FILE_PATH, encoding='utf-8-sig') as input_file:
            print("json file started")
            json_books = ijson.items(input_file, "bookList.books.item")
            books = []
            for book in json_books:
                book_instance = Book()
                book_instance.title = book["title"]
                book_instance.page_number = book["numberOfPages"]
                book_instance.price = book["price"]
                book_instance.publisher = book["publisher"]
                book_instance.author = self.convert_authors_to_string(book["authors"])
                # book_instance.beforeOffPrice = book["beforeOffPrice"]
                # book_instance.rating = book["rating"]
                # book_instance.physicalPrice = book["PhysicalPrice"]
                # book_instance.publish_date = book["publishDate"]
                books.append(book_instance)
        return books

    @staticmethod
    def convert_authors_to_string(list_authors):
        authors_name = " "
        for author_index in range(list_authors.__len__()):
            author = list_authors[author_index]
            authors_name = authors_name + str(author["firstName"]) + " " + str(author["lastName"]) + " "
        return authors_name

    @staticmethod
    def __get_next_offset_from_json():
        try:
            with open(JSON_FILE_PATH, encoding='utf-8-sig') as input_file:
                json_object = json.load(input_file)
                pagination = Pagination()
                pagination.hasMore = json_object["hasMore"]
                pagination.offset = json_object["nextOffset"]
                return pagination
        except Exception as error:
            pagination = Pagination()
            pagination.hasMore = True
            pagination.offset = INITIAL_OFFSET
            return pagination

    @staticmethod
    def __save_json_to_file(json_object, file_name):
        try:
            with open(file_name, 'w') as json_file:
                json.dump(json_object, json_file)
        except Exception as error:
            raise error

    @staticmethod
    def __remove_json_file():
        if os.path.exists(JSON_FILE_PATH):
            os.remove(JSON_FILE_PATH)
