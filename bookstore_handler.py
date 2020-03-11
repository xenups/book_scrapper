from abc import ABC
from fidibo.book_scrapper import BookScrapper as FidiboScrapper
from bookcrawler.selenium_driver import webdriver
from bookcrawler.selenium_driver import ChromeDriverManager
from taghche.book_scrapper import BookScrapper as TaghcheScrapper
from ketabrah.book_scrapper import BookScrapper as KetabrahScrapper
from bookcrawler.file_handler.csv_handler import export_book_to_csv


class BookStore(ABC):
    def scrape_by_publishers(self):
        pass

    def scrape_by_category(self):
        pass


class Fidibo(BookStore):
    def scrape_by_publishers(self):
        web_driver = webdriver.Chrome(ChromeDriverManager().install())
        publishers_url = "https://fidibo.com/books/publisher"
        FidiboScrapper(driver=web_driver).extract_books_by_publishers(publishers_url=publishers_url)


class Taghche(BookStore):
    def scrape_by_category(self):
        TaghcheScrapper(category_id=1).extract_books_by_category()


class Ketabrah(BookStore):
    def scrape_by_publishers(self):
        publishers_url = "https://www.ketabrah.ir/page/publishers"
        web_driver = webdriver.Chrome(ChromeDriverManager().install())
        KetabrahScrapper(driver=web_driver).extract_by_publishers(publishers_url=publishers_url)

    def scrape_by_category(self):
        category_url = "https://www.ketabrah.ir/book-category/%DA%A9%D8%AA%D8%A7%D8%A8%E2%80%8C%D9%87%D8%A7%DB%8C-%D8%AD%D9%82%D9%88%D9%82/"
        web_driver = webdriver.Chrome(ChromeDriverManager().install())
        KetabrahScrapper(driver=web_driver).extract_by_category(category_url=category_url)
