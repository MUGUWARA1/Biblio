from flask import Flask, render_template, request, redirect, url_for
from services.mongodb_service import MongoDBService
from services.neo4j_service import Neo4JService
from services.sync_service import SyncService
from models.book import Book

app = Flask(__name__)

uri="mongodb+srv://karimderou:9CWbTbSzfoCk7g6F@cluster0.293rwjg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Configure MongoDB and Neo4J services
mongodb_service = MongoDBService(uri, db_name="NoSql")
#neo4j_service = Neo4JService(uri="bolt://localhost:7687", user="neo4j", password="password")
#sync_service = SyncService(mongodb_service, neo4j_service)

@app.route('/')
def index():
    books = mongodb_service.get_books()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author_id = request.form['author_id']
        published_year = request.form['published_year']
        isbn = request.form['isbn']
        book = Book(title, author_id, published_year, isbn)
        mongodb_service.add_book(book)
       # sync_service.sync_books()
        return redirect(url_for('index'))
    return render_template('add_book.html')

# Routes similaires pour auteurs, adhérents, et prêts

if __name__ == '__main__':
    app.run(debug=True)
    
    





