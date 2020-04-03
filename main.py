from bookcrawler.util import initialize_logs
from bookstore_handler import Fidibo, Taghche, Ketabrah, Navar

if __name__ == '__main__':
    initialize_logs()
    Fidibo().crawl_by_publishers()
    # Taghche().crawl_by_publishers()
    # Taghche().crawl_by_category()
    # Ketabrah().crawl_by_category()
    # Ketabrah().crawl_by_publishers()
    # Navar().crawl_by_category()
