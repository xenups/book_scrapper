import logging
from abc import ABC
from pyvirtualdisplay import Display
from bookcrawler.csv_to_db import CSVToDB
from bookcrawler.csv_corrector import CSVCorrectorFactory
from navar.book_scrapper import BookScrapper as NavarScrapper
from fidibo.book_scrapper import BookScrapper as FidiboScrapper
from taghche.book_scrapper import BookScrapper as TaghcheScrapper
from ketabrah.book_scrapper import BookScrapper as KetabrahScrapper
from settings import fidibo_worker, taghche_response_count


class BookStore(ABC):
    def __init__(self):
        self.display = Display(visible=1, size=(800, 600))

    def crawl_by_publishers(self):
        pass

    def crawl_by_category(self):
        pass


class Fidibo(BookStore):
    def crawl_by_publishers(self):
        self.display.start()
        csv_path = FidiboScrapper(without_browser=False).multi_book_extractor_by_publishers_url(
            worker=int(fidibo_worker))
        cleaned_data = CSVCorrectorFactory().correct_data("FidiboCorrector", csv_path)
        CSVToDB(csv_input=cleaned_data, table_name="fidibo_test").convert_to_postgres()
        logging.info("Task successfully finished ...")
        self.display.stop()

    def __del__(self):
        self.display.stop()


class Taghche(BookStore):
    def crawl_by_category(self):
        self.display.stop()
        taghche = TaghcheScrapper()
        taghche.set_response_count(int(taghche_response_count))
        csv_path = taghche.extract_books_api_by_category(category_id=1)
        cleaned_data = CSVCorrectorFactory().correct_data("TaghcheCorrector", csv_path)


class Ketabrah(BookStore):
    def crawl_by_publishers(self):
        self.display.start()
        csv_path = KetabrahScrapper(without_browser=False, optimized_mode=True).extract_books_by_publishers()
        cleaned_data = CSVCorrectorFactory().correct_data("KetabrahCorrector", csv_path)
        CSVToDB(csv_input=cleaned_data, table_name="ketabrah")
        self.display.stop()

    def crawl_by_category(self):
        self.display.start()
        csv_path = KetabrahScrapper(without_browser=False, optimized_mode=True).extract_books_by_category()
        cleaned_data = CSVCorrectorFactory().correct_data("KetabrahCorrector", csv_path)
        self.display.stop()

    def __del__(self):
        self.display.stop()


class Navar(BookStore):
    def crawl_by_category(self):
        self.display.start()
        navar = NavarScrapper(optimized_mode=False, without_browser=False)
        csv_path = navar.extract_books()
        cleaned_data = CSVCorrectorFactory().correct_data("NavarCorrector", csv_path)
        self.display.stop()

    def __del__(self):
        self.display.stop()
