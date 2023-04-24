import base64
import datetime
import os
from math import ceil

from flask import (Flask, render_template, redirect, request, url_for)
from flask_login import (LoginManager, login_user, login_required,
                         logout_user, current_user)
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import (EmailField, PasswordField, BooleanField,
                     SubmitField)
from wtforms.validators import DataRequired

from data import db_session
from data.companies import Company
from data.games import Game
from data.genres import Genre
from data.platforms import Platform
from data.users import User, RegisterForm, EditProfileForm

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
        logo_img=url_for('static', filename='img/gamepad.png'),
        games=games,
    )


@app.route('/search/genres/<genre_id>/<cur_page>')
def search_by_genre(genre_id, cur_page):
    db_sess = db_session.create_session()
    genre = db_sess.query(Genre).filter(Genre.id == genre_id).first()
    games = db_sess.query(Game).filter(Game.genres.contains(genre)).order_by(Game.rating)[::-1]
    games_per_page = 5
    cur_page = int(cur_page)
    total_pages = ceil(len(games) / games_per_page)
    near_pages = range(max(1, cur_page - 5), min(cur_page + 6, total_pages))
    return render_template(
        'search_by_genre.html',
        logo_img=url_for('static', filename='img/gamepad.png'),
        style1=url_for('static', filename='css/all_data_pages.css'),
        style2=url_for('static', filename='css/pagination.css'),
        style3=url_for('static', filename='css/style.css'),
        games=games[(cur_page - 1) * games_per_page: cur_page * games_per_page],
        near_pages=near_pages,
        total_pages=total_pages,
        cur_page=cur_page,
        games_per_page=games_per_page,
        genre=genre,
    )


@app.route('/search/platforms/<platform_id>/<cur_page>')
def search_by_platform(platform_id, cur_page):
    db_sess = db_session.create_session()
    platform = db_sess.query(Platform).filter(Platform.id == platform_id).first()
    games = db_sess.query(Game).filter(Game.platforms.contains(platform)).order_by(Game.rating)[::-1]
    games_per_page = 5
    cur_page = int(cur_page)
    total_pages = ceil(len(games) / games_per_page)
    near_pages = range(max(1, cur_page - 5), min(cur_page + 6, total_pages))
    return render_template(
        'search_by_platform.html',
        logo_img=url_for('static', filename='img/gamepad.png'),
        style1=url_for('static', filename='css/all_data_pages.css'),
        style2=url_for('static', filename='css/pagination.css'),
        style3=url_for('static', filename='css/style.css'),
        games=games[(cur_page - 1) * games_per_page: cur_page * games_per_page],
        near_pages=near_pages,
        total_pages=total_pages,
        cur_page=cur_page,
        games_per_page=games_per_page,
        platform=platform,
    )


@app.route('/search/companies/<company_id>/<cur_page>')
def search_by_company(company_id, cur_page):
    db_sess = db_session.create_session()
    company = db_sess.query(Genre).filter(Company.id == company_id).first()
    games = db_sess.query(Game).filter(Game.companies.contains(company)).order_by(Game.rating)[::-1]
    games_per_page = 5
    cur_page = int(cur_page)
    total_pages = ceil(len(games) / games_per_page)
    near_pages = range(max(1, cur_page - 5), min(cur_page + 6, total_pages))
    return render_template(
        'search_by_company.html',
        logo_img=url_for('static', filename='img/gamepad.png'),
        style1=url_for('static', filename='css/all_data_pages.css'),
        style2=url_for('static', filename='css/pagination.css'),
        style3=url_for('static', filename='css/style.css'),
        games=games[(cur_page - 1) * games_per_page: cur_page * games_per_page],
        near_pages=near_pages,
        total_pages=total_pages,
        cur_page=cur_page,
        games_per_page=games_per_page,
        company=company,
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
        logo_img=url_for('static', filename='img/gamepad.png'),
        games=all_games[(cur_page - 1) * games_per_page: cur_page * games_per_page],
        near_pages=near_pages,
        total_pages=total_pages,
        cur_page=cur_page,
        games_per_page=games_per_page,
    )


@app.route('/all_users/<cur_page>')
def all_users_page(cur_page):
    db_sess = db_session.create_session()
    all_users = db_sess.query(User).order_by(User.created_date)[::-1]
    users_per_page = 5
    cur_page = int(cur_page)
    total_pages = ceil(len(all_users) / users_per_page)
    near_pages = range(max(1, cur_page - 5), min(cur_page + 6, total_pages))
    return render_template(
        'all_users.html',
        logo_img=url_for('static', filename='img/gamepad.png'),
        users=all_users[(cur_page - 1) * users_per_page: cur_page * users_per_page],
        near_pages=near_pages,
        total_pages=total_pages,
        cur_page=cur_page,
        users_per_page=users_per_page,
    )


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/game/<game_id>')
def game_page(game_id):
    db_sess = db_session.create_session()
    game = db_sess.query(Game).filter(Game.id == game_id)[0]
    return render_template(
        'game.html',
        logo_img=url_for('static', filename='img/gamepad.png'),
        game=game
    )


@app.route('/profile/<user_id>')
def profile(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id)[0]
    form = EditProfileForm()
    date = calculate_date(user)
    avatar = make_avatar(user)
    return render_template(
        'profile.html',
        logo_img=url_for('static', filename='img/gamepad.png'),
        avatar=avatar, date=date[0], days=date[1],
        edit_mode=False,
        form=form,
        user=user,
    )


@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm(
        name=current_user.name,
        email=current_user.email
    )
    user = current_user

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

        return redirect(f'/profile/{current_user.id}')
    return render_template(
        'profile.html', title='Profile edit',
        logo_img=url_for('static', filename='img/gamepad.png'),
        edit_mode=True,
        form=form,
        user=user,
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
    return render_template(
        'register.html', title='Registry', form=form,
        logo_img=url_for('static', filename='img/gamepad.png'),
    )


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
    return render_template(
        'login.html', title='Authorization', form=form,
        logo_img=url_for('static', filename='img/gamepad.png'),
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def calculate_date(user):
    date = user.created_date.date()

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
    app.run(host='127.0.0.1', port=3128)


if __name__ == '__main__':
    main()
