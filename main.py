import datetime as dt
import os.path
import sys
from typing import Union

from PyQt5 import QtCore, QtWidgets, QtGui
from sqlalchemy.orm import Session

from data import db_session
from data.baseApplicationForm import BaseApplicationForm
from data.categories import CategoriesForm, CategoriesObjForm
from data.category import Category
from data.exceptions import InvalidDateFormat
from data.login import LoginForm
from data.note import Note
from data.profile import Profile
from data.task import Task
from data.ui.mainWindowUi import Ui_MainWindow
from data.ui.noteAddUi import NoteAddDialog
from data.ui.taskAddUi import TaskAddDialog
from data.utils import DateFunctions, FocusGradedText


class Window(QtWidgets.QMainWindow, Ui_MainWindow, BaseApplicationForm, DateFunctions):
    def __init__(self, session: Session):
        super(Window, self).__init__()
        self.setupUi(self)  # Инициализация интерфейса
        self.hide()  # Скрытие основного окна до прохода авторизации
        self.text = None  # Обозначение атрибута поля для ввода текста
        list_widget_position = self.listWidget.pos()  # Текущая позиция списка для размещения кнопок секций
        self.note_tool.move(list_widget_position.x(),
                            self.calendarWidget.pos().y() - self.note_tool.height())  # Размещение кнопок секций
        self.hide_tools()  # Скрытие кнопок форматирования, так как первый виджет после входа - календарь

        self.setMinimumSize(1100, 730)  # Обозначение минимального размера окна для корректного масштабирования
        self.calendarWidget.setMinimumSize(550, 550)  # -/- для календаря

        self.session = session
        self.login_form = None  # Обозначение переменной формы авторизации, дабы она не пропала
        self.authorize()  # Инициализация авторизации
        self.category_form = None  # Обозначение переменной формы взаимодействия с категориями
        self.obj_category_form = None  # Обозначение переменной формы взаимодействия с категориями объекта

        self.add_action.triggered.connect(self.add_object)  # Привязка сигнала к функции создания заметки
        self.delete_action.triggered.connect(self.delete_object)  # Привязка сигнала к функции удаления заметки
        self.add_task_action.triggered.connect(self.add_object)  # Привязка сигнала к функции создания задачи
        self.delete_task_action.triggered.connect(self.delete_object)  # Привязка сигнала к функции удаления задачи
        self.close_task_action.triggered.connect(self.close_task)  # Привязка сигнала к функции выполнения задачи
        self.save_action.triggered.connect(self.save_object)  # Привязка сигнала к функции сохранения объекта
        self.save_btn.clicked.connect(self.save_object)
        self.insert_image_action.triggered.connect(self.insert_image)  # Привязка сигнала к функции вставки изображения
        self.show_all_action.triggered.connect(self.search)  # Привязка сигнала к функции отключения фильтра
        self.category_action.triggered.connect(self.handle_categories)
        self.handle_categories_action.triggered.connect(self.handle_object_categories)
        self.format_bold.triggered.connect(lambda x: self.formatting("make_bold"))  # Далее - функции форматирования
        self.format_italic.triggered.connect(lambda x: self.formatting("make_italic"))
        self.format_underline.triggered.connect(lambda x: self.formatting("make_underline"))
        self.format_overline.triggered.connect(lambda x: self.formatting("make_overline"))
        self.format_strike_out.triggered.connect(lambda x: self.formatting("make_strike_out"))
        self.format_regular.triggered.connect(lambda x: self.formatting("make_regular"))

        self.alignment_right.triggered.connect(lambda x: self.formatting("align_right"))  # Выравнивание справа
        self.alignment_center.triggered.connect(lambda x: self.formatting("align_center"))  # Выравнивание по центру
        self.alignment_left.triggered.connect(lambda x: self.formatting("align_left"))  # Выравнивание слева

        self.bold_tool.clicked.connect(lambda x: self.formatting("make_bold"))  # при нажатии кнопки над полем текста
        self.italic_tool.clicked.connect(lambda x: self.formatting("make_italic"))  # Далее - сигналы форматирования...
        self.underline_tool.clicked.connect(lambda x: self.formatting("make_underline"))
        self.overline_tool.clicked.connect(lambda x: self.formatting("make_overline"))
        self.strike_out_tool.clicked.connect(lambda x: self.formatting("make_strike_out"))

        self.saving_action.triggered.connect(self.manage_saving)  # Привязка сигнала к функции изменения вида сохранения
        self.green.triggered.connect(self.set_theme)  # Далее - смена тем
        self.purple.triggered.connect(self.set_theme)
        self.blue.triggered.connect(self.set_theme)
        self.white.triggered.connect(self.set_theme)

        self.combo_shift.currentFontChanged.connect(self.change_field_font)  # Привязка сигнала к функции изменения
        # шрифта

        self.active_object = None  # Определение переменной активного объекта на данный момент
        self.user = None  # Определение переменной активного пользователя
        self.notes, self.tasks = [], []  # Определения списков заметок и задач
        self.active_section = 'notes'  # Определение переменной активной секции на данный момент
        self.current_theme = None  # Определение переменной активной темы на данный момент

        self.listWidget.itemClicked.connect(self.load_object)  # Привязка нажатия на объект списка к функции загрузки
        self.listWidget.itemDoubleClicked.connect(self.edit_object_title)  # Привязь двойного клика к редактору названия
        self.calendarWidget.selectionChanged.connect(self.add_object)  # Привязка изменения выделенной даты
        # к обработчику

        self.note_tool.clicked.connect(self.change_section)  # Привязка смены секции на заметки к обработчику
        self.task_tool.clicked.connect(self.change_section)  # Привязка смены секции на задачи к обработчику

        self.search_field.textChanged.connect(self.search)

        self.inner_change = False  # Определение внутренней переменной для игнорирования сигнала
        # об изменении текста поля при подгрузке текста объекта из БД
        self.saving_preference = None  # Определение переменной текущего типа сохранения
        self.show_calendar = True  # Техническая переменная для корректного отображения виджетов при смене темы
        self.last_dates = []  # Определение переменной для последних выбранных дат на календаре для очищения оного
        # при смене секций и прочих ситуациях

        self.selected_tools = []  # Определение переменной для выделенных инструментов на данный момент
        self.tools_stylesheets = ['font-weight:bold', 'font-style: italic',
                                  'text-decoration: underline', 'text-decoration: overline',
                                  'text-decoration: line-through']  # Стандартные значения для инструментов

        self.dialog = None  # Диалог создания заметки или задачи

    def search(self, text: str, from_date_refresh=False):
        self.listWidget.clear()
        if text and self.sender() != self.show_all_action:
            if not from_date_refresh:
                self.load_objects(no_list=True)
            if self.active_section == 'notes':
                self.notes = list(filter(lambda x: x.get_title().lower().startswith(text.lower()), self.notes))
                self.listWidget.addItems([x.get_title() for x in self.notes])
            else:
                self.tasks = list(filter(lambda x: x.get_title().lower().startswith(text.lower()), self.tasks))
                self.listWidget.addItems([x.get_title() for x in self.tasks])
        else:
            show_tasks = False if self.active_section == 'notes' else True
            self.load_objects(show_tasks=show_tasks)  # Здесь выбирается, что нужно отобразить именно задачи
            section = self.notes if self.active_section == 'notes' else self.tasks
            if section:  # Дополнительная проверка для корректного отображения после изменения темы
                self.listWidget.item(0).setSelected(True)

    def handle_categories(self):  # Функция, позволяющая настраивать все категории
        self.category_form = CategoriesForm(self)
        self.category_form.show()

    def handle_object_categories(self):  # Функция, позволяющая настраивать категории выбранного объекта
        if self.active_object and not self.calendarWidget.isVisible():
            self.obj_category_form = CategoriesObjForm(self)
            self.obj_category_form.show()
        else:
            if self.active_section == 'notes':
                self.status_bar.showMessage('Заметка должна быть открыта')
            elif self.active_section == 'tasks':
                self.status_bar.showMessage('Задача должна быть открыта')

    def change_field_font(self, font: QtGui.QFont) -> None:  # Обработчик изменений шрифта
        if self.active_object and not self.calendarWidget.isVisible():
            self.active_object.change_font(font)
            self.unselect_tools()
        else:
            if self.active_section == 'notes':
                self.status_bar.showMessage('Заметка должна быть открыта')
            elif self.active_section == 'tasks':
                self.status_bar.showMessage('Задача должна быть открыта')

    def hide_tools(self) -> None:  # Скрывает в нужный момент инструменты форматирования
        for elem in self.shif_tools:
            elem.hide()
        self.combo_shift.hide()

    def clear_calendar(self) -> None:  # Очищает календарь от отмеченных дат, дабы отобразить новые
        for date in self.last_dates:
            date_fmt = QtGui.QTextCharFormat()
            date_fmt.setBackground(QtGui.QColor(255, 255, 255))
            self.calendarWidget.setDateTextFormat(date, date_fmt)

    def repaint_calendar(self) -> None:  # Отмечает даты, в которых действующие объекты были созданы/имеют дедлайн
        if self.last_dates:
            self.clear_calendar()
            self.last_dates = []
        self.calendarWidget.setStyleSheet('background-color:"#ffffff"; '
                                          'color:"#000000";')
        self.calendarWidget.repaint()
        dates = ([x.get_date_dt() for x in self.notes] if self.active_section == 'notes'
                 else [x.get_deadline_dt() for x in self.tasks])
        non_repeated_dates = set(dates)
        for date in non_repeated_dates:
            count = dates.count(date)
            if 1 <= count <= 2:
                color = QtGui.QColor(247, 250, 101)
            elif 3 <= count <= 5:
                color = QtGui.QColor(255, 156, 57)
            else:
                color = QtGui.QColor(255, 72, 72)
            date_fmt = QtGui.QTextCharFormat()
            date_fmt.setBackground(color)
            self.calendarWidget.setDateTextFormat(date, date_fmt)
        self.last_dates = dates[:]

    def change_section(self) -> None:  # Осуществляет переход от одной секции к другой
        if self.saving_preference == 'auto':
            self.text.clearFocus()
        if self.active_object and self.show_calendar:
            self.active_object.change_open(False)
            self.active_object = None
            self.text.hide()
            self.hide_tools()
            self.calendarWidget.show()
        self.listWidget.clear()
        sender = self.sender().text()
        tools = [self.note_tool, self.task_tool]
        current_tool, other_tool = ((tools[0], tools[1]) if sender == 'Заметки'
                                    else (tools[1], tools[0]))
        if other_tool.isChecked():
            other_tool.setChecked(False)
            other_tool.setStyleSheet('background-color: white;border-style: solid;'
                                     'border-width: 1px;border-color: black')
        text_color = 'black' if self.current_theme == 'Белый' else 'white'
        color = self.get_selection_color()
        current_tool.setChecked(True)
        current_tool.setStyleSheet('background-color: white;border-style: solid; border-width: 1px;'
                                   'border-color: black;background: %s;color: %s' % (color,
                                                                                     text_color))
        self.active_section = 'notes' if current_tool == self.note_tool else 'tasks'
        section = self.notes if self.active_section == 'notes' else self.tasks
        self.listWidget.addItems([x.get_title() for x in section])
        section_to_tool_translation = {self.note_tool: (self.note_menu, self.task_menu),
                                       self.task_tool: (self.task_menu, self.note_menu)}
        self.menubar.removeAction(section_to_tool_translation[current_tool][1].menuAction())
        self.menubar.insertAction(self.font_menu.menuAction(),
                                  section_to_tool_translation[current_tool][0].menuAction())
        if self.active_section == 'tasks':
            self.repaint_task_list()
        if self.show_calendar:
            self.repaint_calendar()
            # self.calendarWidget.setSelectedDate(dt.date.today())

    def insert_image(self) -> None:  # Обработчик вставки изображения в поле для ввода текста
        if not self.active_object or self.calendarWidget.isVisible():
            self.status_bar.showMessage('Для вставки картинки должна быть открыта заметка')
        else:
            filename = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Выбрать картинку', '',
                'Картинка (*.jpg);;Картинка (*.png);;'
                'Картинка (*.bmp);;Картинка (*.webm)')[0]
            if filename:
                # self.saving_action.trigger()
                # self.save_object()
                self.active_object.insert_picture(filename)
                # self.saving_action.trigger()

    def set_theme(self) -> None:  # Осуществляет применение новой темы
        if self.active_section == 'tasks':
            self.repaint_task_list()
        if (not self.purple.isChecked() and not self.green.isChecked()
            and not self.blue.isChecked()) or self.sender().text() == 'Белый':
            self.user.profile.set_preferred_theme('Белый', self.session)
            self.current_theme = 'Белый'
            self.green.setChecked(False)
            self.blue.setChecked(False)
            self.purple.setChecked(False)
            self.white.setChecked(True)
            self.menubar.setStyleSheet('')
            self.calendarWidget.setStyleSheet('')
            self.setStyleSheet('')
            self.search_field.setStyleSheet('')
            self.listWidget.setStyleSheet('border: 1px solid;border-radius: 3px;')
        elif self.sender().text() == 'Фиолетовый':
            self.current_theme = 'Фиолетовый'
            self.user.profile.set_preferred_theme('Фиолетовый', self.session)
            self.green.setChecked(False)
            self.blue.setChecked(False)
            self.white.setChecked(False)
            self.menubar.setStyleSheet('background-color:"#f4e9ff";'
                                       ' selection-background-color: "#af8eb5";')
            self.calendarWidget.setStyleSheet('background-color:"#ffffff"; '
                                              'color:"#000000";')
            self.setStyleSheet('background-color:"#fff7ff"')
            self.listWidget.setStyleSheet('background-color:"#ffffff";border: 1px solid;'
                                          'border-radius: 3px;')
            self.search_field.setStyleSheet('background-color:"#ffffff"')
        elif self.sender().text() == 'Зелёный':
            self.current_theme = 'Зелёный'
            self.user.profile.set_preferred_theme('Зелёный', self.session)
            self.purple.setChecked(False)
            self.blue.setChecked(False)
            self.white.setChecked(False)
            self.menubar.setStyleSheet('background-color:"#a5d6a7"; '
                                       'selection-background-color: "#75a478";')
            self.calendarWidget.setStyleSheet('background-color:"#ffffff"; color:"#000000";')
            self.setStyleSheet('background-color:"#d7ffd9"')
            self.listWidget.setStyleSheet('background-color:"#ffffff";border: 1px solid;'
                                          'border-radius: 3px;')
            self.search_field.setStyleSheet('background-color:"#ffffff"')
        elif self.sender().text() == 'Голубой':
            self.current_theme = 'Голубой'
            self.user.profile.set_preferred_theme('Голубой', self.session)
            self.purple.setChecked(False)
            self.green.setChecked(False)
            self.white.setChecked(False)
            self.menubar.setStyleSheet('background-color:"#64b5f6"; selection-background-color: "#0077c2";')
            self.calendarWidget.setStyleSheet('background-color:"#ffffff"; color:"#000000";')
            self.setStyleSheet('background-color:"#9be7ff"')
            self.listWidget.setStyleSheet('background-color:"#ffffff"; border: 1px solid;'
                                          'border-radius: 3px;')
            self.search_field.setStyleSheet('background-color:"#ffffff"')
        self.bold_tool.setStyleSheet('font-weight:bold;background: #ffffff')
        self.italic_tool.setStyleSheet('font-style: italic;background: #ffffff')
        self.underline_tool.setStyleSheet('text-decoration: underline;background: #ffffff')
        self.overline_tool.setStyleSheet('text-decoration: overline;background: #ffffff')
        self.strike_out_tool.setStyleSheet('text-decoration: line-through;background: #ffffff')
        self.show_calendar = not bool(self.active_object)
        if self.active_section == 'notes':
            self.note_tool.click()
        elif self.active_section == 'tasks':
            self.task_tool.click()
        if self.active_object:
            section = self.notes if self.active_section == 'notes' else self.tasks
            idx = section.index(self.active_object)
            self.listWidget.item(idx).setSelected(True)
        for tool in self.selected_tools:
            self.set_tool_selected(tool)
        self.show_calendar = True

    def manage_saving(self) -> None:  # Применяет новый способ сохранения
        if self.text.isVisible():
            self.text.hide()
        self.text.destroy()
        self.text = None
        if self.saving_action.isChecked():
            self.saving_preference = 'auto'
            self.save_object()
            self.text = FocusGradedText(self)
        else:
            self.saving_preference = 'manual'
            self.text = QtWidgets.QTextEdit(self)
        self.user.profile.set_saving_preference(self.saving_preference, self.session)
        section = self.notes if self.active_section == 'notes' else self.tasks
        for obj in section:
            obj.set_text_field(self.text)
        self.setup_text_field()
        if not self.calendarWidget.isVisible():
            self.text.show()
        self.initiate_resize_event()
        if self.active_object and not self.calendarWidget.isVisible():
            # Здесь inner_change используется для того, чтобы игнорировался сигнал изменения текста
            self.inner_change = True
            idx = section.index(self.active_object)
            item = self.listWidget.item(idx)
            title = item.text()
            if title.endswith('*'):
                item.setText(title[:-1])
            self.active_object.show()
            self.inner_change = False

    def get_selection_color(self) -> str:  # Возвращает цвет выделения при текущей теме
        translate = {'Белый': '#cce8ff', 'Зелёный': '#75a478',
                     'Голубой': '#0077c2', 'Фиолетовый': '#af8eb5'}
        return translate[self.current_theme]

    def unselect_tools(self) -> None:  # Снимает выделения инструментов
        for tool, func in zip(self.shif_tools, self.tools_stylesheets):
            tool.setStyleSheet('%s;background: #ffffff' % func)

    def set_tool_selected(self, sender: Union[QtWidgets.QAction, QtWidgets.QToolButton]) -> None:
        # Выделяет нажатый инструмент
        if sender in self.alignment_menu.actions():
            return
        elif sender == self.format_regular:
            self.unselect_tools()
            return
        tools_with_styles = list(zip(self.shif_tools, self.tools_stylesheets))
        sender_list = (self.font_menu.actions() if isinstance(sender, QtWidgets.QAction)
                       else self.shif_tools)
        translate = dict(zip(sender_list, tools_with_styles))
        obj, stylesheet = translate[sender]
        color = (self.get_selection_color() if 'background: #ffffff' in obj.styleSheet().split(';')
                 else '#ffffff')
        obj.setStyleSheet('background: %s;%s' % (color, stylesheet))
        if color != '#ffffff' and obj not in self.selected_tools:
            self.selected_tools.append(obj)
        elif obj in self.selected_tools:
            self.selected_tools.pop(self.selected_tools.index(obj))

    def formatting(self, make: str) -> None:  # Изменяет шрифт в текущем поле
        if self.active_object and not self.calendarWidget.isVisible():
            eval('self.active_object.%s()' % make)
            self.set_tool_selected(self.sender())
        else:
            if self.active_section == 'notes':
                self.status_bar.showMessage('Заметка должна быть открыта')
            elif self.active_section == 'tasks':
                self.status_bar.showMessage('Задача должна быть открыта')

    def check_title(self, title: str) -> bool:  # Проверяет, уникально ли название объекта (заметки)
        return len(self.listWidget.findItems(title, QtCore.Qt.MatchFixedString)) == 1

    def handle_changing_text(self) -> None:  # Обработчик изменений в текстовом поле
        if not self.inner_change and self.saving_preference == 'manual':
            title = self.listWidget.selectedItems()[0].text()
            if not title.endswith('*'):
                self.listWidget.selectedItems()[0].setText(title + '*')
        if not self.text.toPlainText():
            self.combo_shift.setCurrentFont(QtGui.QFont('Consolas', 12))
            self.unselect_tools()

    def initiate_resize_event(self) -> None:  # Перемасштабирование для корректного отображения
        size = self.size()
        x, y = size.width(), size.height()
        self.resize(x + 1, y)
        self.resize(x, y)

    def setup_text_field(self) -> None:  # Инициализирует поля для ввода текста
        self.text.setGeometry(QtCore.QRect(310, 95, 711, 431))
        self.text.setObjectName("text")
        self.text.raise_()
        self.text.setFont(QtGui.QFont('Consolas', 12))
        self.text.setStyleSheet('border: 1px solid;border-radius: 3px;')
        self.text.hide()
        self.text.textChanged.connect(self.handle_changing_text)

    def get_object(self, item: QtWidgets.QListWidgetItem) -> Union[Note, Task]:
        # Возвращает объект по индексу выделенного элемента в QListWidget
        idx = self.listWidget.indexFromItem(item).row()
        section = self.notes if self.active_section == 'notes' else self.tasks
        return section[idx]

    def handle_opened_editor(self) -> bool:  # Закрывает действующие редакторы названия объектов
        i = 0
        item = self.listWidget.item(i)
        while item:
            i += 1
            item = self.listWidget.item(i) if i > 1 else item
            if self.listWidget.isPersistentEditorOpen(item):
                item.setSelected(True)
                return self.close_editor(message=False)
        return True

    def load_object(self, clicked_item: QtWidgets.QListWidgetItem) -> None:
        # Загружает объект, поле для ввода или календарь в зависимости от количества предыдущих нажатий по элементу
        self.unselect_tools()
        self.status_bar.showMessage('')
        if self.listWidget.isPersistentEditorOpen(clicked_item):
            return
        if not self.handle_opened_editor() and self.active_section == 'notes':
            self.show_message('Название предыдущей заметки с открытым редактором заголовка занято',
                              'Ошибка заметки')
            return
        self.inner_change = True
        obj = self.get_object(clicked_item)
        obj.show()
        if self.active_object:
            self.active_object.make_regular()
            if self.active_object != obj:
                self.active_object.change_open(False)
                self.active_object = obj
            section = self.notes if self.active_section == 'notes' else self.tasks
            idx = section.index(self.active_object)
            clicked_item = self.listWidget.item(idx)
            last_title = clicked_item.text()
            if last_title.endswith('*'):
                clicked_item.setText(last_title[:-1])
        if self.calendarWidget.isVisible() or not obj.is_opened():
            self.active_object = obj
            obj.change_open(True)
            self.calendarWidget.hide()
            for elem in self.shif_tools:
                elem.show()
            self.text.show()
            self.save_btn.show()
            # На данном этапе инициализируется прожатие инструментов, кои уже были применены до этого
            document = self.text.document()
            cursor = QtGui.QTextCursor(document)
            cursor.setPosition(document.characterCount() - 1)
            cursor.movePosition(QtGui.QTextCursor.End)
            self.text.setTextCursor(cursor)
            translate = ['is_bold', 'is_italic', 'is_underlined', 'is_overlined', 'is_striked_out']
            for i in range(len(self.shif_tools)):
                if eval('obj.%s()' % translate[i]):
                    self.set_tool_selected(self.shif_tools[i])
            self.combo_shift.show()
            title, date = self.active_object.get_title(), self.active_object.get_date_str()
            categories = ', '.join([cat.name for cat in self.active_object.categories])
            status = ('%s. Дата создания: %s.%s' % (title, date,
                                                    (' Категории: %s' % categories) if categories else '')
                      if self.active_section == 'notes'
                      else '%s. Дата создания: %s. Дедлайн: %s.%s'
                           % (title, date, obj.get_deadline_str(),
                              (' Категории: %s' % categories) if categories else ''))
            self.status_bar.showMessage(status)
        else:
            obj.change_open(False)
            self.text.hide()
            self.hide_tools()
            self.save_btn.hide()
            self.calendarWidget.show()
        clicked_item.setSelected(True)
        self.inner_change = False

    def load_objects(self, no_list=False, show_tasks=False) -> None:  # Подгружает все объекты из БД в память
        self.notes = self.session.query(Note).all()
        for note in self.notes:
            note.__init__(self.session, self.text, note.title, note.body, note.user_id, note.date)
        self.tasks = self.session.query(Task).all()
        for task in self.tasks:
            task.__init__(self.session, self.text, task.title, task.body, task.user_id, task.date,
                          task.deadline, task.closed)
        if not no_list:
            if not show_tasks:
                self.listWidget.addItems([x.get_title() for x in self.notes])
            else:
                self.listWidget.addItems([x.get_title() for x in self.tasks])
                self.repaint_task_list()
            self.repaint_calendar()
        elif show_tasks:
            self.repaint_task_list()

    def save_object(self) -> None:  # Инициализирует сохранение объекта
        item = self.listWidget.selectedItems()
        if not item:
            return
        item = item[0]
        title = item.text()
        if title.endswith('*'):
            item.setText(title[:-1])
        try:
            obj = self.get_object(item)
            obj.save()
            self.status_bar.showMessage('Изменения в %s были успешно сохранены.' % obj.title)
        except IndexError:
            field_name = 'Заметка' if self.active_section == 'notes' else 'Задача'
            self.show_message('%s ещё не была создана, нажмите Enter в названии заметки,'
                              ' чтобы её создать' % field_name, 'Ошибка сохранения')
            self.text.hide()
            self.calendarWidget.show()

    def proceed(self, login: str) -> None:  # Инициализирует работу основного окна после авторизации
        self.user = self.session.query(Profile).filter(Profile.login == login).first().user
        self.saving_preference = self.user.profile.saving_preference
        if self.saving_preference == 'manual':
            self.text = QtWidgets.QTextEdit(self)
        elif self.saving_preference == 'auto':
            self.saving_action.setChecked(True)
            self.text = FocusGradedText(self)
        theme = self.user.profile.theme
        theme_objects = {'Зелёный': self.green, 'Фиолетовый': self.purple,
                         'Голубой': self.blue, 'Белый': self.white}
        theme_objects[theme].trigger()
        self.setup_text_field()
        self.load_objects()
        self.task_tool.click()
        self.note_tool.click()
        self.show()

    def authorize(self) -> None:  # Проводит авторизацию, открывая форму
        self.login_form = LoginForm(self.session, self)
        self.login_form.show()

    def change_widgets(self, instruction: str) -> None:  # Варьирует календарь и текстовое поле
        if instruction == 'field -> calendar':
            self.text.hide()
            self.calendarWidget.show()
            self.repaint_calendar()
            self.hide_tools()
        elif instruction == 'calendar -> field':
            self.calendarWidget.hide()
            self.text.show()

    def delete_object(self):  # Удаляет выделенный объект
        if self.active_object and not self.calendarWidget.isVisible():
            section = self.notes if self.active_section == 'notes' else self.tasks
            idx = section.index(self.active_object)
            self.active_object.delete()
            self.active_object = None
            if self.active_section == 'notes':
                self.notes = self.notes[:idx] + self.notes[idx + 1:]
            else:
                self.tasks = self.tasks[:idx] + self.tasks[idx + 1:]
            self.listWidget.takeItem(idx)
            self.inner_change = True
            idx = idx if idx < len(section) - 1 else idx - 1
            item = self.listWidget.item(idx)
            if item:
                obj = self.get_object(self.listWidget.item(idx))
                self.active_object = obj
                self.listWidget.item(idx).setSelected(True)
                obj.show()
                self.inner_change = False
            else:
                self.change_widgets('field -> calendar')
            self.repaint_calendar()
        else:
            field_name = 'Заметка' if self.active_section == 'notes' else 'Задача'
            self.status_bar.showMessage('%s должна быть открыта' % field_name)

    def add_object(self) -> None:  # Добавляет новый объект в список
        deadline_date = (self.calendarWidget.selectedDate().toPyDate().strftime('%d.%m.%Y')
                         if self.calendarWidget.isVisible() else None)
        self.inner_change = True
        self.text.setText('')
        self.inner_change = False
        self.dialog = NoteAddDialog(self) if self.active_section == 'notes' else TaskAddDialog(self, deadline_date)
        self.dialog.show()

    def proceed_adding_note(self, title: str, category: str):
        self.listWidget.addItem(QtWidgets.QListWidgetItem(title))
        item = self.listWidget.item(self.listWidget.count() - 1)
        self.listWidget.setFocus()
        if self.active_object:
            self.active_object.change_open(False)
        item.setSelected(True)
        note = Note(self.session, self.text, title, '', self.user.profile.id, dt.datetime.now())
        self.notes.append(note)
        self.session.add(note)
        self.session.commit()
        if not self.session.query(Category).filter(Category.name == category).first():
            category = Category(name=category)
            self.session.add(category)
            self.session.commit()
        else:
            category = self.session.query(Category).filter(Category.name == category).first()
        note.categories.append(category)
        self.session.add(note)
        self.session.commit()
        self.active_object = self.notes[-1]
        self.change_widgets('calendar -> field')
        self.active_object.edit_title(title)
        self.load_object(item)
        self.repaint_calendar()

    def proceed_adding_task(self, title: str, deadline: dt.datetime, category: str):
        self.listWidget.addItem(QtWidgets.QListWidgetItem(title))
        item = self.listWidget.item(self.listWidget.count() - 1)
        self.listWidget.setFocus()
        if self.active_object:
            self.active_object.change_open(False)
        item.setSelected(True)
        task = Task(self.session, self.text, 'Новая задача', '', self.user.profile.id,
                    dt.datetime.now(), deadline, False)
        self.tasks.append(task)
        self.session.add(task)
        self.session.commit()
        if not self.session.query(Category).filter(Category.name == category).first():
            category = Category(name=category)
            self.session.add(category)
            self.session.commit()
        else:
            category = self.session.query(Category).filter(Category.name == category).first()
        task.categories.append(category)
        self.session.add(task)
        self.active_object = self.tasks[-1]
        self.change_widgets('calendar -> field')
        self.active_object.edit_title(title)
        self.load_object(item)
        self.repaint_calendar()

    def edit_object_title(self, item: QtWidgets.QListWidgetItem) -> None:
        # Открывает редактор названия выделенного объекта
        self.status_bar.showMessage('')
        self.listWidget.openPersistentEditor(item)
        item.setSelected(True)

    @staticmethod
    def paint_item(item: QtWidgets.QListWidgetItem, status: str) -> None:  # Окрашивает объект задачи в списке
        if item:
            color = QtGui.QColor(134, 223, 145) if status == 'closed' else QtGui.QColor(255, 72, 72)
            item.setBackground(color)

    def repaint_task_list(self) -> None:  # Перекрашивает объекты задач после каких-либо изменений
        for i, task in enumerate(self.tasks):
            if task.is_expired():
                status = 'expired'
            elif task.is_closed():
                status = 'closed'
            else:
                continue
            self.paint_item(self.listWidget.item(i), status)

    def add_task_deadline(self) -> None:  # Добавляет пустую задачу с введённым дедлайном в список (не внося в БД)
        deadline, ok_pressed = QtWidgets.QInputDialog.getText(self, 'Создание задачи',
                                                              'Введите дедлайн (дд.мм.гггг чч:мм)')
        if not ok_pressed:
            return
        date = self.convert_dt_to_str(dt.datetime.now())
        try:
            try:
                deadline = self.convert_str_to_dt(deadline)
            except (IndexError, ValueError, InvalidDateFormat):
                raise InvalidDateFormat('Неверный формат дедлайна')
            if dt.datetime.now() > deadline:
                raise InvalidDateFormat('Неверный формат дедлайна')
        except InvalidDateFormat as e:
            self.status_bar.showMessage(str(e))
        else:
            task = Task(self.session, self.text, 'Новая задача', '', self.user.profile.id,
                        date, deadline, False)
            self.session.add(task)
            self.session.commit()
            self.tasks.append(task)
            self.active_object = self.tasks[-1]
            self.repaint_calendar()
            self.add_object()

    def close_task(self) -> None:  # Отмечает задачу выполненной
        items = self.listWidget.selectedItems()
        if items:
            item = items[0]
            task = self.get_object(item)
            if not task.is_closed():
                result = task.close()
                if result:
                    self.paint_item(item, 'closed')
                else:
                    self.status_bar.showMessage('Задача уже была просрочена')
            else:
                self.status_bar.showMessage('Задача уже была закрыта')
        else:
            self.status_bar.showMessage('Задача должна быть открыта')

    def position_section_bar(self) -> None:  # Относительно позиционирует кнопки секций
        tool_width = self.listWidget.size().width() // 2 - 1
        self.note_tool.resize(tool_width, self.note_tool.height())
        self.task_tool.move(self.note_tool.pos().x() + tool_width + 2, self.note_tool.pos().y())
        self.task_tool.resize(tool_width, self.task_tool.height())

    def position_tool_bar(self):  # Относительно позиционирует инструменты
        pos_tool_y = self.text.pos().y() - 60
        self.bold_tool.move(self.text.pos().x(), pos_tool_y)
        for i in range(1, len(self.shif_tools)):
            self.shif_tools[i].move(self.shif_tools[i - 1].pos().x()
                                    + self.shif_tools[i - 1].size().width() + 4, pos_tool_y)
        self.combo_shift.move(self.strike_out_tool.pos().x() + self.strike_out_tool.size().width() + 4,
                              pos_tool_y)
        self.save_btn.move(self.text.pos().x() + self.text.width() - self.save_btn.width(),
                           self.text.pos().y() - self.save_btn.height() - 30)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:  # Обработчик изменения размера окна
        size = event.size()
        x, y = size.width(), size.height()
        self.listWidget.resize(int(x / 4.07), int(y / 1.3))
        self.search_field.resize(self.listWidget.width(), self.search_field.height())
        self.text.setStyleSheet('background-color:"#ffffff";border: 1px solid;border-radius: 3px;')
        widgets_to_adjust = [self.calendarWidget, self.text]
        for wdg in widgets_to_adjust:
            wdg.move(int(x / 3.5), wdg.pos().y())
            wdg.resize(int(x / 1.4 - 10), int(y / 1.2))
        self.position_section_bar()
        self.position_tool_bar()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # Обработчик закрытия окна
        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Question)
        box.setWindowTitle('Информация')
        box.setText('Вы уверены, что хотите уйти?')
        box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        button_yes = box.button(QtWidgets.QMessageBox.Yes)
        button_yes.setText('Да')
        button_no = box.button(QtWidgets.QMessageBox.No)
        button_no.setText('Нет')
        box.exec_()
        if box.clickedButton() == button_yes:
            event.accept()
            self.load_objects(show_tasks=True)
            for task in self.tasks:
                if task.get_title() == '':
                    task.delete()
            QtWidgets.qApp.quit()
        else:
            event.ignore()

    def close_editor(self, message=True) -> bool:  # Обработчик закрытия редактора названия, применения изменений
        try:
            item = self.listWidget.selectedItems()[0]
        except IndexError:
            return True
        if self.listWidget.isPersistentEditorOpen(item):
            section = self.notes if self.active_section == 'notes' else self.tasks
            self.listWidget.closePersistentEditor(item)
            title = item.text()
            self.inner_change = True
            idx = self.listWidget.indexFromItem(item).row()
            title_is_available = (True if idx < len(section) and self.get_object(item).get_title()
                                          == title or self.active_section == 'tasks'
                                  else self.check_title(title))
            try:
                obj = self.get_object(item)
                if not title_is_available:
                    field_name = 'заметки' if self.active_section == 'notes' else 'задачи'
                    self.show_message('Данное название уже занято', 'Ошибка создания %s' % field_name)
                    self.edit_object_title(item)
                    return False
                else:
                    if self.calendarWidget.isVisible():
                        self.calendarWidget.hide()
                    self.active_object = obj
                    self.active_object.edit_title(title)
                    self.load_object(item)
                    return True
            # IndexError будет пойман только в случае того, что в данный момент объектом является заметка
            except IndexError:
                if not title_is_available:
                    if message:
                        self.show_message('Данное название уже занято', 'Ошибка создания заметки')
                    self.edit_object_title(item)
                    return False
                else:
                    date = self.convert_dt_to_str(dt.datetime.now())
                    note = Note(self.session, self.text, title, '', self.user.profile.id, date)
                    self.notes.append(note)
                    self.session.add(note)
                    self.session.commit()
                    self.active_object = self.notes[-1]
                    self.change_widgets('calendar -> field')
                    self.active_object.edit_title(title)
                    self.load_object(item)
                    self.repaint_calendar()
            finally:
                self.inner_change = False

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:  # Обработчик нажатия клавиш
        if event.key() == QtCore.Qt.Key_Return:
            self.close_editor()


if __name__ == '__main__':
    with open(os.path.join('data', 'db_data.txt'), encoding='utf-8') as f:
        db_session.global_init(f.read().replace('\n', ' '))
    app = QtWidgets.QApplication(sys.argv)
    wnd = Window(db_session.create_session())
    sys.exit(app.exec())
