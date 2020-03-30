import json
import os
import ijson
import logging
import requests
from furl import furl
from urllib.parse import unquote
import xml.etree.ElementTree as ET
from bookcrawler.models.model import Book, Pagination
from selenium.webdriver.chrome.webdriver import WebDriver
from bookcrawler.file_handler.csv_handler import CSVHandler

JSON_FILE_PATH = "./navar/data/navar.json"
TEMPLATE_URL = "https://www.navaar.ir/api/audiobooks/genre/3/?$inlinecount=allpages"
WEBSITE = "https://www.navaar.ir/catalog/genre/2/%D8%AF%D8%A7%D8%B3%D8%AA%D8%A7%D9%86-%D9%88-%D8%B1%D9%85%D8%A7%D9%86-%D8%AE%D8%A7%D8%B1%D8%AC%DB%8C"


class BookScrapper(object):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.csv_handler = CSVHandler()

    def __scrape_genres_urls(self):
        self.driver.get(url=WEBSITE)
        menu_items = self.driver.find_element_by_class_name("side-nav")
        items = menu_items.find_elements_by_xpath(".//a[@href]")
        _list_genres = []
        for item in items:
            if "genre" in item.get_attribute("href"):
                _list_genres.append(item.get_attribute("href"))

        _list_genres_without_duplication = list(set(_list_genres))
        self.driver.close()
        return _list_genres_without_duplication

    def __extract_genres_id(self):
        genre_urls = self.__scrape_genres_urls()
        genres = []
        for url in genre_urls:
            unquote_url = furl(unquote(url))
            "segment 2 belong to category"
            genres.append(unquote_url.path.segments[2])
        return genres

    def extract_books(self):
        genres_id = self.__extract_genres_id()
        genres_id.sort()
        for id in genres_id:
            self.extract_books_api_by_category(id)

    def extract_books_api_by_category(self, category_id):
        category_url = self.__generate_category_url(category_id)
        books = self.__get_books_from_api(category_url)
        self.csv_handler.export_book_to_csv(books, file_name="navar")

    def __get_books_from_api(self, category_url):
        logging.info("API CALLED")
        self.__remove_json_file()
        pagination = self.__get_next_offset_from_json()
        url = category_url
        logging.info(pagination.offset)
        list_books = []
        while pagination.hasMore:
            response = requests.get(url)
            response.encoding = 'UTF-8'
            logging.info(pagination.offset)
            self.__save_json_to_file(response.json(), JSON_FILE_PATH)
            pagination = self.__get_next_offset_from_json()
            url = pagination.offset
            books = self.__extract_books_from_json()
            list_books.extend(books)
        return list_books

    def __extract_books_from_json(self):
        with open(JSON_FILE_PATH, encoding='utf-8-sig') as input_file:
            logging.info('reading from json file')
            parser = ijson.parse(input_file)
            books = []
            __found_book = False
            for prefix, event, value in parser:
                if prefix == "items.item.title":
                    __found_book = True
                    book = Book()
                    book.title = value
                    book.author = " "
                    book.publisher = " "
                    logging.info(book.title)
                if prefix == "items.item.products.item.price":
                    book.price = value
                if prefix == "items.item.authors.item.firstName":
                    book.author = value
                if prefix == "items.item.authors.item.lastName":
                    book.author = str(book.author) + " " + value
                if prefix == "items.item.audioPublisherTitle":
                    book.publisher = value
                if __found_book:
                    __found_book = False
                    books.append(book)

            return books

    @staticmethod
    def __parse_xml(response):
        try:

            root_namespace = "{http://schemas.datacontract.org/2004/07/System.Web.Http.OData}"
            item_namespace = "{http://schemas.datacontract.org/2004/07/Navaar.Data}"
            print(1)

            root = ET.fromstring(response.data)
            url = root.find(root_namespace + "NextPageLink").text
            print(url)
            # print(root.getchildren())

            items = root.find(root_namespace + "Items").getchildren()
            for item in items:
                book = Book()
                # print(item.getchildren())
                book.publisher = item.find(item_namespace + "AudioPublisherTitle").text
                book.title = item.find(item_namespace + "Title").text
                products = item.find(item_namespace + 'Products')
                for product in products:
                    book.price = product.find(item_namespace + "Price").text
                authors = item.find(item_namespace + "Authors")
                for author in authors:
                    book.author = author.find(item_namespace + "FirstName").text + " " + author.find(
                        item_namespace + "LastName").text
        except Exception as e:
            print(getattr(e, 'message', repr(e)))

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

    @staticmethod
    def __get_next_offset_from_json():
        try:
            with open(JSON_FILE_PATH, encoding='utf-8-sig') as input_file:
                json_object = json.load(input_file)
                pagination = Pagination()
                pagination.offset = json_object["nextPageLink"]
                if pagination.offset is not None:
                    pagination.hasMore = True
                else:
                    pagination.hasMore = False
                return pagination
        except Exception:
            pagination = Pagination()
            pagination.offset = " "
            pagination.hasMore = True
            return pagination

    @staticmethod
    def __generate_category_url(category_id):
        unquote_url = furl(unquote(TEMPLATE_URL))
        "segment 3 belong to category"
        unquote_url.path.segments[3] = str(category_id)
        return unquote_url.url
