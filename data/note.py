import datetime as dt
import os
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, orm, Table
from PyQt5.QtWidgets import QTextEdit
from sqlalchemy.orm import Session

if os.getcwd().split('\\')[-1] != 'data':
    from data.baseField import BaseField
    from data.db_session import DbBase
else:
    from baseField import BaseField
    from db_session import DbBase


category_to_note = Table('category_to_note', DbBase.metadata,
                         Column('category', Integer, ForeignKey('categories.id')),
                         Column('note', Integer, ForeignKey('notes.id')))


class Note(DbBase, BaseField):  # Класс, отвечающий за инкапсуляцию данных о заметках
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String, unique=True, nullable=False)
    body = Column(String, nullable=True)
    categories = orm.relation('Category', secondary=category_to_note, backref='notes')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = orm.relation('User', foreign_keys=user_id)
    date = Column(DateTime, default=dt.datetime.now)

    def __init__(self, session: Session, text: QTextEdit,
                 title: str, body: str, user_id: int, date: str = None):
        super(Note, self).__init__()
        BaseField.__init__(self, session, text, title, body, user_id, date)