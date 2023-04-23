import datetime
import os
import base64
from PIL import Image
import io
from math import ceil

from flask import (Flask, render_template, redirect, request)
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

import api_requests
from data import db_session
from data.users import User, RegisterForm, EditProfileForm
from data.games import Game

from werkzeug.utils import secure_filename

from DBCreator import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log in')


@app.route('/')
@app.route('/home')
def index():
    days_to_subtract = 90
    date = datetime.datetime.today() - datetime.timedelta(days=days_to_subtract)
    db_sess = db_session.create_session()
    games = list(db_sess.query(Game).filter(
        Game.release_date > date
    ).order_by(Game.rating))[:-15:-1]
    return render_template(
        'index.html',
        games=games
    )


@app.route('/game/<game_id>')
def game_page(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == game_id)[0]
    return render_template(
        'game.html',
        game=game
    )


@app.route('/all_games/<cur_page>')
def all_games_page(cur_page):
    db_sess = db_session.create_session()
    all_games = db_sess.query(Game).order_by(Game.rating)[::-1]
    games_per_page = 5
    cur_page = int(cur_page)
    total_pages = ceil(len(all_games) / games_per_page)
    near_pages = range(max(1, cur_page - 5), min(cur_page + 6, total_pages))
    return render_template(
        'all_games.html',
        games=all_games[(cur_page - 1) * games_per_page: cur_page * games_per_page],
        near_pages=near_pages,
        total_pages=total_pages,
        cur_page=cur_page,
        games_per_page=games_per_page,
    )


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/profile')
def profile():
    form = EditProfileForm()
    date = calculate_date()
    avatar = make_avatar(current_user)
    return render_template(
        'profile.html',
        avatar=avatar, date=date[0], days=date[1],
        edit_mode=False,
        form=form
    )


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(
        name=current_user.name,
        email=current_user.email
    )

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        same_name = db_sess.query(User).filter(User.email == form.email.data).first()
        same_email = db_sess.query(User).filter(User.name == form.name.data).first()
        if same_name and same_name != current_user:
            return render_template('profile.html', title='Регистрация',
                                   form=form,
                                   edit_mode=True,
                                   message='This name already exists')
        if same_email and same_email != current_user:
            return render_template('profile.html', title='Регистрация',
                                   form=form,
                                   edit_mode=True,
                                   message='This email already exists')

        user = db_sess.query(User).filter(User.email == current_user.email).first()
        user.name = form.name.data
        user.email = form.email.data
        loaded_avatar = request.files['avatar']
        if loaded_avatar.filename:
            avatar_name = secure_filename(loaded_avatar.filename)
            loaded_avatar.save(avatar_name)
            with open(avatar_name, 'rb') as file:
                avatar = file.read()
            os.remove(avatar_name)
            user.avatar = avatar
        db_sess.commit()

        return redirect('/profile')
    return render_template(
        'profile.html', title='Profile edit',
        edit_mode=True,
        form=form
    )


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

        user = User(
            form.name.data,
            form.email.data,
            form.password.data
        )
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('register.html', title='Registry', form=form)


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
                               message="Invalid login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def calculate_date():
    date = current_user.created_date.date()

    end = datetime.datetime.now().date()

    diff = end - date

    days = int(diff.total_seconds() // 86400)
    return date, days


def make_avatar(user):
    avatar = user.avatar
    avatar = base64.b64encode(avatar)
    avatar = avatar.decode("UTF-8")
    return avatar


def main():
    db_session.global_init("db/GameManager.db")
    # init_db()  # this is used to create db
    app.run()


# def get_popular_games():


if __name__ == '__main__':
    main()
