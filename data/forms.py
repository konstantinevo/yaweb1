from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField, RadioField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    type = RadioField('Кто вы?', coerce=str, choices=[('1', 'User'), ('2', 'Administrator')],
                      default='1', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Продолжить')


class UserProfileForm(FlaskForm):
    email = EmailField('Адрес электронной почты', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    save = SubmitField('Сохранить')
    delete = SubmitField('Удалить аккаунт')


class ChangePasswordForm(FlaskForm):
    new_password = StringField('Введите новый пароль', validators=[DataRequired()])
    new_password_again = StringField('Повторите пароль', validators=[DataRequired()])
    button = SubmitField('Подтвердить')


class SearchForm(FlaskForm):
    city = StringField('Город', validators=[DataRequired()])
    name = StringField('Название книги', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class ItemForm(FlaskForm):

    name = StringField('Название книги', validators=[DataRequired()])
    author = StringField('Автор', validators=[DataRequired()])
    library_id = StringField('Библиотека', validators=[DataRequired()])
    save = SubmitField('Сохранить')


class LibraryForm(FlaskForm):  # форма показа сведений о конкретном товаре либо его добавлении
    name = StringField('Название библиотеки', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    address = StringField('Адрес библиотеки', validators=[DataRequired()])
    save = SubmitField('Сохранить')
