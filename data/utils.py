import datetime as dt
import os

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPalette, QFontMetrics, QStandardItem, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QComboBox, QStyledItemDelegate, qApp

if os.getcwd().split('\\')[-1] != 'data':
    from data.exceptions import InvalidDateFormat
else:
    from exceptions import InvalidDateFormat


class DateFunctions:  # Класс, в который вынесены основные функции преобразования объектов datetime и str
    @staticmethod
    def convert_str_to_dt(raw_string: str) -> dt.datetime:  # Перевод строки в объект даты
        if len(raw_string.split('.')) == 3 and len(raw_string.split(':')) == 2:  # При вызове из добавления дедлайна
            day, month, year = map(int, raw_string.split()[0].split('.'))
            hours, minutes = map(int, raw_string.split()[1].split(':'))
        elif len(raw_string.split('.')) == 3 and len(raw_string.split(':')) == 3:  # При вызове из атрибутов заметок
            day, month, year = map(int, raw_string.split()[0].split('.'))
            hours, minutes, _ = map(int, raw_string.split()[1].split(':'))
        elif len(raw_string.split('-')) == 3 and len(raw_string.split(':')) == 3:  # При преобразования из БД
            year, month, day = map(int, raw_string.split()[0].split('-'))
            hours, minutes, _ = map(int, raw_string.split()[1].split(':'))
        else:
            raise InvalidDateFormat('Неверный формат дедлайна')
        return dt.datetime(year, month, day, hours, minutes)

    @staticmethod
    def convert_dt_to_str(date: dt.datetime) -> str:  # Перевод объекта даты в строку
        date = str(date)
        date = ('.'.join(date.split('.')[0].split()[0].split('-')[::-1])
                + ' ' + date.split()[-1].split('.')[0])
        return date


class FocusGradedText(QTextEdit):  # Переопределяемый класс QTextEdit, использующийся для автосохранения
    def __init__(self, parent: QMainWindow):
        super(FocusGradedText, self).__init__(parent)
        self.parent_wdg = parent  # Определение ссылки на виджета-родителя (MainWindow)

    def focusInEvent(self, _) -> None:
        self.setFocusPolicy(Qt.NoFocus)
        self.setEnabled(True)
        self.setCursorWidth(1)

    def focusOutEvent(self, _) -> None:
        self.parent_wdg.save_object()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setCursorWidth(0)


class CheckableComboBox(QComboBox):
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        self.setItemDelegate(CheckableComboBox.Delegate())

        self.model().dataChanged.connect(self.updateText)

        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, obj, event):
        if obj == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if obj == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)
        self.updateText()

    def timerEvent(self, event):
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res
