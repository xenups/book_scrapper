import logging
import sqlite3
import pandas as pd
from settings import database
from sqlalchemy import create_engine


class CSVToDB(object):
    def __init__(self, csv_input, table_name):
        logging.info("Converting CSV To Database ...")
        self._db_name = database["db_name"]
        self._db_user = database["db_user"]
        self._db_pass = database["db_pass"]
        self._db_host = database["db_host"]
        self._db_port = database["db_port"]
        self._csv_input = csv_input
        self._table_name = table_name

    def convert_to_postgres(self, ):
        try:
            _engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(self._db_user, self._db_pass,
                                                                         self._db_host, self._db_port,
                                                                         self._db_name))
            df = pd.read_csv(self._csv_input)
            df.to_sql(self._table_name, _engine, if_exists="replace")
        except Exception as e:
            logging.error("Database  error")
            raise e

    def convert_to_sqlite(self, ):
        _con = sqlite3.connect("{}.db".format(self._db_name))
        df = pd.read_csv(self._csv_input)
        df.to_sql("{}Table".format(self._db_name), _con)
        _con.close()
