import datetime

from flask_login import UserMixin
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sqlalchemy import Column, Integer, String, DateTime, BLOB
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)
    with open('static/img/default_avatar.png', 'rb') as file:
        default_avatar = file.read()
    avatar = Column(BLOB, default=default_avatar)

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return f'<User> {self.id} {self.name} {self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def set_avatar(self, new_avatar):
        with open(new_avatar, 'rb') as avatar:
            self.avatar = avatar.read()

    def change_name(self, new_name):
        self.name = new_name

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditProfileForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    avatar = FileField(
        'Avatar',
        validators=[FileAllowed(['jpg', 'png'], 'Images only!')],
    )
    submit = SubmitField('Submit')
