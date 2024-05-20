from neo4j import GraphDatabase

class Neo4JService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def add_author(self, author):
        with self.driver.session() as session:
            session.write_transaction(self._create_and_return_author, author)

    @staticmethod
    def _create_and_return_author(tx, author):
        query = (
            "CREATE (a:Author {name: $name, birthdate: $birthdate}) "
            "RETURN a"
        )
        result = tx.run(query, name=author.name, birthdate=author.birthdate)
        return result.single()

    # Méthodes similaires pour la gestion des livres via Neo4J
