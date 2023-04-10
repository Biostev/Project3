from flask import (Flask, render_template, redirect)
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import (LoginManager, login_user, login_required,
                         logout_user)
from data import db_session
from data.users import User, RegisterForm
from data.games import Game

from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route("/")
def index():
    return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def init_db():  # test func to initialize db with test users and games
    db_sess = db_session.create_session()

    user = User()
    user.name = 'Пользователь 1'
    user.email = 'email1@email.ru'
    user.set_password('Password')
    db_sess.add(user)

    user = User()
    user.name = 'Пользователь 2'
    user.email = 'email2@email.ru'
    user.set_password('Password')
    db_sess.add(user)

    user = User()
    user.name = 'Пользователь 3'
    user.email = 'email3@email.ru'
    user.set_password('Password')
    db_sess.add(user)

    user = User()
    user.name = 'Пользователь 4'
    user.email = 'email4@email.ru'
    user.set_password('Password')
    db_sess.add(user)

    game = Game(name="BioShock",
                genre="Adventure",
                company='2K',
                platform='PC',
                release_date=date(2010, 12, 5))
    db_sess.add(game)

    db_sess.commit()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/GameManager.db")
    app.run()


if __name__ == '__main__':
    main()
