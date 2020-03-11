from abc import ABC
from bookcrawler.selenium_driver import webdriver
from bookcrawler.selenium_driver import ChromeDriverManager
from fidibo.book_scrapper import BookScrapper as FidiboScrapper
from taghche.book_scrapper import BookScrapper as TaghcheScrapper
from ketabrah.book_scrapper import BookScrapper as KetabrahScrapper


class BookStore(ABC):
    def scrape_by_publishers(self):
        pass

    def scrape_by_category(self):
        pass


class Fidibo(BookStore):
    def scrape_by_publishers(self):
        web_driver = webdriver.Chrome(ChromeDriverManager().install())
        url = "https://fidibo.com/books/publisher"
        FidiboScrapper(driver=web_driver).extract_books_by_publishers(publishers_url=url)


class Taghche(BookStore):
    def scrape_by_category(self):
        taghche = TaghcheScrapper()
        taghche.set_response_count(150)
        taghche.extract_books_api_by_category(category_id=1)


class Ketabrah(BookStore):
    def scrape_by_publishers(self):
        publishers_url = "https://www.ketabrah.ir/page/publishers"
        web_driver = webdriver.Chrome(ChromeDriverManager().install())
        KetabrahScrapper(driver=web_driver).extract_books_by_publishers(publishers_url=publishers_url)

    def scrape_by_category(self):
        category_url = "https://www.ketabrah.ir/book-category/%DA%A9%D8%AA%D8%A7%D8%A8%E2%80%8C%D9%87%D8%A7%DB%8C-%D8%AD%D9%82%D9%88%D9%82/"
        web_driver = webdriver.Chrome(ChromeDriverManager().install())
        KetabrahScrapper(driver=web_driver).extract_books_by_category(category_url=category_url)
