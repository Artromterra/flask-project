import json

from flask import render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from database import Base, engine, session
from app_init import app
from forms import LoginForm, RegistrationForm, BookCreateForm
from models import Book, Genre, GenreBook, User
from utils import upload_file, upload_image


@app.before_request
def before_request():
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    stmt = select(Book)
    exist = session.execute(stmt)
    if exist.fetchall():
        return

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

    password = generate_password_hash('admin')
    user = User(
        name='admin',
        email='admin@email.com',
        password=password,
        is_admin=True,
    )
    session.add(user)

    session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(User).filter(User.name == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('books_list'))
        flash('Не правильный логин или пароль.', 'error')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/admin/')
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html')
    return render_template('index.html')


@app.route('/books/', methods=['GET'])
@login_required
def books_list():
    books = session.query(Book).filter(Book.archived == False).order_by(Book.title).all()
    return render_template('books.html', books=books)


@app.route('/book/detail/<int:book_id>/', methods=['GET'])
@login_required
def book_detail(book_id):
    book = session.query(Book).filter(Book.id == book_id).first()
    return render_template('book-detail.html', book=book)


@app.route('/book/genres/<genre>/', methods=['GET'])
@login_required
def book_sort_by_genre(genre):
    books = (session.query(Book).
             filter(Book.genres.any(Genre.name == genre)).
             order_by(Book.title).all()
             )
    return render_template('filter-books.html', books=books, genres=genre)


@app.route('/book/create/', methods=['GET', 'POST'])
@login_required
def book_create():
    gb_list  = []
    if current_user.is_admin:
        form = BookCreateForm()
        form.genres.choices = [(g.id, g.name) for g in session.query(Genre).order_by(Genre.name).all()]
        if form.validate_on_submit():
            file_path = upload_file(form=form)
            img_path = upload_image(form=form)
            book = Book(
                title=form.title.data,
                author=form.author.data,
                year=form.year.data,
                description=form.description.data,
                image=img_path,
                file=file_path,
            )
            session.add(book)
            session.commit()
            book_id = session.query(Book.id).filter(
                Book.title == form.title.data,
                Book.author == form.author.data,
            ).first()
            for genre_id in form.genres.data:
                genre_book = GenreBook(
                    book_id=book_id,
                    genre_id=int(genre_id),
                )
                gb_list.append(genre_book)
            session.add_all(gb_list)
            session.commit()
        return render_template('create-book.html', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/book/update/', methods=['GET', 'POST'])
@login_required
def book_update_list():
    if current_user.is_admin:
        books = session.query(Book).order_by(Book.title).all()
        return render_template('book-update-list.html', books=books)
    return redirect(url_for('books_list'))


@app.route('/book/update/<int:book_id>/', methods=['GET', 'POST'])
@login_required
def book_update(book_id):
    if current_user.is_admin:
        book = session.query(Book).filter(Book.id == book_id).first()
        form = BookCreateForm(obj=book)
        if form.validate_on_submit():
            file_path = upload_file(form=form)
            img_path = upload_image(form=form)

            book.title = form.title.data
            book.author = form.author.data
            book.year = form.year.data
            book.description = form.description.data
            book.archived = form.archived.data
            if img_path is None:
                book.image = book.image
            else:
                book.image = img_path
            if file_path is None:
                book.file = book.file
            else:
                book.file = file_path

            session.add(book)
            session.commit()
            return redirect(url_for('book_update_list'))
        return render_template('update-book.html', form=form)


@app.route('/book/download/<path:name>/', methods=['GET'])
@login_required
def book_download(name):
    return send_from_directory(app.config['UPLOAD_FILE_FOLDER'], name, as_attachment=True)


if __name__ == '__main__':
    app.run()
