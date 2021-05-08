import os
from random import randint
from flask_restful import abort
from flask import Flask, make_response, jsonify, render_template, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.utils import redirect
from data.models import People, Library, Book
from data.forms import RegistrationForm, LoginForm, UserProfileForm, \
    ChangePasswordForm, ItemForm, SearchForm, LibraryForm
from werkzeug.security import generate_password_hash
from data import db_session, search, api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.config["JSON_AS_ASCII"] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

login_manager = LoginManager()
login_manager.init_app(app)
id_ = 0


@login_manager.user_loader
def load_user(user_email):
    db_sess = db_session.create_session()
    return db_sess.query(People).get(user_email)


@app.errorhandler(404)
def not_found(_):
    return make_response(jsonify({'error': 'Страничка не найдена'}), 404)


@app.errorhandler(400)
def not_found(_):
    return make_response(jsonify({'error': 'Такая библиотека отсутствует в БД'}), 400)


@app.errorhandler(403)
def no_access(_):
    return make_response(jsonify({'error': 'У вас нет прав доступа к этой странице'}))


@app.errorhandler(401)
def unauthorized(_):
    return make_response(jsonify({'error': 'Вы не авторизованы'}))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/user_registration', methods=['GET', 'POST'])  # регистрация нового аккаунта
def user_registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('user_registration.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()  # создаём сессию
        if db_sess.query(People).filter(People.email == form.email.data).first():
            return render_template('user_registration.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже существует")
        if form.type.data == '2':
            role = 'Admin'
        else:
            role = 'User'
        user = People(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            role=role
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

    return render_template('user_registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        human = db_sess.query(People).filter(People.email == form.email.data).first()
        if human and human.check_password(form.password.data):
            login_user(human, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неверный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if form.new_password.data != form.new_password_again.data:
            return render_template('change_password.html', title='Смена пароля', form=form,
                                   message="Пароли не совпадают")
        db_sess.query(People).filter(People.email == current_user.email). \
            update({'hashed_password': generate_password_hash(form.new_password.data)})
        db_sess.commit()  # обновляем данные в дб и коммитим
        return redirect('/')
    return render_template('change_password.html', title='Смена пароля', form=form)


@app.route('/', methods=['POST', 'GET'])
def index():
    form = SearchForm()
    if form.validate_on_submit():

        name = form.name.data.lower()
        try:
            db_sess = db_session.create_session()
            author = str(db_sess.query(Book.author).filter(Book.name == name.lower()).first()[0]).lower()
            library_id = int(db_sess.query(Book.library_id).filter(Book.name == name.lower()).first()[0])
            library = str(db_sess.query(Library.name).filter(Library.id == library_id).first()[0]).lower()
            address = form.city.data + ' ' + str(db_sess.query(Library.address).filter(Library.id == library_id).
                                                 first()[0]).lower()
            books = []
            for book in db_sess.query(Book).filter(Book.name == name.lower(), Book.author == author,
                                                   Book.library_id == library_id):
                books.append(book.serialize)
            search.image(address)
            true_city = db_sess.query(Library.city).filter(Library.name == library.lower()).first()[0].lower()
            if true_city == form.city.data.lower():
                if books:
                    params = {
                        'address': address,
                        'img': f'map1.png',
                        'ver': f'{randint(0, 10324324939)}'
                    }
                    return render_template('content.html', **params,
                                           title=f'{name} автор {author} в'
                                                 f' {library} в городе {form.city.data}', form=form)
        except:
            params = {
                'title': f'Книга не найдена\n({form.name.data})'
            }
            return render_template('content.html', **params, form=form)

        return render_template('content.html', title=f'Такая книга есть, но она в городе {true_city}', form=form)
    return render_template('content.html', title=f'Давайте найдем интересующую вас книгу:)', form=form)


@app.route('/book_add', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role == 'Admin':
        form = ItemForm()
        db_sess = db_session.create_session()
        if form.validate_on_submit():
            try:
                lib_id = int(db_sess.query(Library.id).filter(Library.name == form.library_id.data.lower()).
                             first()[0])
                book = Book(
                    name=form.name.data.lower(),
                    author=form.author.data.lower(),
                    library_id=lib_id,
                )
                db_sess.add(book)
                db_sess.commit()
                return redirect('/book_add')
            except:
                abort(400)
        return render_template('book_add.html', form=form, title='Добавление книги')
    abort(403)


@app.route('/libraries_add', methods=['GET', 'POST'])
@login_required
def add_library():
    if current_user.role == 'Admin':
        form = LibraryForm()
        db_sess = db_session.create_session()
        if form.validate_on_submit():

            library = Library(
                name=form.name.data.lower(),
                city=form.city.data.lower(),
                address=form.address.data.lower(),
            )
            db_sess.add(library)
            db_sess.commit()
            return redirect('/libraries_add')
        return render_template('libraries_add.html', form=form, title='Добавление библиотеки')
    abort(403)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def on_profile():
    db_sess = db_session.create_session()
    info = db_sess.query(People).filter_by(email=current_user.email)
    info = [x.serialize for x in info.all()][0]
    if info['role'] == 'User':
        form = UserProfileForm()
        if form.validate_on_submit():
            if 'save' in [i for i in request.form]:
                db_sess.query(People).filter(People.email == current_user.email). \
                    update({"email": form.email.data,
                            "surname": form.surname.data,
                            "name": form.name.data})
                db_sess.commit()
                return redirect('/')
            else:
                db_sess.query(People).filter(People.email == current_user.email).delete()
                db_sess.commit()
                return redirect('/')
        form.email.data = info['email']
        form.surname.data = info['surname']
        form.name.data = info['name']
        return render_template('lets see user profile.html', form=form, title='Редактирование профиля')
    else:
        form = UserProfileForm()
        if form.validate_on_submit():
            if 'save' in [i for i in request.form]:
                db_sess.query(People).filter(People.email == current_user.email). \
                    update({"email": form.email.data,
                            "surname": form.surname.data,
                            "name": form.name.data})
                db_sess.commit()
                return redirect('/')
            else:  # если это не кнопка сохранить
                db_sess.query(People).filter(People.email == current_user.email).delete()
                db_sess.commit()
                return redirect('/')
        form.email.data = info['email']
        form.surname.data = info['surname']
        form.name.data = info['name']
        return render_template('lets see user profile.html', form=form, title='Редактирование профиля')


if __name__ == '__main__':
    db_session.global_init("db/library.db")  # инициилизация дб
    app.register_blueprint(api.blueprint)
    port = int(os.environ.get("PORT", 8000))
    app.run(host='127.0.0.1', port=port)

