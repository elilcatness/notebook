import datetime as dt

from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox

from data.exceptions import InvalidDateFormat
from data.utils import AddDialog


class TaskAddDialogUi:
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(394, 290)
        font = QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(9)
        Dialog.setFont(font)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.name_edit = QLineEdit(Dialog)
        self.name_edit.setObjectName("name_edit")
        self.horizontalLayout.addWidget(self.name_edit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.deadline_edit = QLineEdit(Dialog)
        self.deadline_edit.setObjectName("deadline_edit")
        self.horizontalLayout_2.addWidget(self.deadline_edit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.cat_value = QComboBox(Dialog)
        self.cat_value.setObjectName("cat_value")
        self.horizontalLayout_3.addWidget(self.cat_value)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Создание задачи"))
        self.label.setText(_translate("Dialog", "Название задачи"))
        self.label_2.setText(_translate("Dialog", "Дедлайн"))
        self.label_3.setText(_translate("Dialog", "Категория"))


class TaskAddDialog(AddDialog, TaskAddDialogUi):
    def __init__(self, parent, deadline_date: str):
        super(TaskAddDialog, self).__init__(parent)
        if deadline_date:
            self.deadline_edit.setText(deadline_date + ' ')

    def accept(self):
        name = self.name_edit.text()
        if not name:
            return self.show_message('Задача не должна быть пустой')
        deadline = self.deadline_edit.text()
        try:
            try:
                deadline = self.parent.convert_str_to_dt(deadline)
            except (IndexError, ValueError, InvalidDateFormat):
                raise InvalidDateFormat('Неверный формат дедлайна')
            if dt.datetime.now() > deadline:
                raise InvalidDateFormat('Неверный формат дедлайна')
        except InvalidDateFormat as e:
            self.show_message(str(e), 'Ошибка создания задачи')
        else:
            self.parent.proceed_adding_task(name, deadline, self.cat_value.currentText())
            self.destroy()
