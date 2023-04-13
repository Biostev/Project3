from datetime import date

from sqlalchemy import (Column, Integer, String,
                        Date, Table, orm, ForeignKey)

from .db_session import SqlAlchemyBase

users_association_table = Table(
    'users_to_games',
    SqlAlchemyBase.metadata,
    Column('game_id', Integer,
           ForeignKey('games.id')),
    Column('user_id', Integer,
           ForeignKey('users.id'))
)

genres_association_table = Table(
    'genres_to_games',
    SqlAlchemyBase.metadata,
    Column('game_id', Integer,
           ForeignKey('games.id')),
    Column('genre_id', Integer,
           ForeignKey('genres.id'))
)


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    platform = Column(String, nullable=True)
    release_date = Column(Date, nullable=False)

    users = orm.relationship(
        'User', secondary=users_association_table, backref='linked_users'
    )

    genres = orm.relationship(
        'Genre', secondary=genres_association_table, backref='genres'
    )

    def __init__(self, name: str, company: str,
                 platform: str, release_date: date):
        self.name = name
        self.company = company
        self.platform = platform
        self.release_date = release_date

    def __repr__(self):
        return f'<News> {self.id} {self.title} {self.is_private} {self.user_id}'
