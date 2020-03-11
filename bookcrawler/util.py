import sys
import logging


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def initial_logs():
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    root_logger = logging.getLogger()

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)

    file_handler = logging.FileHandler(filename='mylog.log', mode='a')
    file_handler.setLevel(level=logging.ERROR)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(level=logging.INFO)
    # file_handler.setLevel(level=logging.ERROR)
