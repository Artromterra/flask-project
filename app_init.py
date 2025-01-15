import os

from flask import Flask
from flask_login import LoginManager

from env_conf import SECRET_KEY

UPLOAD_IMAGE_FOLDER = os.path.abspath('static/images')
UPLOAD_FILE_FOLDER = os.path.abspath('static/files')
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
app.config['UPLOAD_FILE_FOLDER'] = UPLOAD_FILE_FOLDER

login_manager = LoginManager(app)
login_manager.login_view = 'login'

print(UPLOAD_IMAGE_FOLDER)