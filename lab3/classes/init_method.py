class Book:
    def __init__(self, title, author="Unknown"):
        self.title = title
        self.author = author

b = Book("Kazakh Literature")
print(b.title, b.author)
