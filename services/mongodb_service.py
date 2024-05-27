from pymongo import MongoClient

class MongoDBService:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def add_book(self, book):
        return self.db.Books.insert_one(book.__dict__)

    def get_books(self):
        return self.db["Books"].find()

    # Méthodes similaires pour membres et prêts
