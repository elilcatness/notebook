from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QPushButton,
                             QListWidget, QLabel, QLineEdit, QDialogButtonBox)


class CategoriesFormUi:
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(570, 488)
        font = QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.create_btn = QPushButton(Form)
        self.create_btn.setObjectName("create_btn")
        self.horizontalLayout.addWidget(self.create_btn)
        self.edit_btn = QPushButton(Form)
        self.edit_btn.setObjectName("edit_btn")
        self.horizontalLayout.addWidget(self.edit_btn)
        self.delete_btn = QPushButton(Form)
        self.delete_btn.setObjectName("delete_btn")
        self.horizontalLayout.addWidget(self.delete_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.status = QLabel(Form)
        self.status.setText("")
        self.status.setObjectName("status")
        self.verticalLayout.addWidget(self.status)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Категории"))
        self.create_btn.setText(_translate("Form", "Создать"))
        self.edit_btn.setText(_translate("Form", "Изменить"))
        self.delete_btn.setText(_translate("Form", "Удалить"))


class CategoryDialogUi:
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(322, 106)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(Dialog)
        font = QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label.setText(_translate("Dialog", "Введите название категории"))


class CategoriesObjFormUi:
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(641, 562)
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        Form.setFont(font)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(Form)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.listWidget = QListWidget(Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Категории"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Введите запрос для поиска"))
