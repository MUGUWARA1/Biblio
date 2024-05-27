class Book:
    def __init__(self, title, author_id, published_year, isbn):
        self.title = title
        self.author_id = author_id
        self.published_year = published_year
        self.isbn = isbn

    def to_dict(self):
        return {
            'title': self.title,
            'author_id': self.author_id,
            'published_year': self.published_year,
            'isbn': self.isbn
        }
