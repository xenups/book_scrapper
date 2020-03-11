import logging
import os
import sys
import json
import ijson
import requests
from furl import furl
from urllib.parse import unquote
from bookcrawler.models.model import Book, Pagination
from bookcrawler.file_handler.csv_handler import export_book_to_csv

JSON_FILE_PATH = "./taghche/data/taghche.json"
TEMPLATE_URL = "https://get.taaghche.com/v2/everything?filters={%22list%22:[{%22value%22:31,%22type%22:1},{%22type%22:3,%22value%22:-106},{%22type%22:21,%22value%22:0},{%22type%22:50,%22value%22:0}],%22refId%22:%22ff27bfa7-2166-46bf-9b2f-221ab9f18e7d.1%22}&offset=0-0-0-15&order=7"
HOST = "https://get.taaghche.com/v2/everything"


# INITIAL_OFFSET = "0-0-0-100"


class BookScrapper(object):
    def __init__(self):
        self.__remove_json_file()
        self.response_count = 100
        self.INITIAL_OFFSET = "0-0-0-100"

    def extract_books_api_by_category(self, category_id):
        __pagination = self.__get_next_offset_from_json()
        while True:
            if __pagination.hasMore:
                url = self.__generate_url_pagination_by_category(category_id, offset=__pagination.offset)
                export_book_to_csv(self.__get_books_from_api(url=url))
                __pagination = self.__get_next_offset_from_json()
            else:
                break

    def set_response_count(self, count: int):
        self.INITIAL_OFFSET = "0-0-0-" + str(count)
        self.response_count = count

    @staticmethod
    def __generate_url_pagination_by_category(category_id, offset):
        unquote_url = furl(unquote(TEMPLATE_URL))
        filters = json.loads(unquote_url.query.params["filters"])
        filters["list"][0]["value"] = str(category_id)
        category_filter = json.dumps(filters)
        paginated_furl = furl(unquote(HOST)).add(args={'filters': category_filter, 'offset': offset})
        return paginated_furl.url

    def __get_books_from_api(self, url):
        logging.info("API Called")
        r = requests.get(url)
        r.encoding = 'UTF-8'
        self.__save_json_to_file(r.json(), JSON_FILE_PATH)

        with open(JSON_FILE_PATH, encoding='utf-8-sig') as input_file:
            logging.info('reading from json file')
            json_books = ijson.items(input_file, "bookList.books.item")
            books = []
            for book in json_books:
                book_instance = Book()
                book_instance.title = book["title"]
                book_instance.page_number = book["numberOfPages"]
                book_instance.price = book["price"]
                book_instance.publisher = book["publisher"]
                book_instance.author = self.convert_authors_to_string(book["authors"])
                book_instance.category = self.convert_categories_to_string(book["categories"])
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
    def convert_categories_to_string(list_categories):
        category_name = " "
        for category_index in range(list_categories.__len__()):
            category = list_categories[category_index]
            category_name = category_name + str(category["title"]) + " "
        return category_name

    @staticmethod
    def change_offset_lentgh(offset, length=20):
        _custom_offset = offset.split('-')
        _custom_offset[-1] = str(length)
        _offset = '-'.join(_custom_offset)
        logging.info(offset)
        return _offset

    def __get_next_offset_from_json(self, ):
        try:
            with open(JSON_FILE_PATH, encoding='utf-8-sig') as input_file:
                json_object = json.load(input_file)
                pagination = Pagination()
                pagination.hasMore = json_object["hasMore"]
                pagination.offset = self.change_offset_lentgh(json_object["nextOffset"], self.response_count)
                return pagination
        except Exception as error:
            pagination = Pagination()
            pagination.hasMore = True
            pagination.offset = self.INITIAL_OFFSET
            return pagination

    @staticmethod
    def __save_json_to_file(json_object, file_name):
        try:
            with open(file_name, 'w') as json_file:
                json.dump(json_object, json_file)
        except Exception as error:
            logging.error("JSON could not save")
            raise error

    @staticmethod
    def __remove_json_file():
        if os.path.exists(JSON_FILE_PATH):
            os.remove(JSON_FILE_PATH)
