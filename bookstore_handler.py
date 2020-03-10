from fidibo.book_scrapper import BookScrapper
from fidibo.publisher_scrapper import PublisherScrapper

from bookcrawler.file_handler.csv_handler import export_book_to_csv
from bookcrawler.selenium_driver import ChromeDriverManager
from bookcrawler.selenium_driver import webdriver
from abc import ABC

from taghche.book_scrapper import BookScrapper as TaghcheScrapper


class BookStore(ABC):
    def scrape(self):
        pass


class Fidibo(BookStore):
    def scrape(self):
        web_driver = webdriver.Chrome(ChromeDriverManager().install())
        print("hi2")
        url = "https://fidibo.com/books/publisher"
        publishers = PublisherScrapper(url=url, driver=web_driver).extract_publishers_by_web()

        for publisher in publishers:
            books = BookScrapper(url=publisher.link, publisher_name=publisher.name,
                                 driver=web_driver).extract_books_by_web()
            export_book_to_csv(books=books)


class Taghche(BookStore):
    def scrape(self):
        TaghcheScrapper(category_id=1).extract_books()
