from sqlalchemy import Column, Integer, String, orm, ForeignKey
from sqlalchemy.orm import Session

from data.db_session import DbBase


class Profile(DbBase):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = orm.relation('User', foreign_keys=user_id)
    login = Column(String, unique=True)
    password = Column(String)
    saving_preference = Column(String, default='manual')
    theme = Column(String, default='Белый')

    def set_preferred_theme(self, theme_color: str, session: Session):
        """" Осуществляет изменение предпочитаемой темы в БД """
        self.theme = theme_color
        session.merge(self)
        session.commit()

    def set_saving_preference(self, preference: str, session: Session):
        """ Изменяет способ сохранения """
        self.saving_preference = preference
        session.merge(self)
        session.commit()
