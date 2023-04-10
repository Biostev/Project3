import sqlalchemy
# from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Game(SqlAlchemyBase):
    # collections = orm.relationship("Collection",
    #                                secondary="type",
    #                                backref="games")
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    company = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    platform = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    release_date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)

    def __repr__(self):
        return f'<News> {self.id} {self.title} {self.is_private} {self.user_id}'
