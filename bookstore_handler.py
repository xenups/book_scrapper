import subprocess
from abc import ABC

from bookcrawler.csv_corrector import FidiboCSVCorrector, TaghcheCSVCorrector, KetabrahCSVCorrector, NavarCSVCorrector
from bookcrawler.csv_to_db import CSVToDB
from bookcrawler.selenium_driver import SeleniumDriver
from fidibo.book_scrapper import BookScrapper as FidiboScrapper
from taghche.book_scrapper import BookScrapper as TaghcheScrapper
from ketabrah.book_scrapper import BookScrapper as KetabrahScrapper
from navar.book_scrapper import BookScrapper as NavarScrapper


class BookStore(ABC):
    def scrape_by_publishers(self):
        pass

    def scrape_by_category(self):
        pass


class Fidibo(BookStore):
    def scrape_by_publishers(self):
        url = "https://fidibo.com/books/publisher"
        fidibo_csv_file = FidiboScrapper(without_browser=False).multi_book_extractor_by_publishers_url(
            publishers_url=url,
            worker=2)
        cleaned_data = FidiboCSVCorrector(fidibo_csv_file).correct_data()


class Taghche(BookStore):
    def scrape_by_category(self):
        taghche = TaghcheScrapper()
        taghche.set_response_count(150)
        taghche_csv_path = taghche.extract_books_api_by_category(category_id=1)
        cleaned_data = TaghcheCSVCorrector(taghche_csv_path).correct_data()


class Ketabrah(BookStore):
    def scrape_by_publishers(self):
        publishers_url = "https://www.ketabrah.ir/page/publishers"
        driver = SeleniumDriver()
        csv_path = KetabrahScrapper(without_browser=False, optimized_mode=True).extract_books_by_publishers(
            publishers_url=publishers_url)
        cleaned_data = KetabrahCSVCorrector(csv_path).correct_data()

    def scrape_by_category(self):
        category_url = "https://www.ketabrah.ir/book-category/%DA%A9%D8%AA%D8%A7%D8%A8%E2%80%8C%D9%87%D8%A7%DB%8C-%D8%AD%D9%82%D9%88%D9%82/"
        csv_path = KetabrahScrapper(without_browser=False, optimized_mode=True).extract_books_by_category(
            category_url=category_url)
        cleaned_data = KetabrahCSVCorrector(csv_path).correct_data()


class Navar(BookStore):
    def scrape_by_category(self):
        navar = NavarScrapper(optimized_mode=False, without_browser=False)
        csv_path = navar.extract_books()
        cleaned_data = NavarCSVCorrector(csv_path).correct_data()
