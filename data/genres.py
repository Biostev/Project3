from sqlalchemy import Column, Integer, String

from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<News> {self.id} {self.title} {self.is_private} {self.user_id}'
