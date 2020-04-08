import time
import bottle
import logging
import schedule
from pubsub import pub
from bottle import route, run
from bookcrawler.util import initialize_logs
from multiprocessing import Process, Queue, Value
from bookstore_handler import Fidibo, Taghche, Ketabrah, Navar


class WebAPI(object):
    def __init__(self):
        self.q = None
        _last_message = ""

    def status(self, ):
        if not q.empty():
            self._last_message = str(q.get())
            return self._last_message
        else:
            return "nothing new " + self._last_message

    def runserver(self, q):
        bottle.route("/status")(self.status)
        run(host='localhost', port=8080, debug=True)


def listener(message):
    q.put(message)


def crawling():
    try:
        Taghche().crawl_by_category()
        Ketabrah().crawl_by_publishers()
        Navar().crawl_by_category()
        Fidibo().crawl_by_publishers()
    except Exception as ex:
        logging.error(ex)


def scheduler():
    # schedule.every().minute.do(crawling)
    schedule.every().thursday.at("04:00").do(crawling)
    pub.sendMessage('server_status', message="Wait for crawling...")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    initialize_logs()
    pub.subscribe(listener, 'server_status')
    q = Queue()
    server_process = Process(target=WebAPI().runserver, args=(q,))
    server_process.start()
    scheduler()
