import logging
from abc import ABC
from pyvirtualdisplay import Display
from bookcrawler.csv_to_db import CSVToDB
from bookcrawler.csv_corrector import CSVCorrectorFactory
from bookcrawler.util import clean_csv_files
from navar.book_scrapper import BookScrapper as NavarScrapper
from fidibo.book_scrapper import BookScrapper as FidiboScrapper
from taghche.book_scrapper import BookScrapper as TaghcheScrapper
from ketabrah.book_scrapper import BookScrapper as KetabrahScrapper
from settings import fidibo_worker, taghche_response_count, display_visibility


class BookStore(ABC):
    def __init__(self):
        clean_csv_files()

    def crawl_by_publishers(self):
        pass

    def crawl_by_category(self):
        pass


class Fidibo(BookStore):
    def crawl_by_publishers(self):
        csv_path = FidiboScrapper(without_browser=True).multi_book_extractor_by_publishers_url(
            worker=int(fidibo_worker))
        cleaned_data = CSVCorrectorFactory().correct_data("FidiboCorrector", csv_path)
        CSVToDB(csv_input=cleaned_data, table_name="fidibo").convert_to_postgres()
        logging.info("Task successfully finished ...")


class Taghche(BookStore):
    def crawl_by_category(self):
        taghche = TaghcheScrapper()
        taghche.set_response_count(int(taghche_response_count))
        csv_path = taghche.extract_books_api_by_category(category_id=1)
        # csv_path = taghche.extract_books_api_by_category(category_id=115)
        cleaned_data = CSVCorrectorFactory().correct_data("TaghcheCorrector", csv_path)
        CSVToDB(csv_input=cleaned_data, table_name="taghche").convert_to_postgres()
        logging.info("Task successfully finished ...")


class Ketabrah(BookStore):
    def crawl_by_publishers(self):
        csv_path = KetabrahScrapper(without_browser=True, optimized_mode=True).extract_books_by_publishers()
        cleaned_data = CSVCorrectorFactory().correct_data("KetabrahCorrector", csv_path)
        CSVToDB(csv_input=cleaned_data, table_name="ketabrah").convert_to_postgres()
        logging.info("Task successfully finished ...")

    def crawl_by_category(self):
        csv_path = KetabrahScrapper(without_browser=True, optimized_mode=True).extract_books_by_category()
        cleaned_data = CSVCorrectorFactory().correct_data("KetabrahCorrector", csv_path)
        CSVToDB(csv_input=cleaned_data, table_name="ketabrah_by_category").convert_to_postgres()
        logging.info("Task successfully finished ...")


class Navar(BookStore):
    def crawl_by_category(self):
        navar = NavarScrapper(optimized_mode=True, without_browser=True)
        csv_path = navar.extract_books()
        cleaned_data = CSVCorrectorFactory().correct_data("NavarCorrector", csv_path)
        CSVToDB(csv_input=cleaned_data, table_name="navar").convert_to_postgres()
        logging.info("Task successfully finished ...")
