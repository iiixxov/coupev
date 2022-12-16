from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

from new_order.order_edit_ui import Ui_NewOrder
from new_order.set_size_window import SetSizeDialog
from new_order.grawing import Drawing
import sys


class OrderEditWindow:
    draw = None
    k = 0.15

    sizes = [0, 0, 0, 0, 0, 0, 0]
    divide = [0, 0, 0, 0, 0, 0, 0]
    materials = ['', '', '', '', '', '', '']
    doors_sizes = [0, 0, 0, 0, 0, 0, 0]

    profile = (26, 52, 59, 36)
    uplotnitel = 2
    shlegel = 5
    napravlaushaya = 40
    rigel = 7

    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.NewOrder = QtWidgets.QMainWindow()
        self.connect_to_db()
        self.ui = Ui_NewOrder()
        self.ui.setupUi(self.NewOrder)
        self.add_connect()

    def connect_to_db(self):
        from PyQt5.QtSql import QSqlDatabase
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("contacts.sqlite")
        con.open()

    def get_customers(self):
        self.ui.list_customers.clear()
        text = self.ui.inp_customer.text()
        if text != '':
            query = QSqlQuery(f"SELECT Имя FROM Клиенты WHERE Имя LIKE '{text}%'")
            while query.next():
                self.ui.list_customers.addItem(query.value(0))

    def get_profiles(self):
        self.ui.list_profile.clear()
        text = self.ui.inp_profile.text()
        if text != '':
            query = QSqlQuery(f"SELECT Название FROM Профили WHERE Название LIKE '{text}%'")
            while query.next():
                self.ui.list_profile.addItem(query.value(0))

    def add_connect(self):
        self.ui.size_1.clicked.connect(lambda: self.show_set_size(0))
        self.ui.size_2.clicked.connect(lambda: self.show_set_size(1))
        self.ui.size_3.clicked.connect(lambda: self.show_set_size(2))
        self.ui.size_4.clicked.connect(lambda: self.show_set_size(3))
        self.ui.size5.clicked.connect(lambda: self.show_set_size(4))
        self.ui.size_6.clicked.connect(lambda: self.show_set_size(5))
        self.ui.size_7.clicked.connect(lambda: self.show_set_size(6))

        self.ui.btn_merge.clicked.connect(self.merge)
        self.ui.btn_up_draw.clicked.connect(self.update_drawing)
        self.ui.custom_mat.clicked.connect(self.custom_material)

        self.ui.btn_plus.clicked.connect(lambda: self.scale(0))
        self.ui.btn_nimus.clicked.connect(lambda: self.scale(1))
        self.ui.btn_grass.clicked.connect(lambda: self.draw_material('Стекло'))
        self.ui.btn_mirror.clicked.connect(lambda: self.draw_material('Зеркало'))
        self.ui.btn_LDSP.clicked.connect(lambda: self.draw_material('ЛДСП'))
        self.ui.btn_unmerge.clicked.connect(self.unmerge)

        self.ui.inp_customer.textChanged.connect(self.get_customers)
        self.ui.list_customers.itemDoubleClicked.connect(lambda item: self.ui.inp_customer.setText(item.text()))

        self.ui.inp_profile.textChanged.connect(self.get_profiles)
        self.ui.list_profile.itemDoubleClicked.connect(lambda item: self.ui.inp_profile.setText(item.text()))

    @staticmethod
    def norm_value(value, default=1):
        if value == '' or not value.isdigit():
            return default
        else:
            return int(value)

    def custom_material(self):
        if self.draw is not None:
            material = self.ui.inp_mat.text()
            self.draw.custom_mat(material)

    def merge(self):
        if self.draw is not None:
            self.draw.merge()

    def unmerge(self):
        if self.draw is not None:
            self.draw.unmerge()

    def scale(self, action):
        if self.draw is not None:
            if action == 0:
                self.k += 0.05
            else:
                self.k -= 0.05
            self.draw.update_scale(self.k)

    def draw_material(self, material):
        if self.draw is not None:
            self.draw.change_materials(material)

    def normalize_all_value(self):
        self.doors = self.norm_value(self.ui.inp_door.text())
        self.height = self.norm_value(self.ui.inp_height.text()) - self.napravlaushaya
        self.long = self.norm_value(self.ui.inp_long.text())

        for i, size in enumerate(self.ui.int_door_w.text().split()):
            self.doors_sizes[i] = self.norm_value(size, default=0)
        for i in range(len(self.ui.int_door_w.text().split()), 7):
            self.doors_sizes[i] = 0

        for i in range(self.doors):
            l, h = self.norm_value(eval(f"self.ui.l{i + 1}.text()")), self.norm_value(eval(f"self.ui.h{i + 1}.text()"))
            if l == 0 or h == 0:
                return 1

            if self.divide[i] != (h, l):
                self.divide[i] = (h, l)
                self.sizes[i] = [[0 for _ in range(h)], [0 for _ in range(l)]]
            self.materials[i] = eval(f"self.ui.mat{i + 1}.currentText()")

    def show_set_size(self, n):
        if self.normalize_all_value() == 1:
            QMessageBox.warning(self.NewOrder, "Ошибка", "Деление на 0.")
            return
        if n >= self.doors:
            QMessageBox.warning(self.NewOrder, "Ошибка", "Двери не существует.")
            return
        h, l = self.divide[n]

        if h > 15 or l > 15:
            QMessageBox.warning(self.NewOrder, "Ошибка", "Слишком большое значение.")
            return
        set_size_dialog = SetSizeDialog(self.sizes[n], h, l)
        size = set_size_dialog.size
        if type(size) == list:
            if 0 not in size[0] or 0 not in size[1] or sum(size[0]) >= self.long or sum(
                    size[1]) >= self.height // self.doors:
                QMessageBox.warning(self.NewOrder, "Ошибка", "Недопустимые значения.")
            else:
                self.sizes[n] = size

    def update_drawing(self):
        if self.normalize_all_value() == 1:
            QMessageBox.warning(self.NewOrder, "Ошибка", "Деление на 0.")
            return
        profile_name = self.ui.inp_profile.text()

        query = QSqlQuery(f"SELECT Название FROM Профили WHERE Название='{profile_name}'")
        query.next()
        if query.value(0) is None:
            QMessageBox.warning(self.NewOrder, "Ошибка", "Профиль не найден")
            return

        query = QSqlQuery(f"SELECT * FROM Профили WHERE Название='{profile_name}'")
        query.next()
        profile = (query.value(0), query.value(1), query.value(2), query.value(3))

        query = QSqlQuery(f"SELECT * FROM Константы;")
        query.next()
        napravlaushaya = query.value(0)
        uplotnitel = query.value(1)
        rigel = query.value(2)

        if self.ui.r_have_schlegel.isChecked():
            shlegel = query.value(3)
        else:
            shlegel = 0

        if self.ui.r_standart_overlap.isChecked():
            n_perehlest = self.doors - 1
        elif self.ui.r_nostandart_overlap.isChecked():
            n_perehlest = int(self.ui.inp_overlap_count.text())
        else:
            n_perehlest = 0

        if self.draw is not None:
            self.ui.verticalGroupBox.layout().removeWidget(self.draw)
        self.draw = Drawing(self.ui.centralwidget, self.height, self.long, self.doors, self.divide, self.sizes, self.k,
                            self.materials, self.doors_sizes, profile, uplotnitel, shlegel, rigel, n_perehlest)
        self.ui.verticalGroupBox.layout().addWidget(self.draw)

    def exec(self):
        self.NewOrder.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    OrderEditWindow().exec()
