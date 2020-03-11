import logging

from bookcrawler.util import initial_logs
from bookstore_handler import Fidibo, Taghche, Ketabrah

if __name__ == '__main__':
    initial_logs()

    # Fidibo().scrape_by_category()
    # Taghche().scrape_by_category()
    Ketabrah().scrape_by_publishers()
