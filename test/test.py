import io

from main.models import Book
from main import db


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_registration(client, init_db):
    response = client.post('/registration/', data={
        'username': 'test_name',
        'email': 'mail@test.kl',
        'password': 'pass',
        'password2': 'pass',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Вы успешно зарегистрировались!' in response.data.decode('utf-8')


def test_correct_login(client, init_db):
    response = client.post('/login/', data={
        'username': 'test-admin',
        'password': 'admin',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'test-admin' in response.data.decode('utf-8')


def test_logout(client):
    response = client.get('/logout/', follow_redirects=True)
    assert response.status_code == 200


def test_admin(client, init_db, user_authorization):
    response = client.get('/admin/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Админ панель' in response.data.decode('utf-8')


def test_books(client, user_authorization, init_db):
    response = client.get('/books/', follow_redirects=True)
    assert response.status_code == 200
    assert 'Test Book' in response.data.decode('utf-8')


def test_book_detail(client, user_authorization, init_db):
    response = client.get('/book/detail/1', follow_redirects=True)
    assert response.status_code == 200
    b = response.data.decode('utf-8')
    # breakpoint()
    assert 'genre_1' in response.data.decode('utf-8')


def test_book_genre_sort(client, user_authorization):
    response = client.get('/book/genres/genre_1', follow_redirects=True)
    assert response.status_code == 200
    assert 'Список книг по жанру genre_1' in response.data.decode('utf-8')


def test_book_create(client, user_authorization, init_db):
    response = client.post('/book/create/', data={
        'title': 'Book2',
        'author': 'Author2',
        'year': 1999,
        'description': 'Description2',
        'genres': 1,
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Вы успешно создали книгу!' in response.data.decode('utf-8')


def test_update_book_list(client, user_authorization, init_db):
    response = client.get('/book/update/', follow_redirects=True)
    assert 'Test Book' in response.data.decode('utf-8')
    assert response.status_code == 200


def test_book_update(client, user_authorization, init_db):
    client.post('/book/update/1', data={
        'title': 'Update book',
        'author': 'Update author',
        'year': 2000,
        'description': 'Update description',
        'archived': True,
    }, follow_redirects=True)
    response = client.get('/book/update/1', follow_redirects=True)
    assert response.status_code == 200
    assert 'Update book' in response.data.decode('utf-8')
    assert 'Update description' in response.data.decode('utf-8')


def test_book_download(client, user_authorization, init_db):
    response = client.get('/book/download/test.txt', follow_redirects=True)
    assert response.status_code == 200


def test_download_files(client, user_authorization, init_db):
    response = client.post(
        '/book/update/1',
        data={
            'title': 'Test Book',
            'author': 'Test Author',
            'year': 2000,
            'description': 'Test Description',
            'file': (io.BytesIO(b'test file'), 'test.txt'),
            'image': (io.BytesIO(b'test image'), 'test.jpg'),
        },
        follow_redirects=True,
        content_type='multipart/form-data'
    )
    book = db.session.query(Book).filter(Book.id == 1).first()
    assert response.status_code == 200
    assert 'Test_Book.txt' in book.file
    assert '/static/images/Test_Book.jpg' in book.image
