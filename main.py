import logging
import time
import schedule
from bookcrawler.util import initialize_logs
from bookstore_handler import Fidibo, Taghche, Ketabrah, Navar


def crawling():
    try:
        Fidibo().crawl_by_publishers()
        Taghche().crawl_by_category()
        Ketabrah().crawl_by_publishers()
        Navar().crawl_by_category()
    except Exception as ex:
        logging.error(ex)


if __name__ == '__main__':
    initialize_logs()
    schedule.every(1).minutes.do(crawling)
    while True:
        schedule.run_pending()
        time.sleep(1)
