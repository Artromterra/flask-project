from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    TextAreaField,
    FileField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from main import db
from main.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), EqualTo('password2')])
    password2 = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Отправить')

    def validate_email(self, field):
        if db.session.query(User).filter_by(email=field.data).first():
            raise ValidationError('Почта уже используется')


class LoginForm(FlaskForm):
    username = StringField('Пользователь', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Отправить')


class BookCreateForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    year = IntegerField('Год публикации', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Картинка', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Only images!')
    ])
    file = FileField('Файл', validators=[
        FileAllowed(['pdf', 'txt'], 'PDF or TXT files only!')])
    genres = SelectMultipleField('Жанр',choices=[])
    archived = BooleanField('Архивировать книгу')
    submit = SubmitField('Создать')


class BookUpdateForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    year = IntegerField('Год публикации', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    image = FileField('Картинка', validators=[
        FileAllowed(['png', 'jpg', 'jpeg', 'gif'], 'Only images!')
    ])
    file = FileField('Файл', validators=[
        FileAllowed(['pdf', 'txt'], 'PDF or TXT files only!')])
    archived = BooleanField('Архивировать книгу')
    submit = SubmitField('Обновить')
