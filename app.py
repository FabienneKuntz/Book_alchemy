from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/')
def home():
    sort = request.args.get("sort", "title")
    query = request.args.get("q")

    books_query = Book.query.join(Author)

    if query:
        books_query = books_query.filter(Book.title.ilike(f"%{query}%"))

    if sort == "author":
        books = books_query.order_by(Author.name).all()
    else:
        books = books_query.order_by(Book.title).all()

    return render_template(
        "home.html",
        books=books,
        sort=sort,
        query=query
    )


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birthdate']
        date_of_death = request.form.get('date_of_death')

        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d').date() if date_of_death else None

        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()

        message = f"Author {name} was added!"

        return render_template('add_author.html', message=message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    message = ""

    authors = Author.query.all()  # für das Dropdown

    if request.method == 'POST':
        title = request.form['title']
        isbn = request.form['isbn']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']

        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )

        db.session.add(new_book)
        db.session.commit()

        message = "Book was added successfully!"

    return render_template(
        'add_book.html',
        authors=authors,
        message=message
    )


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    message = f"Book '{book.title}' was deleted!"

    books = Book.query.join(Author).order_by(Book.title).all()
    return render_template('home.html', books=books, message=message)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)


#with app.app_context():
#  db.create_all()