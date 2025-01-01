import json

from flask import Flask, render_template
from sqlalchemy import select, insert

from database import Base, engine, session
from models import User, Book, Genre, GenreBook

app = Flask(__name__)


@app.before_request
def before_request():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # stmt = select(Book)
    # exist = session.execute(stmt)
    # if exist.fetchall():
    #     return

    with open('fixtures/books.json', encoding='utf-8') as file:
        books = json.load(file)

    with open('fixtures/genre.json', encoding='utf-8') as file:
        genres = json.load(file)

    with open('fixtures/genre_book.json', encoding='utf-8') as file:
        genre_books = json.load(file)

    for book_data in books:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            year=book_data['pub date'],
            description=book_data['description'],
        )
        session.add(book)

    for genre_data in genres:
        genre = Genre(name=genre_data['name'])
        session.add(genre)

    for gb_data in genre_books:
        gb = GenreBook(
            book_id=gb_data['book_id'],
            genre_id=gb_data['genre_id'],
        )
        session.add(gb)

    session.commit()

@app.route('/')
def index():
    books = session.query(Book).all()
    return render_template('books.html', books=books)


if __name__ == '__main__':
    app.run(debug=True)
