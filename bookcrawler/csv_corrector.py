from abc import ABC
import pandas as pd


class CSVCorrectorAbstract(ABC):
    def __init__(self, file_path):
        self._data_frame = pd.read_csv(file_path, skipinitialspace=True)

    def drop_blank_columns(self):
        self._data_frame.dropna(how='all', axis=1, inplace=True)

    def clean_price(self):
        self._data_frame['price'].fillna(0, inplace=True)
        self._data_frame['price'] = self._data_frame['price'].astype(str).str.replace(r'\D+', '').astype(float)

    def drop_column(self, column_name: str):
        self._data_frame.drop(column_name, axis=1, inplace=True)

    def remove_duplicate_lines(self):
        self._data_frame.drop_duplicates(inplace=True)

    def export_to_csv(self, file_name="output"):
        self._data_frame.to_csv(file_name, index=False, encoding='utf-8')

    def correct_data(self):
        pass


class NavarCSVCorrector(CSVCorrectorAbstract):
    def correct_data(self):
        self.drop_blank_columns()
        self.remove_duplicate_lines()
        self.clean_price()
        self.export_to_csv("cleaned_navar.csv")


class KetabrahCSVCorrector(CSVCorrectorAbstract):
    def correct_data(self):
        self.drop_blank_columns()
        self.remove_duplicate_lines()
        self.clean_price()
        self.export_to_csv("cleaned_ketabrah.csv")


class TaghcheCSVCorrector(CSVCorrectorAbstract):
    def correct_data(self):
        self.drop_blank_columns()
        self.remove_duplicate_lines()
        self.export_to_csv("cleaned_taghche.csv")


class FidiboCSVCorrector(CSVCorrectorAbstract):
    def correct_data(self):
        self.drop_blank_columns()
        self.drop_column("url")
        self.remove_duplicate_lines()
        self.clean_price()
        self.export_to_csv("cleaned_fidibo.csv")
