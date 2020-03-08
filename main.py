from fidibo.book_scrapper import BookScrapper
from fidibo.publisher_scrapper import PublisherScrapper

from file_handler.csv_handler import export_book_to_csv
from selenium_driver import ChromeDriverManager
from selenium_driver import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome(ChromeDriverManager().install())

    url = "https://fidibo.com/books/publisher"
    publishers = PublisherScrapper(url=url, driver=driver).extract_publishers()

    for publisher in publishers:
        books = BookScrapper(url=publisher.link, publisher_name=publisher.name, driver=driver).extract_books()
        export_book_to_csv(books=books)
