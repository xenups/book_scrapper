from bookcrawler.util import initial_logs, split_to_sublist
from bookstore_handler import Fidibo, Taghche, Ketabrah, Navar

if __name__ == '__main__':
    initial_logs()

    Fidibo().scrape_by_publishers()
    # Taghche().scrape_by_category()
    # Ketabrah().scrape_by_publishers()
    # Navar().scrape_by_category()

