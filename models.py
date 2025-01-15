from typing import Any, Dict
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, Column, DateTime, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from werkzeug.security import generate_password_hash, check_password_hash

from app_init import login_manager
from database import Base, session


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(70), nullable=False)
    email = Column(String(120), nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    is_admin = Column(Boolean, nullable=False, default=False)

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


@login_manager.user_loader
def load_user(user_id: int):
    return session.query(User).get(user_id)


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(120), nullable=False)
    author = Column(String(60), nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    image = Column(String, nullable=True)
    file = Column(String, nullable=True)
    archived = Column(Boolean, nullable=False, default=False)

    genrebook = relationship(
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


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    genrebook = relationship(
        'GenreBook',
        back_populates='genre',
        cascade='all, delete-orphan'
    )
    books = association_proxy('genrebook', 'book')


class GenreBook(Base):
    __tablename__ = 'genre_book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    genre_id = Column(Integer, ForeignKey('genre.id'), nullable=False)

    book = relationship('Book', back_populates='genrebook')
    genre = relationship('Genre', back_populates='genrebook')
