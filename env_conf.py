import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_USER=os.getenv("DATABASE_USER")
    DATABASE_PASSWORD=os.getenv("DATABASE_PASSWORD")
    DB_NAME=os.getenv("DB_NAME")
    DB_HOST=os.getenv("DB_HOST")
    UPLOAD_IMAGE_FOLDER = os.path.abspath('main/static/images')
    UPLOAD_FILE_FOLDER = os.path.abspath('main/static/files')
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://{user}:{password}@{host}:5432'.format(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DB_HOST,
    )
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    DEBUG=False
    TESTING=False


class DevelopmentConfig(Config):
    DEBUG=True


class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
    WTF_CSRF_ENABLED=False
    UPLOAD_FILE_FOLDER = os.path.abspath('files')
    UPLOAD_IMAGE_FOLDER = os.path.abspath('files')


class ProductionConfig(Config):
    DEBUG=False
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DB_HOST = os.getenv("DB_PRODUCTION_HOST")
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}:5432'.format(
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DB_HOST,
    )
