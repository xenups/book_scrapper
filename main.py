from fidibo.book_scrapper import BookScrapper
from fidibo.publisher_scrapper import PublisherScrapper
import requests

if __name__ == '__main__':
    # url = "https://fidibo.com/books/publisher"
    # PublisherScrapper(url=url)

    url = "https://fidibo.com/books/publisher/%D9%86%D8%B4%D8%B1-%DA%86%D8%B4%D9%85%D9%87"
    books = BookScrapper(url=url).extract_books()
    for book in books:
        print(book.author)
        print(book.title)
