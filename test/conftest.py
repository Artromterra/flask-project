import pytest

from werkzeug.security import generate_password_hash

from main import app, db as _db
from main.models import Book, Genre, GenreBook, User


@pytest.fixture(scope='session')
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture(scope='session')
def init_db(client):
    _db.drop_all()
    _db.create_all()
    book = Book(
        title='Test Book',
        author='Test Author',
        year=2000,
        description='Test Description',
    )
    genre1 = Genre(
        name='genre_1',
    )
    genre2 = Genre(
        name='genre_2',
    )
    genrebook1 = GenreBook(
        book_id=1,
        genre_id=1,
    )
    genrebook2 = GenreBook(
        book_id=1,
        genre_id=2,
    )
    password = generate_password_hash('admin')
    user = User(
        name='test-admin',
        email='test-admin@mail.ru',
        password=password,
        is_admin=True,
    )
    _db.session.add_all([book, genre1, genre2, genrebook1, genrebook2, user])
    _db.session.commit()

    yield app

    _db.session.close()
    _db.drop_all()


@pytest.fixture(scope='function')
def user_authorization(client):
    client.post('/login/', data={
        'username': 'test-admin',
        'password': 'admin',
    }, follow_redirects=True)

    yield client

    client.get('/logout/', follow_redirects=True)