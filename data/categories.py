from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QDialog, QListWidgetItem

from .category import Category
from .ui.categoriesUi import CategoriesFormUi, CategoryDialogUi, CategoriesObjFormUi


class CategoriesDialog(QDialog, CategoryDialogUi):
    def __init__(self, parent, title: str, inner_text: str = ''):
        super(CategoriesDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle(title)

        self.parent = parent
        self.inner_text = inner_text
        if self.inner_text:
            self.lineEdit.setText(inner_text)

        self.accepted.connect(self.validate_accept)

    def validate_accept(self):
        items_found = len(self.parent.listWidget.findItems(self.lineEdit.text(),
                                                           Qt.MatchFixedString))
        if not self.lineEdit.text():
            self.parent.status.setText('Категория должна иметь название')
        else:
            session = self.parent.parent.session
            if self.inner_text:
                if items_found > 1:
                    return self.parent.status.setText('Такая категория уже есть')
                category = session.query(Category).filter(
                    Category.name == self.inner_text).first()
                category.name = self.lineEdit.text()
                session.merge(category)
                session.commit()
                self.parent.status.setText('Категория "%s" была успешно изменена на "%s"' %
                                           (self.inner_text, self.lineEdit.text()))
            else:
                if items_found > 0:
                    return self.parent.status.setText('Такая категория уже есть')
                session.add(Category(name=self.lineEdit.text()))
                session.commit()
                self.parent.status.setText('Категория "%s" была успешно добавлена' % self.lineEdit.text())
            self.parent.fill_categories()


class CategoriesForm(QWidget, CategoriesFormUi):
    def __init__(self, parent):
        super(CategoriesForm, self).__init__()
        self.setupUi(self)

        self.parent = parent
        self.create_btn.clicked.connect(self.add_category)
        self.edit_btn.clicked.connect(self.edit_category)
        self.delete_btn.clicked.connect(self.delete_category)
        self.search_field.textChanged.connect(self.search)
        self.fill_categories()

        self.dialog = None

    def fill_categories(self):
        while self.listWidget.takeItem(0):
            pass
        self.listWidget.addItems([cat.name for cat in self.parent.session.query(Category).all()])

    def search(self, text):
        self.listWidget.clear()
        if text:
            categories = []
            for cat in self.parent.session.query(Category).all():
                if cat.name.lower().startswith(text.lower()):
                    self.listWidget.addItem(cat.name)
        else:
            self.fill_categories()

    def add_category(self):
        self.status.setText('')
        self.dialog = CategoriesDialog(self, 'Добавление категории')
        self.dialog.show()

    def edit_category(self):
        self.status.setText('')
        try:
            self.dialog = CategoriesDialog(self, 'Изменение категории',
                                           self.listWidget.selectedItems()[0].text())
            self.dialog.show()
        except IndexError:
            self.status.setText('Категория должна быть выбрана!')

    def delete_category(self):
        self.status.setText('')
        try:
            name = self.listWidget.selectedItems()[0].text()
            category = self.parent.session.query(Category).filter(Category.name == name).first()
            self.parent.session.delete(category)
            self.parent.session.commit()
            self.fill_categories()
        except IndexError:
            self.status.setText('Категория должна быть выбрана!')


class CategoriesObjForm(QWidget, CategoriesObjFormUi):
    def __init__(self, parent):
        super(CategoriesObjForm, self).__init__()
        self.setupUi(self)

        self.parent = parent
        self.items = []
        for i, category in enumerate(self.parent.session.query(Category).all()):
            self.items.append(category.name)
            self.listWidget.addItem(category.name)
            if category in self.parent.active_object.categories:
                item = self.listWidget.item(i)
                item.setBackground(QColor(0, 255, 0))
        self.chosen = []

        self.lineEdit.textChanged.connect(self.search)
        self.listWidget.itemClicked.connect(self.interact)

    def search(self):
        text = self.lineEdit.text()
        while self.listWidget.takeItem(0):
            pass
        for category in filter(lambda x: x.lower().startswith(text.lower()), self.items):
            self.listWidget.addItem(category)
            if category in self.chosen:
                item = self.listWidget.findItems(category, Qt.MatchFixedString)[0]
                item.setBackground(QColor(0, 255, 0))

    def interact(self, item: QListWidgetItem):
        text = item.text()
        category = self.parent.session.query(Category).filter(Category.name == text).first()
        if text not in self.chosen:
            self.chosen.append(text)
            self.parent.active_object.categories.append(category)
            item.setBackground(QColor(0, 255, 0))
        else:
            self.chosen.pop(self.chosen.index(text))
            self.parent.active_object.categories.pop(
                self.parent.active_object.categories.index(category)
            )
            item = self.listWidget.findItems(text, Qt.MatchFixedString)[0]
            item.setBackground(QColor(255, 255, 255))
        self.parent.session.merge(self.parent.active_object)
        self.parent.session.commit()

    # def mousePressEvent(self, event: QMouseEvent) -> None:
    #     pass
