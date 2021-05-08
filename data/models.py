import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class People(UserMixin, SerializerMixin, SqlAlchemyBase):
    __tablename__ = 'people'  # имя таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, primary_key=True, autoincrement=True)  # id аккаунта
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # фамилия
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # имя
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)  # адрес эл.почты
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # хэшированный пароль
    role = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # роль - админ или юзер
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)  # дата и время регистрации

    def set_password(self, password):  # функция добавления пароля
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):  # функция хэширования пароля
        return check_password_hash(self.hashed_password, password)

    @property  # функция со спец.декоратором для удобного представления данных об объекте модели из query() запроса
    def serialize(self):
        return {
            'id': self.id,
            'surname': self.surname,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_date': self.created_date
        }


class Library(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'libraries'  # имя таблицы

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # адрес работы
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    city = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # название места работы
    books = orm.relation("Book", back_populates='library')

    @property  # функция со спец.декоратором для удобного представления данных об объекте модели из query() запроса
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city
        }


class Book(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'books'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)  # id товара
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # наименование товара
    author = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # категория товара
    library_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("libraries.id"))

    created_datetime = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)  # дата и время последнего
    # редактирования
    library = orm.relation('Library')

    @property  # функция со спец.декоратором для удобного представления данных об объекте модели из query() запроса
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'library_id': self.library_id,
            'date': self.created_datetime
        }
