from sqlalchemy import Column, Integer, String

from .db_session import SqlAlchemyBase


class Platform(SqlAlchemyBase):
    __tablename__ = 'platforms'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Platform> {self.id} {self.name}'
