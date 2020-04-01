import logging
import os
from csv import writer
import pandas as pd

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

    def join_csv_files(self, file_names, out_put="out_put.csv"):
        try:
            combined_csv = pd.concat([pd.read_csv(f) for f in file_names], sort=True)
            combined_csv.to_csv(out_put, index=False, encoding='utf-8-sig')
            return out_put
        except Exception as e:
            raise e

    @staticmethod
    def remove_files(files_path: []) -> bool:
        try:
            for path in files_path:
                if os.path.exists(path):
                    os.remove(path)
            return True
        except Exception as e:
            logging.info(getattr(e, 'message', repr(e)))
            return False
