class Publisher(object):
    def __init__(self):
        self.name = None


class Book(object):
    def __init__(self):
        self.title = None
        self.author = None
        self.publisher = None
        self.is_free = False
        self.price = None
