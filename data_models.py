from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    date_of_death = db.Column(db.Date, nullable=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return f"{self.name}\n born: ({self.birth_date}\n died: {self.date_of_death})"


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    author = db.relationship('Author', backref=db.backref('books', lazy=True))

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return f"{self.title} ({self.publication_year}) von {self.author.name}"

