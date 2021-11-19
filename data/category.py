import os

from sqlalchemy import Column, Integer, String

if os.getcwd().split('\\')[-1] != 'data':
    from data.db_session import DbBase
else:
    from db_session import DbBase


class Category(DbBase):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, unique=True)
