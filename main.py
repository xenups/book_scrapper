import time
import logging
import schedule
from bookcrawler.util import initialize_logs
from bookstore_handler import Fidibo, Taghche, Ketabrah, Navar


def crawling():
    try:
        Taghche().crawl_by_category()
        Ketabrah().crawl_by_publishers()
        Navar().crawl_by_category()
        Fidibo().crawl_by_publishers()
    except Exception as ex:
        logging.error(ex)


if __name__ == '__main__':
    initialize_logs()
    schedule.every().thursday.at("04:00").do(crawling)
    while True:
        schedule.run_pending()
        time.sleep(1)
