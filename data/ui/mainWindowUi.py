from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QListWidget, QCalendarWidget, QMenuBar, QMenu, QAction,
                             QToolButton, QStatusBar, QFontComboBox, QLineEdit, QPushButton)


# class CalendarWidget(QCalendarWidget):
#     def __init__(self, *args, **kwargs):
#         super(CalendarWidget, self).__init__(*args, **kwargs)
#         self.last_click_date = None
#
#     def selec(self, event: QMouseEvent) -> None:
#         date = self.selectedDate().toPyDate()
#         if date == self.last_click_date:
#             self.last_click_date = None
#             print(date)
#             print(self.parent().__class__.__name__)


class Ui_MainWindow:  # No comments
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1050, 580)
        font = QFont()
        font.setFamily("Segoe UI Historic")
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QRect(10, 118, 256, 361))
        self.listWidget.setObjectName("listWidget")
        # self.calendarWidget = CalendarWidget(self.centralwidget)
        self.calendarWidget = QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QRect(310, 70, 600, 361))
        self.calendarWidget.setObjectName("calendarWidget")
        self.listWidget.raise_()
        self.listWidget.setStyleSheet("border: 1px solid;border-radius: 3px;")
        self.calendarWidget.raise_()
        self.search_field = QLineEdit(self.centralwidget)
        self.search_field.setGeometry(QRect(self.listWidget.pos().x(), 80, self.listWidget.width() + 12, 30))
        self.search_field.setPlaceholderText('Введите запрос для поиска')
        MainWindow.setCentralWidget(self.centralwidget)

        self.combo_shift = QFontComboBox(self.centralwidget)
        self.combo_shift.resize(150, self.combo_shift.size().height() + 5)
        self.combo_shift.setStyleSheet('background-color:"#ffffff"')

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1043, 26))
        self.menubar.setObjectName("menubar")
        self.note_menu = QMenu(self.menubar)
        self.note_menu.setObjectName("menu")

        self.font_menu = QMenu(self.menubar)
        self.font_menu.setObjectName("menu")

        self.alignment_menu = QMenu(self.menubar)
        self.alignment_menu.setObjectName("menu")

        self.note_menu = QMenu(self.menubar)
        self.note_menu.setObjectName("menu")

        self.task_menu = QMenu(self.menubar)
        self.task_menu.setObjectName("menu")

        self.category_menu = QMenu(self.menubar)
        self.category_menu.setObjectName("menu")

        self.category_action = QAction(MainWindow)
        self.category_action.setObjectName('category_action')
        self.category_action.setShortcut('Ctrl+W')
        self.category_menu.addAction(self.category_action)

        self.settings_menu = QMenu(self.menubar)
        self.settings_menu.setObjectName("menu")

        self.theme_menu = QMenu(self.menubar)
        self.theme_menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)

        self.green = QAction(MainWindow)
        self.green.setCheckable(True)
        self.green.setChecked(False)
        self.purple = QAction(MainWindow)
        self.purple.setCheckable(True)
        self.purple.setChecked(False)
        self.blue = QAction(MainWindow)
        self.blue.setCheckable(True)
        self.blue.setChecked(False)
        self.white = QAction(MainWindow)
        self.white.setCheckable(True)
        self.white.setChecked(False)
        theme_menu_actions = [self.white, self.blue, self.green, self.purple]
        self.theme_menu.addActions(theme_menu_actions)

        self.note_tool = QToolButton(self.centralwidget)
        self.note_tool.setText('Заметки')
        self.note_tool.setStyleSheet('background-color: white;border-style: solid; border-width: 1px;'
                                     ' border-color: black')
        self.note_tool.setCheckable(True)
        self.task_tool = QToolButton(self.centralwidget)
        self.task_tool.setText('Задачи')
        self.task_tool.setStyleSheet('background-color: white;border-style: solid; border-width: 1px;'
                                     ' border-color: black;')
        self.task_tool.setCheckable(True)

        self.bold_tool = QToolButton(self.centralwidget)
        self.bold_tool.setStyleSheet('font-weight:bold;')
        self.bold_tool.setText('B')
        self.bold_tool.resize(26, self.bold_tool.size().height())

        self.italic_tool = QToolButton(self.centralwidget)
        self.italic_tool.setStyleSheet('font-style: italic;')
        self.italic_tool.setText('I')
        self.italic_tool.resize(26, self.italic_tool.size().height())

        self.underline_tool = QToolButton(self.centralwidget)
        self.underline_tool.setStyleSheet('text-decoration: underline;')
        self.underline_tool.setText('U')
        self.underline_tool.resize(24, self.underline_tool.size().height())

        self.overline_tool = QToolButton(self.centralwidget)
        self.overline_tool.setStyleSheet('text-decoration: overline;')
        self.overline_tool.setText('O')
        self.overline_tool.resize(26, self.overline_tool.size().height())

        self.strike_out_tool = QToolButton(self.centralwidget)
        self.strike_out_tool.setStyleSheet('text-decoration: line-through;')
        self.strike_out_tool.setText('ABC')
        self.strike_out_tool.resize(27, self.strike_out_tool.size().height())
        # self.strike_out_tool.setStyleSheet('color:"#ffffff"')

        self.save_btn = QPushButton(self.centralwidget)
        self.save_btn.setText('Сохранить')
        self.save_btn.resize(125, 40)
        self.save_btn.hide()

        self.shif_tools = [self.bold_tool, self.italic_tool,
                           self.underline_tool, self.overline_tool,
                           self.strike_out_tool]

        for tool in self.shif_tools:
            tool.setStyleSheet('background:"#ffffff"')

        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.add_action = QAction(MainWindow)
        self.add_action.setObjectName("add_action")
        self.add_action.setShortcut("Ctrl+N")

        self.delete_action = QAction(MainWindow)
        self.delete_action.setObjectName("delete_action")
        self.delete_action.setShortcut("Delete")

        self.save_action = QAction(MainWindow)
        self.save_action.setObjectName("save_action")
        self.save_action.setShortcut("Ctrl+S")

        self.insert_image_action = QAction(MainWindow)
        self.insert_image_action.setObjectName("insert_image_action")
        self.insert_image_action.setShortcut("Ctrl+O")

        self.show_all_action = QAction(MainWindow)
        self.show_all_action.setObjectName("show_all_action")
        self.show_all_action.setShortcut("Ctrl+K")

        self.add_task_action = QAction(MainWindow)
        self.add_task_action.setObjectName("add_task_action")
        self.add_task_action.setShortcut('Ctrl+N')

        self.delete_task_action = QAction(MainWindow)
        self.delete_task_action.setObjectName('delete_task_action')
        self.delete_task_action.setShortcut('Delete')

        self.close_task_action = QAction(MainWindow)
        self.close_task_action.setObjectName('close_task_action')
        self.close_task_action.setShortcut('Ctrl+Q')

        self.handle_categories_action = QAction(MainWindow)
        self.handle_categories_action.setObjectName('handle_categories_action')
        self.handle_categories_action.setShortcut('Ctrl+Tab')

        note_actions = [self.add_action, self.delete_action,
                        self.save_action, self.insert_image_action,
                        self.show_all_action, self.handle_categories_action]
        self.note_menu.addActions(note_actions)

        task_actions = [self.add_task_action, self.delete_task_action, self.close_task_action,
                        self.save_action, self.insert_image_action, self.show_all_action,
                        self.handle_categories_action]
        self.task_menu.addActions(task_actions)

        self.saving_action = QAction(MainWindow)
        self.saving_action.setCheckable(True)
        self.saving_action.setChecked(False)

        self.settings_menu.addAction(self.saving_action)

        self.format_bold = QAction(MainWindow)
        self.format_bold.setShortcut('Ctrl+B')
        self.format_bold.setObjectName("format_bold")

        self.format_italic = QAction(MainWindow)
        self.format_italic.setShortcut('Ctrl+I')
        self.format_italic.setObjectName("format_italic")

        self.format_underline = QAction(MainWindow)
        self.format_underline.setShortcut('Ctrl+U')
        self.format_underline.setObjectName("format_italic")

        self.format_overline = QAction(MainWindow)
        self.format_overline.setShortcut('Ctrl+L')
        self.format_overline.setObjectName("format_italic")

        self.format_strike_out = QAction(MainWindow)
        self.format_strike_out.setShortcut('Ctrl+T')
        self.format_strike_out.setObjectName("format_italic")

        self.format_regular = QAction(MainWindow)
        self.format_regular.setShortcut('Ctrl+D')
        self.format_regular.setObjectName("format_italic")

        self.alignment_right = QAction(MainWindow)
        self.alignment_right.setShortcut('Ctrl+R')
        self.alignment_right.setObjectName("align_right")

        self.alignment_center = QAction(MainWindow)
        self.alignment_center.setShortcut('Ctrl+E')
        self.alignment_center.setObjectName("align_center")

        self.alignment_left = QAction(MainWindow)
        self.alignment_left.setShortcut('Ctrl+F')
        self.alignment_left.setObjectName("align_left")

        font_menu_actions = [self.format_bold, self.format_italic, self.format_underline,
                             self.format_overline, self.format_strike_out, self.format_regular]
        self.font_menu.addActions(font_menu_actions)

        align_menu = [self.alignment_right, self.alignment_center, self.alignment_left]

        self.alignment_menu.addActions(align_menu)

        self.menu_actions = [self.note_menu.menuAction(), self.category_menu.menuAction(),
                             self.font_menu.menuAction(), self.alignment_menu.menuAction(),
                             self.settings_menu.menuAction(), self.theme_menu.menuAction()]
        self.menubar.addActions(self.menu_actions)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Notebook"))
        self.note_menu.setTitle(_translate("MainWindow", "Заметка"))
        self.task_menu.setTitle(_translate("MainWindow", "Задача"))
        self.category_menu.setTitle(_translate("MainWindow", "Категории"))
        self.font_menu.setTitle(_translate("MainWindow", "Шрифт"))
        self.alignment_menu.setTitle(_translate("MainWindow", "Выравнивание"))
        self.alignment_left.setText(_translate("MainWindow", "Выравнивание по левому краю"))
        self.alignment_center.setText(_translate("MainWindow", "Выравнивание по центру"))
        self.alignment_right.setText(_translate("MainWindow", "Выравнивание по правому краю"))
        self.settings_menu.setTitle(_translate("MainWindow", "Настройки"))
        self.theme_menu.setTitle(_translate("MainWindow", "Темы"))
        self.white.setText(_translate("MainWindow", "Белый"))
        self.green.setText(_translate("MainWindow", "Зелёный"))
        self.purple.setText(_translate("MainWindow", "Фиолетовый"))
        self.blue.setText(_translate("MainWindow", "Голубой"))
        self.add_action.setText(_translate("MainWindow", "Создать заметку"))
        self.delete_action.setText(_translate("MainWindow", "Удалить заметку"))
        self.save_action.setText(_translate("MainWindow", "Сохранить"))
        self.insert_image_action.setText(_translate("MainWindow", "Вставить картинку"))
        self.show_all_action.setText(_translate("MainWindow", "Сброс поиска и фильтра по дате"))
        self.add_task_action.setText(_translate("MainWindow", "Создать задачу"))
        self.delete_task_action.setText(_translate("MainWindow", "Удалить задачу"))
        self.close_task_action.setText(_translate("MainWindow", "Отметить задачу выполненной"))
        self.category_action.setText(_translate("MainWindow", "Взаимодействие с категориями"))
        self.handle_categories_action.setText(_translate("MainWindow", "Управление категориями"))
        self.saving_action.setText(_translate("MainWindow", "Автосохранение"))
        self.format_bold.setText(_translate("MainWindow", "Полужирный"))
        self.format_italic.setText(_translate("MainWindow", "Курсив"))
        self.format_underline.setText(_translate("MainWindow", "Нижнее подчеркивание"))
        self.format_overline.setText(_translate("MainWindow", "Верхнее подчеркивание"))
        self.format_strike_out.setText(_translate("MainWindow", "Зачёркивание"))
        self.format_regular.setText(_translate("MainWindow", "Обычный"))
