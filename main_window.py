import sys
import datetime

from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlQuery

from login.login_ui import Ui_login
from orders_table.order_table_ui import Ui_MainWindow
from order_edit_window import OrderEditWindow


class MainWindow:
    def __init__(self):
        self.widgets = []

        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)

        self.add_connect()
        self.connect_to_db()

    def update_table(self):
        self.ui.listWidget.clear()

        query = QSqlQuery(f"SELECT id, Дата, Клиент_id, Описание, Номер, Профиль_id FROM Заказы ORDER BY id DESC LIMIT 100;")
        while query.next():
            id = query.value(0)
            date = query.value(1)

            customer_query = QSqlQuery(f"SELECT Имя FROM Клиенты WHERE id={query.value(2)}")
            customer_query.next()
            customer_id = customer_query.value(0)

            description = query.value(3)
            doc = query.value(4)

            profile_query = QSqlQuery(f"SELECT Название FROM Профили WHERE id={query.value(5)}")
            profile_query.next()
            profile_id = profile_query.value(0)

            item = QtWidgets.QListWidgetItem(f"{date} {customer_id} ({description}) {doc} {profile_id}")
            item.id = id
            self.ui.listWidget.addItem(item)

    @staticmethod
    def connect_to_db():
        from PyQt5.QtSql import QSqlDatabase
        con = QSqlDatabase.addDatabase("QSQLITE")
        con.setDatabaseName("contacts.sqlite")
        con.open()

    def add_connect(self):
        self.ui.btn_update.clicked.connect(self.update_table)
        self.ui.btn_form.clicked.connect(self.open_form)
        self.ui.btn_create.clicked.connect(self.create)

    def create(self):
        now = datetime.datetime.now()
        date = '.'.join(str(e) for e in (now.day, now.month, now.year))
        QSqlQuery().exec(
            f"""INSERT INTO Заказы ("Дата", "Дата В", "Описание") VALUES ('{date}', '{date}', 'Новый заказ');"""
        )
        self.update_table()

    def exec(self):
        def check_login():
            name = ui_login.comboBox.currentText()
            password = ui_login.lineEdit.text()

            query = QSqlQuery(f"SELECT Пароль FROM Пользователи WHERE Имя='{name}';")
            query.next()
            if password == query.value(0):
                self.is_logining = True
                login.close()
            else:
                ui_login.label_3.setText("Неверный пароль")

        login = QtWidgets.QDialog()
        ui_login = Ui_login()
        ui_login.setupUi(login)
        login.setModal(True)

        self.is_logining = False
        ui_login.pushButton.clicked.connect(check_login)

        login.show()
        login.exec()

        if self.is_logining:
            self.main_window.showMaximized()
        else:
            sys.exit()

        sys.exit(self.app.exec_())

    def open_form(self):
        item = self.ui.listWidget.selectedItems()
        if not item:
            return
        order_edit = OrderEditWindow(item[0].id).edit_order
        self.ui.tabWidget.addTab(order_edit, "Форм")
        self.ui.tabWidget.setCurrentIndex(1)


if __name__ == "__main__":
    MainWindow().exec()
