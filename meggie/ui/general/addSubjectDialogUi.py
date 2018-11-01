# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../addSubjectDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddSubject(object):
    def setupUi(self, AddSubject):
        AddSubject.setObjectName("AddSubject")
        AddSubject.resize(640, 305)
        self.gridLayout = QtWidgets.QGridLayout(AddSubject)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(AddSubject)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listWidgetFileNames = QtWidgets.QListWidget(AddSubject)
        self.listWidgetFileNames.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidgetFileNames.setObjectName("listWidgetFileNames")
        self.horizontalLayout.addWidget(self.listWidgetFileNames)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButtonBrowse = QtWidgets.QPushButton(AddSubject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonBrowse.setSizePolicy(sizePolicy)
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.verticalLayout.addWidget(self.pushButtonBrowse)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 3)
        self.pushButtonShowFileInfo = QtWidgets.QPushButton(AddSubject)
        self.pushButtonShowFileInfo.setObjectName("pushButtonShowFileInfo")
        self.gridLayout.addWidget(self.pushButtonShowFileInfo, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(AddSubject)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)
        self.pushButtonRemove = QtWidgets.QPushButton(AddSubject)
        self.pushButtonRemove.setEnabled(False)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.gridLayout.addWidget(self.pushButtonRemove, 2, 1, 1, 1)

        self.retranslateUi(AddSubject)
        self.buttonBox.accepted.connect(AddSubject.accept)
        self.buttonBox.rejected.connect(AddSubject.reject)
        QtCore.QMetaObject.connectSlotsByName(AddSubject)

    def retranslateUi(self, AddSubject):
        _translate = QtCore.QCoreApplication.translate
        AddSubject.setWindowTitle(_translate("AddSubject", "Meggie - Add subject"))
        self.label.setText(_translate("AddSubject", "Add subject file to the experiment:"))
        self.pushButtonBrowse.setText(_translate("AddSubject", "Browse..."))
        self.pushButtonShowFileInfo.setText(_translate("AddSubject", "Show file info"))
        self.pushButtonRemove.setText(_translate("AddSubject", "Remove"))

