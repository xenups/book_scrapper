import asyncio
import logging


def convert_object_properties_to_list(_object):
    _book_dictionary = _object.__dict__
    _book_dictionary = clean_dict_none_terms(_book_dictionary)
    _list_values = list(_book_dictionary.values())
    return _list_values


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def background(f):
    def wrapped(*args, **kwargs):
        return asyncio.get_event_loop().run_in_executor(None, f, *args, **kwargs)

    return wrapped


def initialize_logs():
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


def clean_dict_none_terms(d):
    return {
        k: v
        for k, v in d.items()
        if v is not None
    }


def open_new_tab(driver):
    driver.execute_script("window.open()")
    driver.switch_to.window(driver.window_handles[1])


def close_current_tab(driver):
    driver.execute_script("window.close()")
    driver.switch_to.window(driver.window_handles[0])


def split(arr, size):
    arrs = []
    while len(arr) > size:
        pice = arr[:size]
        arrs.append(pice)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def split_to_sublist(the_list, number_of_sublist):
    k, m = divmod(len(the_list), number_of_sublist)
    return (the_list[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(number_of_sublist))
