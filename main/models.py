from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.associationproxy import association_proxy

from main import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<User(id='{id}' name='{name}')>".format(
            id=self.id,
            name=self.name,
        )

    # хеширование паролей
    def set_password(self, password: str):
        self.password = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password, password)


class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String, nullable=True)
    file = db.Column(db.String, nullable=True)
    archived = db.Column(db.Boolean, nullable=False, default=False)

    genrebook = db.relationship(
        'GenreBook',
        back_populates='book',
        cascade='all, delete-orphan'
    )
    genres = association_proxy('genrebook', 'genre')

    def __repr__(self):
        return "<Book(title='{title}', author='{author}')>".format(
            title=self.title,
            author=self.author,
        )


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True)

    genrebook = db.relationship(
        'GenreBook',
        back_populates='genre',
        cascade='all, delete-orphan'
    )
    books = association_proxy('genrebook', 'book')


class GenreBook(db.Model):
    __tablename__ = 'genre_book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)

    book = db.relationship('Book', back_populates='genrebook')
    genre = db.relationship('Genre', back_populates='genrebook')
