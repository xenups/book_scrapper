import logging
from csv import writer

from bookcrawler.util import clean_dict_none_terms, convert_object_properties_to_list


class CSVHandler(object):
    def __init__(self, ):
        self._csv_has_title = False

    def _set_csv_title(self, file_name, book):
        if not self._csv_has_title:
            csv_write = writer(open(file_name + ".csv", 'a'))
            book_dictionary = book.__dict__
            clear_book_dictionary = clean_dict_none_terms(book_dictionary)
            titles = list(clear_book_dictionary.keys())
            csv_write.writerow(titles)
            self._csv_has_title = True
            return True
        return False

    def export_book_to_csv(self, books, file_name="books"):
        self._set_csv_title(file_name=file_name, book=books[0])
        _csv_write = writer(open(file_name + ".csv", 'a'))
        for book in books:
            _csv_write.writerow(convert_object_properties_to_list(book))
            logging.info(book.title)
