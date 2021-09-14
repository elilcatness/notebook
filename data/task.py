import datetime as dt
import os
from typing import Union
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table, orm

from PyQt5.QtWidgets import QTextEdit
from sqlalchemy.orm import Session

if os.getcwd().split('\\')[-1] != 'data':
    from data.baseField import BaseField
    from data.db_session import DbBase
else:
    from baseField import BaseField
    from db_session import DbBase


category_to_task = Table('category_to_task', DbBase.metadata,
                         Column('category', Integer, ForeignKey('categories.id')),
                         Column('task', Integer, ForeignKey('tasks.id')))


class Task(DbBase, BaseField):  # Класс, отвечающий за инкапсуляцию данных о задачах
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=True)
    categories = orm.relation('Category', secondary=category_to_task, backref='tasks')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = orm.relation('User', foreign_keys=user_id)
    date = Column(DateTime, default=dt.datetime.now)
    deadline = Column(DateTime, default=dt.datetime.now)
    closed = Column(Boolean, default=False)

    def __init__(self, session: Session, text: QTextEdit,
                 title: str, body: str, user_id: int, date: str, deadline: dt.datetime, closed: bool):
        super(Task, self).__init__()
        BaseField.__init__(self, session, text, title, body, user_id, date)
        self.deadline = deadline  # Объект даты дедлайна
        # self.deadline = self.convert_str_to_dt(deadline)
        self.closed = closed  # Статус выполнения задачи

    def get_deadline_dt(self, with_time=True) -> Union[dt.date, dt.datetime]:  # Возвращает дедлайн в виде объекта даты
        return (self.deadline if with_time else dt.date(self.deadline.year,
                                                        self.deadline.month,
                                                        self.deadline.day))

    def get_deadline_str(self) -> str:  # Возвращает дедлайн в виде строки
        return self.convert_dt_to_str(self.deadline)

    def close(self) -> bool:  # Отмечает задачу выполненной
        if not self.is_expired():
            self.closed = True
            self.session.merge(self)
            self.session.commit()
            return True
        return False

    def is_closed(self) -> bool:  # Возвращает статус выполнения задачи
        return self.closed

    def is_expired(self) -> bool:  # Возвращает статус выхода из дедлайна задачи
        return self.deadline < dt.datetime.now() and not self.is_closed()
