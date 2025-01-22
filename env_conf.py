import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    UPLOAD_IMAGE_FOLDER = os.path.abspath('main/static/images')
    UPLOAD_FILE_FOLDER = os.path.abspath('main/static/files')
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_FOR_DEVELOPMENT")
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
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_FOR_PRODUCTION")
