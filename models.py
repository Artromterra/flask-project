from typing import Any, Dict

from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    password = Column(String, nullable=False)
    is_registered = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return "<User(name='{name}', email='{email}')>".format(
            name=self.name,
            email=self.email
        )

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    image_path = Column(String, nullable=True)

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

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)

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
