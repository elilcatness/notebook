from sqlalchemy import Column, Integer, ForeignKey, orm

from data import db_session


class User(db_session.DbBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    profile = orm.relation('Profile', foreign_keys=profile_id)
