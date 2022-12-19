import datetime

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

from new_order.order_edit_ui import Ui_edit_order
from new_order.set_size_window import SetSizeDialog
from new_order.grawing import Drawing
from new_order.show_profiles import ShowPrifileUi


class OrderEditWindow:
    def __init__(self, order_id):
        self.draw = None
        self.k = 0.15
        self.sizes = [None, None, None, None, None, None, None]
        self.divide = [None, None, None, None, None, None, None]
        self.materials = [None, None, None, None, None, None, None]
        self.doors_sizes = [None, None, None, None, None, None, None]

        self.order_id = order_id

        self.edit_order = QtWidgets.QWidget()
        self.ui = Ui_edit_order()
        self.ui.setupUi(self.edit_order)

        self.add_connect()
        self.set_date()

        self.ui.splitter.setStretchFactor(1, 5)
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.inp_profile.setText("Открытый")

    def set_date(self):
        now = datetime.datetime.now()
        year, month, day = now.year, now.month, now.day
        self.ui.inp_date.setDate(QtCore.QDate(QtCore.QDate(year, month, day)))
        self.ui.inp_date_uot.setDate(QtCore.QDate(QtCore.QDate(year, month, day)))

    def zero(self):
        self.draw = None
        self.k = 0.15
        self.sizes = [None, None, None, None, None, None, None]
        self.divide = [None, None, None, None, None, None, None]
        self.materials = [None, None, None, None, None, None, None]
        self.doors_sizes = [None, None, None, None, None, None, None]

        self.ui.inp_door.setValue(1)
        self.ui.inp_long.setText('')
        self.ui.inp_height.setText('')
        self.ui.inp_longL2.setText('')
        self.ui.int_door_w.setText('')

        self.ui.l1.setText('')
        self.ui.h1.setText('')
        self.ui.l2.setText('')
        self.ui.h2.setText('')
        self.ui.l3.setText('')
        self.ui.h3.setText('')
        self.ui.l4.setText('')
        self.ui.h4.setText('')
        self.ui.l5.setText('')
        self.ui.h5.setText('')
        self.ui.l6.setText('')
        self.ui.h6.setText('')
        self.ui.l7.setText('')
        self.ui.h7.setText('')

        self.set_date()
        self.ui.int_norder.setValue(0)
        self.ui.inp_discription.setText('')
        self.ui.inp_color.setText('')
        self.ui.inp_customer.setText('')
        self.ui.inp_profile.setText('')

        self.ui.r_have_schlegel.setChecked(True)
        self.ui.r_2_guide.setChecked(True)
        self.ui.r_no_fraction.setChecked(True)
        self.ui.r_mechanismR.setChecked(True)
        self.ui.r_no_pack.setChecked(True)
        self.ui.r_no_dilivery.setChecked(True)
        self.ui.r_build.setChecked(True)
        self.ui.r_have_overlay.setChecked(True)
        self.ui.inp_overlay_long.setText('')
        self.ui.inp_overlay_count.setText('')
        self.ui.r_standart_overlap.setChecked(True)
        self.ui.inp_overlap_count.setValue(0)
        self.ui.inp_dop_mat.setText('')

    def add_customer_to_db(self):
        name = self.ui.inp_customer.text()
        QSqlQuery().exec(f"INSERT INTO Клиенты (Имя) VALUES ('{name}');")
        self.get_customers()

    def save(self):
        if self.draw is None and not self.update_drawing():
            return

        ceils = []
        for ceil in self.draw.ceils:
            ceils.append((ceil.geometry_, ceil.material, ceil.pos, ceil.have_uplotnitel))

        if self.ui.r_no_pack.isChecked():
            pack = 0
        elif self.ui.r_packin_tape.isChecked():
            pack = 1
        elif self.ui.r_packin_corrugation.isChecked():
            pack = 3
        else:
            pack = 4

        if self.ui.r_standart_overlap.isChecked():
            overlap = -1
        else:
            overlap = self.ui.inp_overlap_count.text()

        query = QSqlQuery(f"SELECT id FROM Профили WHERE Название='{self.ui.inp_profile.text()}'")
        query.next()
        profile_id = query.value(0)

        query = QSqlQuery(f"SELECT id FROM Клиенты WHERE Имя LIKE '{self.ui.inp_customer.text()}%'")
        query.next()
        customer_id = query.value(0)

        longL2 = self.norm_value(self.ui.inp_longL2.text())

        print(QSqlQuery().exec(
            f""" UPDATE Заказы SET
            "Двери" = {self.doors}, 
            "Высота" = {self.height}, 
            "Ширина" = {self.long}, 
            "Ширина Л" = {longL2}, 
            "Ширина Д" = "{self.doors_sizes}", 
            "Разделители" = "{self.divide}", 
            "Материалы" = "{self.materials}", 
            "Дата" = "{self.ui.inp_date.text()}", 
            "Номер" = {self.ui.int_norder.text()}, 
            "Дата В" = "{self.ui.inp_date_uot.text()}", 
            "Описание" = "{self.ui.inp_discription.toPlainText()}", 
            "Цвет" = "{self.ui.color.text()}", 
            "Шлегель Р" = {int(self.ui.r_have_schlegel.isChecked())}, 
            "Направляющая Р" = {int(self.ui.r_2_guide.isChecked())}, 
            "Упаковка Р" = {pack}, 
            "Механизм Р" = {int(self.ui.r_mechanismR.isChecked())}, 
            "Доставка Р" = {int(self.ui.r_no_dilivery.isChecked())}, 
            "Накладка" = null, 
            "Перехлест" = {overlap}, 
            "Дополнительно" = "{self.ui.inp_dop_mat.toPlainText()}", 
            "Клиент_id" = {customer_id},
            "Профиль_id" = {profile_id},
            "Размеры" = "{ceils}"
            WHERE id={self.order_id}; """
        ))

    @staticmethod
    def show_profile():
        profiles = []

        query = QSqlQuery(f"SELECT * FROM Профили;")
        while query.next():
            profiles.append((query.value(2), query.value(1), query.value(3), query.value(4), query.value(5)))

        query = QSqlQuery(f"SELECT * FROM Константы;")
        query.next()
        const = (query.value(0), query.value(1), query.value(2), query.value(3))

        Dialog = QtWidgets.QDialog()
        ui = ShowPrifileUi()
        ui.setupUi(Dialog, profiles, const)
        Dialog.show()
        Dialog.exec()

    @staticmethod
    def connect_to_db():
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

        self.ui.btn_zero.clicked.connect(self.zero)
        self.ui.btn_up_draw.clicked.connect(self.update_drawing)
        self.ui.btn_frofiles.clicked.connect(self.show_profile)
        self.ui.btn_save.clicked.connect(self.save)

        self.ui.btn_merge.clicked.connect(self.merge)
        self.ui.custom_mat.clicked.connect(self.custom_material)
        self.ui.btn_plus.clicked.connect(lambda: self.scale(0))
        self.ui.btn_nimus.clicked.connect(lambda: self.scale(1))
        self.ui.btn_grass.clicked.connect(lambda: self.draw_material('Стекло'))
        self.ui.btn_mirror.clicked.connect(lambda: self.draw_material('Зеркало'))
        self.ui.btn_LDSP.clicked.connect(lambda: self.draw_material('ЛДСП'))
        self.ui.btn_unmerge.clicked.connect(self.unmerge)

        self.ui.btn_add_to_db.clicked.connect(self.add_customer_to_db)
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
        self.height = self.norm_value(self.ui.inp_height.text())
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
            QMessageBox.warning(self.edit_order, "Ошибка", "Деление на 0.")
            return
        if n >= self.doors:
            QMessageBox.warning(self.edit_order, "Ошибка", "Двери не существует.")
            return
        h, l = self.divide[n]

        if h > 15 or l > 15:
            QMessageBox.warning(self.edit_order, "Ошибка", "Слишком большое значение.")
            return
        set_size_dialog = SetSizeDialog(self.sizes[n], h, l)
        size = set_size_dialog.size
        if type(size) == list:
            if 0 not in size[0] or 0 not in size[1] or sum(size[0]) >= self.long or sum(
                    size[1]) >= self.height // self.doors:
                QMessageBox.warning(self.edit_order, "Ошибка", "Недопустимые значения.")
            else:
                self.sizes[n] = size

    def update_drawing(self):
        if self.normalize_all_value() == 1:
            QMessageBox.warning(self.edit_order, "Ошибка", "Деление на 0.")
            return False
        profile_name = self.ui.inp_profile.text()
        customer_name = self.ui.inp_customer.text()

        query = QSqlQuery(f"SELECT Название FROM Профили WHERE Название='{profile_name}'")
        query.next()
        if query.value(0) is None:
            QMessageBox.warning(self.edit_order, "Ошибка", "Профиль не найден")
            return False

        query = QSqlQuery(f"SELECT Имя FROM Клиенты WHERE Имя='{customer_name}'")
        query.next()
        if query.value(0) is None:
            QMessageBox.warning(self.edit_order, "Ошибка", "Клиент не найден")
            return False

        query = QSqlQuery(f"SELECT * FROM Профили WHERE Название='{profile_name}'")
        query.next()
        profile = (query.value(0), query.value(2), query.value(3), query.value(4))
        print(profile)

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
        self.draw = Drawing(self.height - napravlaushaya, self.long, self.doors, self.divide,
                            self.sizes, self.k,
                            self.materials, self.doors_sizes, profile, uplotnitel, shlegel, rigel, n_perehlest)
        self.ui.verticalGroupBox.layout().addWidget(self.draw)
        return True
