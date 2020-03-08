from fidibo.book_scrapper import BookScrapper
from fidibo.publisher_scrapper import PublisherScrapper
import requests
from selenium_driver import ChromeDriverManager
from selenium_driver import webdriver

if __name__ == '__main__':
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = "https://fidibo.com/books/publisher"
    publishers = PublisherScrapper(url=url, driver=driver).extract_publishers()

    for publisher in publishers:
        print(publisher.name)
        books = BookScrapper(url=publisher.link, driver=driver).extract_books()
        for book in books:
            print(book.author)
            print(book.title)

    # url = "https://fidibo.com/books/publisher/%D9%86%D8%B4%D8%B1-%DA%86%D8%B4%D9%85%D9%87"
