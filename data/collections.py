# import sqlalchemy
# from sqlalchemy import orm
#
# from .db_session import SqlAlchemyBase
#
#
# class Collection(SqlAlchemyBase):
#     association_table = sqlalchemy.Table(
#         'users_to_games',
#         SqlAlchemyBase.metadata,
#         sqlalchemy.Column('games', sqlalchemy.Integer,
#                           sqlalchemy.ForeignKey('games.id')),
#         sqlalchemy.Column('users', sqlalchemy.Integer,
#                           sqlalchemy.ForeignKey('users.id'))
#     )
#
#     __tablename__ = 'collection'
#
#     user_id = sqlalchemy.Column(sqlalchemy.Integer,
#                                 sqlalchemy.ForeignKey("users.id"),
#                                 primary_key=True)
#     game_id = sqlalchemy.Column(sqlalchemy.Integer,
#                                 sqlalchemy.ForeignKey("games.id"),
#                                 primary_key=True)
#
#     is_favourite = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
#     is_played = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
#
#     user = orm.relationship('User')
#     game = orm.relationship('Game')
