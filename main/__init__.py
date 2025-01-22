from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from env_conf import DevelopmentConfig, TestingConfig, ProductionConfig

app = Flask(__name__)

# для разработки
# app.config.from_object(DevelopmentConfig)

# для запуска тестов
# app.config.from_object(TestingConfig)

# для production
app.config.from_object(ProductionConfig)

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from main import routes, models
