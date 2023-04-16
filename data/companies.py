from sqlalchemy import Column, Integer, String

from .db_session import SqlAlchemyBase


class Company(SqlAlchemyBase):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Company> {self.id} {self.name}'
