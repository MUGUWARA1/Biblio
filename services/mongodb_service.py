from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDBService:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_books(self):
        books_collection = self.db.books
        return list(books_collection.find())

    def add_book(self, book):
        books_collection = self.db.books
        books_collection.insert_one(book.to_dict())

    def delete_book(self, book_id):
        books_collection = self.db.books
        books_collection.delete_one({'_id': ObjectId(book_id)})
    def add_user(self, user):
        users_collection = self.db.users
        users_collection.insert_one(user.to_dict())

    def get_user(self, username):
        users_collection = self.db.users
        return users_collection.find_one({'username': username})
