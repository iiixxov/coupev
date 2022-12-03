from PyQt5 import QtCore, QtGui, QtWidgets


class CeilFrame(QtWidgets.QFrame):
    def __init__(self, form):
        super(CeilFrame, self).__init__(form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("background-color:rgb(170, 170, 170);")


class InputSize(QtWidgets.QLineEdit):
    def __init__(self, form):
        super().__init__(form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)


class SetSizeDialog(QtWidgets.QDialog):
    def __init__(self, sizes, height_div, long_div):
        super(SetSizeDialog, self).__init__()
        self.setModal(True)
        self.setWindowTitle("Установить размеры")
        self.resize(538, 455)

        #self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.gridLayout = QtWidgets.QGridLayout(self)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)

        self.ceils = []
        for i in range(height_div):
            for j in range(long_div):
                ceil = CeilFrame(self)
                self.gridLayout.addWidget(ceil, i + 1, j + 1, 1, 1)
                self.ceils.append(ceil)

        self.inputs = [[], []]
        for i in range(height_div):
            input_edit = InputSize(self)
            if sizes[0][i] != 0:
                input_edit.setText(str(sizes[0][i]))
            self.gridLayout.addWidget(input_edit, i + 1, 0, 1, 1)
            self.inputs[0].append(input_edit)
        for i in range(long_div):
            input_edit = InputSize(self)
            if sizes[1][i] != 0:
                input_edit.setText(str(sizes[0][i]))
            self.gridLayout.addWidget(input_edit, 0, i + 1, 1, 1)
            self.inputs[1].append(input_edit)

        #self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 0, 1, 1)

        #self.verticalLayout.addWidget(self.buttonBox)

        def reject():
            self.size = None
            self.close()

        def accept():
            self.size = [[], []]
            for i, inputs in enumerate(self.inputs):
                for input_edit in inputs:
                    size = input_edit.text()
                    if not size.isdigit():
                        size = 0
                    else:
                        size = input_edit.text()
                    self.size[i].append(int(size))
            print(self.size)
            self.close()

        self.buttonBox.accepted.connect(accept)
        self.buttonBox.rejected.connect(reject)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()
        self.exec_()

