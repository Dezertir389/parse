import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase


class Flowers(SqlAlchemyBase):
    __tablename__ = 'flowers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    links = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    png = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    mid_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)