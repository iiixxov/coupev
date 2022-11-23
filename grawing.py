from PyQt5 import QtCore, QtWidgets
from ceil import Ceil


class UI_Ceil(QtWidgets.QCheckBox):
    def __init__(self, form, geometry, k, material, door_n):
        super(UI_Ceil, self).__init__(form)
        self.geometry_ = geometry
        self.merged = list()
        self.door_n = door_n
        self.material = material
        self.k = k
        self.update_text()
        self.update_geometry()
        self.setStyleSheet(
            "border: 1px solid black;\n"
            "border-color: rgb(0, 0, 0);"
        )
        self.update_color()

    def update_text(self):
        h, l = round(self.geometry_[3]), round(self.geometry_[2])
        self.setText(f'{self.material}\n{h}x{l}')

    def update_geometry(self):
        self.setGeometry(QtCore.QRect(*map(lambda a: round(a * self.k), self.geometry_)))

    def update_color(self):
        style = self.styleSheet()
        if self.material == 'Стекло':
            self.setStyleSheet(f"{style}\nbackground-color: rgb(232, 232, 232);")
        elif self.material == 'Зеркало':
            self.setStyleSheet(f"{style}\nbackground-color: rgb(102, 205, 170);")
        else:
            self.setStyleSheet(f"{style}\nbackground-color: rgb(255, 127,  80);")


class Drawing(QtWidgets.QWidget):
    def update_scale(self, k):
        for ceil in self.ceils:
            ceil.k = k
            ceil.update_geometry()

    def __init__(self, form, height, long, doors, divide, sizes, k, materials):
        super(Drawing, self).__init__()
        """height = 2500
        long = 3000
        doors = 2
        divide = (
            (3, 2),
            (3, 2)
        )
        sizes = (
            ((0, 300, 0), (0, 0)),
            ((300, 0, 0), (0, 0))
        )
        k = 0.15"""
        doors_sizes = Ceil.get_sizes(height, long, doors, divide)
        for i in range(doors):
            doors_sizes[i] = Ceil.change_sizes(doors_sizes[i], divide[i], sizes[i], height, long / doors)

        self.ceils = []
        for i_door, door in enumerate(doors_sizes):
            for col in door:
                for size in col:
                    x, y, x1, y1 = size
                    x1, y1, = x1 - x, y1 - y
                    self.ceils.append(UI_Ceil(self, (x, y, x1, y1), k, materials[i_door], i_door))
        QtCore.QMetaObject.connectSlotsByName(self)

    def merge(self):
        clicked = list(ceil for ceil in self.ceils if ceil.isChecked())
        if not any(ceil.door_n != clicked[0].door_n for ceil in clicked):
            up_left = min(clicked, key=lambda a: a.geometry().x() + a.geometry().y())
            down_right = max(clicked, key=lambda a: a.geometry().x() + a.geometry().y())
            clicked.remove(up_left)
            up_left.setChecked(False)
            for ceil in clicked:
                up_left.merged.append(ceil)
                ceil.setChecked(False)
                ceil.setEnabled(False)
                ceil.setVisible(False)
            x, y = up_left.geometry_[0], up_left.geometry_[1]
            ceil_l = down_right.geometry_[0] + down_right.geometry_[2] - x
            ceil_h = down_right.geometry_[1] + down_right.geometry_[3] - y
            up_left.geometry_ = (x, y, ceil_l, ceil_h)
            up_left.update_text()
            up_left.update_geometry()

    def change_materials(self, material):
        for ceil in self.ceils:
            if ceil.isChecked():
                ceil.setChecked(False)
                ceil.material = material
                ceil.update_text()
                ceil.update_color()
