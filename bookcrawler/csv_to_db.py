import sqlite3
import pandas as pd


class CSVToDB(object):
    def __init__(self, csv_input, db_name):
        _con = sqlite3.connect("{}.db".format(db_name))
        df = pd.read_csv(csv_input)
        df.to_sql("{}Table".format(db_name), _con)
        _con.close()
