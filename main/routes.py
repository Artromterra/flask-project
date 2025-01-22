import json

from flask import request, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy import select
from werkzeug.security import generate_password_hash

from main import app, db, login_manager
from main.forms import LoginForm, RegistrationForm, BookCreateForm, BookUpdateForm
from main.models import Book, Genre, GenreBook, User
from main.utils import upload_file, upload_image


@login_manager.user_loader
def load_user(user_id: int):
    return db.session.query(User).get(user_id)


@app.before_request
def before_request():
    # db.drop_all()
    db.create_all()
    stmt = select(Book)
    exist = db.session.execute(stmt)
    if exist.fetchall():
        return

    with open('../fixtures/books.json', encoding='utf-8') as file:
        books = json.load(file)

    with open('../fixtures/genre.json', encoding='utf-8') as file:
        genres = json.load(file)

    with open('../fixtures/genre_book.json', encoding='utf-8') as file:
        genre_books = json.load(file)

    for book_data in books:
        book = Book(
            title=book_data['title'],
            author=book_data['author'],
            year=book_data['pub date'],
            description=book_data['description'],
            image=book_data['image'],
            file=book_data['file'],
        )
        db.session.add(book)

    for genre_data in genres:
        genre = Genre(name=genre_data['name'])
        db.session.add(genre)

    for gb_data in genre_books:
        gb = GenreBook(
            book_id=gb_data['book_id'],
            genre_id=gb_data['genre_id'],
        )
        db.session.add(gb)

    password = generate_password_hash('admin')
    user = User(
        name='admin',
        email='admin@email.com',
        password=password,
        is_admin=True,
    )
    db.session.add(user)

    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User(
            name=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('books_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(
            User.name == form.username.data
        ).first()
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


@app.route('/admin/', methods=['GET'])
@login_required
def admin():
    if current_user.is_admin:
        return render_template('admin.html')
    return render_template('index.html')


@app.route('/books/', methods=['GET'])
@login_required
def books_list():
    books = db.session.query(Book).filter(
        Book.archived == False
    ).order_by(
        Book.title
    ).all()
    return render_template('books.html', books=books)


@app.route('/book/detail/<int:book_id>/', methods=['GET'])
@login_required
def book_detail(book_id):
    book = db.session.query(Book).filter(
        Book.id == book_id
    ).first()
    return render_template('book-detail.html', book=book)


@app.route('/book/genres/<genre>/', methods=['GET'])
@login_required
def book_sort_by_genre(genre):
    books = (db.session.query(Book).
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
        form.genres.choices = [
            (g.id, g.name) for g in db.session.query(Genre).order_by(Genre.name).all()
        ]
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
            db.session.add(book)
            db.session.commit()
            book_id = db.session.query(Book.id).filter(
                Book.title == form.title.data,
                Book.author == form.author.data,
            ).first()[0]
            for genre_id in form.genres.data:
                genre_book = GenreBook(
                    book_id=book_id,
                    genre_id=int(genre_id),
                )
                gb_list.append(genre_book)
            db.session.add_all(gb_list)
            db.session.commit()
            flash('Вы успешно создали книгу!', category='create-success')
        return render_template('create-book.html', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/book/update/', methods=['GET', 'POST'])
@login_required
def book_update_list():
    if current_user.is_admin:
        books = db.session.query(Book).order_by(Book.title).all()
        return render_template('book-update-list.html', books=books)
    return redirect(url_for('books_list'))


@app.route('/book/update/<int:book_id>/', methods=['GET', 'POST'])
@login_required
def book_update(book_id):
    if current_user.is_admin:
        book = db.session.query(Book).filter(Book.id == book_id).first()
        form = BookUpdateForm(obj=book)
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

            db.session.add(book)
            db.session.commit()
            flash('Вы успешно обновили книгу!', category='update-success')
        return render_template('update-book.html', form=form)


@app.route('/book/download/<path:name>/', methods=['GET'])
@login_required
def book_download(name):
    return send_from_directory(
        app.config['UPLOAD_FILE_FOLDER'],
        name,
        as_attachment=True
    )
