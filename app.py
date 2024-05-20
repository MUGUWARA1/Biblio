from flask import Flask, render_template, request, redirect, url_for
from services.mongodb_service import MongoDBService
from services.neo4j_service import Neo4JService
from services.sync_service import SyncService
from models.book import Book
from models.author import Author
from models.member import Member
from models.loan import Loan

app = Flask(__name__)

# Configure MongoDB and Neo4J services
mongodb_service = MongoDBService(uri="mongodb://localhost:27017", db_name="library")
neo4j_service = Neo4JService(uri="bolt://localhost:7687", user="neo4j", password="password")
sync_service = SyncService(mongodb_service, neo4j_service)

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
        sync_service.sync_books()
        return redirect(url_for('index'))
    return render_template('add_book.html')

# Routes similaires pour auteurs, adhérents, et prêts

if __name__ == '__main__':
    app.run(debug=True)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# Routes et logiques pour inscription, connexion, et déconnexion

@login_manager.user_loader
def load_user(user_id):
    user_data = mongodb_service.get_user_by_id(user_id)
    return User(user_data['_id'], user_data['username'], user_data['password']) if user_data else None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = mongodb_service.get_user_by_username(username)
        if user_data and user_data['password'] == password:
            user = User(user_data['_id'], user_data['username'], user_data['password'])
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))