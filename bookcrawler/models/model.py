class Pagination(object):
    def __init__(self):
        self.offset = None
        self.hasMore = None


class Category(object):
    def __init__(self):
        self.url = None
        self.title = None


class Publisher(object):
    def __init__(self):
        self.name = None
        self.url = None


class Book(object):
    def __init__(self):
        self.title = None
        self.author = None
        self.publisher = None
        self.price = None
        self.category = None
        self.page_number = None
        self.ISBN = None
        self.beforeOffPrice = None
        self.physicalPrice = None
        self.rating = None
        self.publish_date = None
        self.url = None
