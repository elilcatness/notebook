import os

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QKeyEvent

from data.profile import Profile
from data.user import User

if os.getcwd().split('\\')[-1] != 'data':
    from data.ui.loginUi import UiLoginForm
    from data.baseApplicationForm import BaseApplicationForm
else:
    from ui.loginUi import UiLoginForm
    from baseApplicationForm import BaseApplicationForm


class LoginForm(QWidget, UiLoginForm, BaseApplicationForm):
    def __init__(self, session, parent):
        super(LoginForm, self).__init__()
        self.setupUi(self)
        self.setFixedSize(320, 400)
        self.verticalLayout.setGeometry(QRect(82, 118, 164, 165))
        self.pushButton.clicked.connect(self.entry)
        self.pushButton_2.clicked.connect(self.registration)

        self.parent = parent  # Ссылка на объект окна-родителя
        self.session = session

        self.sequences = [  # Последовательности на клавиатуре
            'qwe', 'wer', 'ert', 'rty', 'tyu', 'yui', 'uio', 'iop',
            'asd', 'sdf', 'dfg', 'fgh', 'ghj', 'hjk', 'jkl',
            'zxc', 'xcv', 'cvb', 'vbn', 'bnm',
            'йцу', 'цук', 'уке', 'кен', 'енг', 'нгш', 'гшщ', 'шщз', 'щзх', 'зхъ',
            'фыв', 'ыва', 'вап', 'апр', 'про', 'рол', 'олд', 'лдж', 'джэ',
            'ячс', 'чсм', 'сми', 'мит', 'ить', 'тьб', 'ьбю', 'жэё'
        ]

        self.enter_key_value = 16777220  # int значение клавиши Enter

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == self.enter_key_value:
            self.entry()
        else:
            return super(LoginForm, self).keyPressEvent(event)

    def get_data(self) -> tuple:  # Получить логин и пароль из полей для ввода
        return self.login_field.text(), self.password_field.text()

    # Проверяет, заполнены ли оба поля для ввода
    def check_fields(self, login: str, password: str, error_window_title: str):
        if not login or not password:
            self.show_message('Поля должны быть заполнены', error_window_title)
            return False
        return True

    def entry(self):  # Функция входа
        error_window_title = 'Ошибка авторизации'
        login, password = self.get_data()
        if not self.check_fields(login, password, error_window_title):
            return
        result = self.session.query(Profile).filter(Profile.login == login).first()
        if not result:
            self.show_message('Такого логина не существует', error_window_title)
            return False
        elif password != result.password:
            self.show_message('Неверный логин или пароль', error_window_title)
        else:
            self.parent.proceed(login)  # Переход к основному окну
            self.destroy()  # Самоуничтожение

    def registration(self):  # Функция регистрации
        error_window_title = 'Ошибка регистрации'
        login, password = self.get_data()
        if not self.check_fields(login, password, error_window_title):
            return
        if self.session.query(Profile).filter(Profile.login == login).first():
            self.show_message('Такой логин уже существует', error_window_title)
            return
        messages = []  # Далее - проверка на надёжность пароля
        if len(password) <= 8:
            messages.append('Слишком короткий пароль')
        if password.lower() == password or password.upper() == password:
            messages.append('Буквы должны быть разного регистра')
        if not any([i in password for i in list('0123456789')]):
            messages.append('В пароле должны присутствовать цифры')
        if any([i in password.lower() for i in self.sequences]):
            messages.append('Слишком простой')
        if messages:
            self.show_message('• ' + '\n• '.join(messages), error_window_title)
        else:
            profile = Profile(login=login, password=password)
            self.session.add(profile)
            self.session.commit()
            user = User(profile_id=profile.id)
            self.session.add(user)
            self.session.commit()
            profile.user_id = user.id
            self.session.merge(profile)
            self.session.commit()
            self.parent.proceed(login)  # -/-
            self.destroy()  # -/-
