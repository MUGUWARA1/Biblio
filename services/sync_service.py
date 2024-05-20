class SyncService:
    def __init__(self, mongodb_service, neo4j_service):
        self.mongodb_service = mongodb_service
        self.neo4j_service = neo4j_service

    def sync_books(self):
        books = self.mongodb_service.get_books()
        for book in books:
            author = self.neo4j_service.get_author_by_id(book['author_id'])
            if not author:
                self.neo4j_service.add_author(book['author_id'])
            self.neo4j_service.add_book(book)
