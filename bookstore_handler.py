from abc import ABC
from bookcrawler.csv_corrector import CSVCorrectorFactory
from fidibo.book_scrapper import BookScrapper as FidiboScrapper
from taghche.book_scrapper import BookScrapper as TaghcheScrapper
from ketabrah.book_scrapper import BookScrapper as KetabrahScrapper
from navar.book_scrapper import BookScrapper as NavarScrapper


class BookStore(ABC):
    def crawl_by_publishers(self):
        pass

    def crawl_by_category(self):
        pass


class Fidibo(BookStore):
    def crawl_by_publishers(self):
        url = "https://fidibo.com/books/publisher"
        csv_path = FidiboScrapper(without_browser=False).multi_book_extractor_by_publishers_url(
            publishers_url=url,
            worker=2)
        cleaned_data = CSVCorrectorFactory().correct_data("FidiboCorrector", csv_path)


class Taghche(BookStore):
    def crawl_by_category(self):
        taghche = TaghcheScrapper()
        taghche.set_response_count(150)
        csv_path = taghche.extract_books_api_by_category(category_id=1)
        cleaned_data = CSVCorrectorFactory().correct_data("TaghcheCorrector", csv_path)


class Ketabrah(BookStore):
    def crawl_by_publishers(self):
        publishers_url = "https://www.ketabrah.ir/page/publishers"
        csv_path = KetabrahScrapper(without_browser=False, optimized_mode=True).extract_books_by_publishers(
            publishers_url=publishers_url)
        cleaned_data = CSVCorrectorFactory().correct_data("KetabrahCorrector", csv_path)

    def crawl_by_category(self):
        category_url = "https://www.ketabrah.ir/book-category/%DA%A9%D8%AA%D8%A7%D8%A8%E2%80%8C%D9%87%D8%A7%DB%8C-%D8%AD%D9%82%D9%88%D9%82/"
        csv_path = KetabrahScrapper(without_browser=False, optimized_mode=True).extract_books_by_category(
            category_url=category_url)
        cleaned_data = CSVCorrectorFactory().correct_data("KetabrahCorrector", csv_path)


class Navar(BookStore):
    def crawl_by_category(self):
        navar = NavarScrapper(optimized_mode=False, without_browser=False)
        csv_path = navar.extract_books()
        cleaned_data = CSVCorrectorFactory().correct_data("NavarCorrector", csv_path)
