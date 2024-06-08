from flask import Flask, render_template, request, redirect, url_for, session, flash
from services.mongodb_service import MongoDBService
from models.book import Book
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB connection URI
#put your uri


# Configure MongoDB service
mongodb_service = MongoDBService(uri, db_name="NoSql")

@app.route('/')
def index():
    if 'username' in session:
        books = mongodb_service.get_books()
        return render_template('index.html', books=books)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongodb_service.get_user(username)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        user = User(username, password)
        mongodb_service.add_user(user)
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            author_id = request.form['author_id']
            published_year = request.form['published_year']
            isbn = request.form['isbn']
            book = Book(title, author_id, published_year, isbn)
            mongodb_service.add_book(book)
            return redirect(url_for('index'))
        return render_template('add_book.html')
    else:
        return redirect(url_for('login'))

@app.route('/delete_book/<book_id>', methods=['POST'])
def delete_book(book_id):
    if 'username' in session:
        mongodb_service.delete_book(book_id)
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
