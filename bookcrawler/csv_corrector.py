from abc import ABC
import pandas as pd


class CSVCorrectorAbstract(ABC):
    def __init__(self, file_path):
        self._data_frame = pd.read_csv(file_path, skipinitialspace=True)

    def remove_blank_columns(self):
        # self._data_frame = self._data_frame[self._data_frame.columns.dropna()]
        self._data_frame.dropna(how='all', axis=1, inplace=True)
        self._data_frame.to_csv('ketabrah.csv', encoding='utf-8', index=False)

    def add_store_name(self):
        pass

    def convert_price(self):
        pass

    def remove_duplicate_lines(self):
        self._data_frame.drop_duplicates(inplace=True)
        self._data_frame.to_csv('ketabrah.csv')


class NavarCSVCorrector(CSVCorrectorAbstract):
    def convert_price(self):
        pass


class KetabrahCSVCorrector(CSVCorrectorAbstract):
    def convert_price(self):
        self._data_frame['price'].fillna(0, inplace=True)
        self._data_frame['price'] = self._data_frame['price'].astype(str).str.replace(r'\D+', '').astype(float)
        self._data_frame.to_csv('ketabrah.csv', index=False)
