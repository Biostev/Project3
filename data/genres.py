from sqlalchemy import Column, Integer, String

from .db_session import SqlAlchemyBase


class Genre(SqlAlchemyBase):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Genre> {self.id} {self.name}'
