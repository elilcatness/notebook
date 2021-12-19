from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit, QComboBox

from data.utils import AddDialog


class NoteAddDialogUi:
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(388, 282)
        font = QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(9)
        Dialog.setFont(font)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_label = QLabel(Dialog)
        self.name_label.setObjectName("name_label")
        self.horizontalLayout.addWidget(self.name_label)
        self.name_edit = QLineEdit(Dialog)
        self.name_edit.setObjectName("name_edit")
        self.horizontalLayout.addWidget(self.name_edit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cat_label = QLabel(Dialog)
        self.cat_label.setObjectName("cat_label")
        self.horizontalLayout_2.addWidget(self.cat_label)
        self.cat_value = QComboBox(Dialog)
        self.cat_value.setObjectName("cat_value")
        self.horizontalLayout_2.addWidget(self.cat_value)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        # self.buttonBox.accepted.connect(Dialog.accept)
        # self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Создание заметки"))
        self.name_label.setText(_translate("Dialog", "Название заметки"))
        self.cat_label.setText(_translate("Dialog", "Категория"))


class NoteAddDialog(AddDialog, NoteAddDialogUi):
    def accept(self):
        name = self.name_edit.text()
        if not name:
            return self.show_message('Заметка не должна быть пустой')
        elif self.parent.check_title(name):
            return self.show_message('Заметка с таким названием уже существует', 'Ошибка создания заметки')
        else:
            self.parent.proceed_adding_note(name, self.cat_value.currentText())
            self.destroy()
