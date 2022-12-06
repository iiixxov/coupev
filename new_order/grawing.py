from PyQt5 import QtCore, QtWidgets
from new_order.ceil import Ceil


class UI_Ceil(QtWidgets.QCheckBox):
    def __init__(self, form, geometry, k, material, door_n, pos):
        super(UI_Ceil, self).__init__(form)
        self.geometry_ = geometry
        self.merged = list()
        self.door_n = door_n
        self.material = material
        self.k = k
        self.pos = pos
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
        self.setToolTip(f'{self.material}\n{h}x{l}\npos={self.pos}')

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
    def custom_mat(self, material):
        for ceil in self.ceils:
            if ceil.isChecked():
                ceil.setChecked(False)
                ceil.material = material
                ceil.update_text()

    def update_scale(self, k):
        for ceil in self.ceils:
            ceil.k = k
            ceil.update_geometry()

    def __init__(self, form, height, long, doors, divide, sizes, k, materials, d_sizes, pofile: tuple, uplotnitel, shlegel):
        """
        :param pofile: (перехлест, горизонт, Н ЛДСП, L ЛДСП)
        """
        super(Drawing, self).__init__()
        d_sizes = Ceil.get_doors_sizes(long, doors, d_sizes)
        doors_sizes = Ceil.get_sizes(height, long, doors, divide, d_sizes)
        for i in range(doors):
            doors_sizes[i] = Ceil.change_sizes(doors_sizes[i], divide[i], sizes[i], height, d_sizes[i])

        self.ceils = []
        for i_door, door in enumerate(doors_sizes):
            for i, col in enumerate(door):
                for j, size in enumerate(col):
                    x, y, x1, y1 = size
                    x1, y1, = x1 - x, y1 - y
                    self.ceils.append(UI_Ceil(self, (x, y, x1, y1), k, materials[i_door], i_door, (i, j)))
        QtCore.QMetaObject.connectSlotsByName(self)

    def merge(self):
        clicked = list(ceil for ceil in self.ceils if ceil.isChecked())
        if clicked and not any(ceil.door_n != clicked[0].door_n for ceil in clicked):
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
            up_left.first_geometry_ = up_left.geometry_
            up_left.geometry_ = (x, y, ceil_l, ceil_h)
            up_left.update_text()
            up_left.update_geometry()

    def unmerge(self):
        for ceil in self.ceils:
            ceil.setChecked(False)
            if ceil.isChecked() and len(ceil.merged) != 0:
                ceil.geometry_ = ceil.first_geometry_
                ceil.update_text()
                ceil.update_geometry()
                for merged_ceil in ceil.merged:
                    merged_ceil.setEnabled(True)
                    merged_ceil.setVisible(True)

    def change_materials(self, material):
        for ceil in self.ceils:
            if ceil.isChecked():
                ceil.setChecked(False)
                ceil.material = material
                ceil.update_text()
                ceil.update_color()
