import logging
from csv import writer


def export_book_to_csv(books, file_name="books"):
    csv_write = writer(open(file_name + ".csv", 'a'))
    for book in books:
        csv_write.writerow(book.list_object())
        logging.info(book.title)
