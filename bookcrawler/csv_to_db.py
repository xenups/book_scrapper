import sqlite3
import pandas as pd
from sqlalchemy import create_engine


class CSVToDB(object):
    def __init__(self, csv_input, db_name, db_address, port, table_name):
        self._db_name = db_name
        self._db_address = db_address
        self._db_port = port
        self._csv_input = csv_input
        self._table_name = table_name

    def convert_to_postgres(self, ):
        try:
            _engine = create_engine(
                'postgresql://{}@{}:{}/{}'.format(self._db_name, self._db_address, self._db_port, self._table_name))
            df = pd.read_csv(self._csv_input)
            df.to_sql("fidibo", _engine)
        except Exception as e:
            raise e

    def convert_to_sqlite(self, ):
        _con = sqlite3.connect("{}.db".format(self._db_name))
        df = pd.read_csv(self._csv_input)
        df.to_sql("{}Table".format(self._db_name), _con)
        _con.close()
