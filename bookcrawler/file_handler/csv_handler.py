import logging
from csv import writer


def export_book_to_csv(books):
    csv_write = writer(open("books.csv", 'a'))
    for book in books:
        csv_write.writerow(book.list_object())
        logging.info(book.title)
