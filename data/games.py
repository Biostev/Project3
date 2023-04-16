from datetime import date

from sqlalchemy import (Column, Integer, String,
                        Date, Table, ForeignKey, orm)

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
    Column('genre_id', Integer,
           ForeignKey('genres.id')),
    Column('game_id', Integer,
           ForeignKey('games.id'))
)

platforms_association_table = Table(
    'platforms_to_games',
    SqlAlchemyBase.metadata,
    Column('platform_id', Integer,
           ForeignKey('platforms.id')),
    Column('game_id', Integer,
           ForeignKey('games.id'))
)

companies_association_table = Table(
    'companies_to_games',
    SqlAlchemyBase.metadata,
    Column('company_id', Integer,
           ForeignKey('companies.id')),
    Column('game_id', Integer,
           ForeignKey('games.id'))
)


class Game(SqlAlchemyBase):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    release_date = Column(Date, nullable=False)

    users = orm.relationship(
        'User', secondary=users_association_table, backref='linked_users'
    )

    genres = orm.relationship(
        'Genre', secondary=genres_association_table, backref='genres'
    )

    platforms = orm.relationship(
        'Platform', secondary=platforms_association_table, backref='platforms'
    )

    companies = orm.relationship(
        'Company', secondary=companies_association_table, backref='companies'
    )

    def __init__(self, id: int, name: str,
                 rating: int, release_date: date):
        self.id = id
        self.name = name
        self.rating = rating
        self.release_date = release_date

    def __repr__(self):
        return f'<Game> {self.id} {self.name} {self.release_date}'
