class Publisher(object):
    def __init__(self):
        self.name = None
        self.link = None


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

    def list_object(self):
        return self.remove_none_objects(
            [self.title, self.author, self.publisher, self.price, self.category, self.page_number,
             self.ISBN, self.beforeOffPrice, self.physicalPrice, self.rating, self.publish_date])

    @staticmethod
    def remove_none_objects(book_objects):
        _book_objects = book_objects
        for book_object in _book_objects:
            if book_object is None:
                _book_objects.remove(book_object)
        return _book_objects
