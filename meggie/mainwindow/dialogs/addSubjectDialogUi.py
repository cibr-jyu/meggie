# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addSubjectDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddSubject(object):
    def setupUi(self, AddSubject):
        AddSubject.setObjectName("AddSubject")
        AddSubject.resize(519, 312)
        self.gridLayout = QtWidgets.QGridLayout(AddSubject)
        self.gridLayout.setObjectName("gridLayout")
        self.labelAddSubjects = QtWidgets.QLabel(AddSubject)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelAddSubjects.setFont(font)
        self.labelAddSubjects.setObjectName("labelAddSubjects")
        self.gridLayout.addWidget(self.labelAddSubjects, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(AddSubject)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        self.pushButtonOk = QtWidgets.QPushButton(AddSubject)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout_2.addWidget(self.pushButtonOk)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 3)
        self.scrollArea = QtWidgets.QScrollArea(AddSubject)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 499, 240))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButtonRemove = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonRemove.setEnabled(False)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.gridLayout_2.addWidget(self.pushButtonRemove, 2, 0, 1, 1)
        self.listWidgetFileNames = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidgetFileNames.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidgetFileNames.setObjectName("listWidgetFileNames")
        self.gridLayout_2.addWidget(self.listWidgetFileNames, 0, 0, 1, 1)
        self.pushButtonBrowse = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonBrowse.setSizePolicy(sizePolicy)
        self.pushButtonBrowse.setObjectName("pushButtonBrowse")
        self.gridLayout_2.addWidget(self.pushButtonBrowse, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)

        self.retranslateUi(AddSubject)
        self.pushButtonCancel.clicked.connect(AddSubject.reject)
        self.pushButtonOk.clicked.connect(AddSubject.accept)
        QtCore.QMetaObject.connectSlotsByName(AddSubject)

    def retranslateUi(self, AddSubject):
        _translate = QtCore.QCoreApplication.translate
        AddSubject.setWindowTitle(_translate("AddSubject", "Meggie - Add subjects"))
        self.labelAddSubjects.setText(_translate("AddSubject", "Add subjects (raw files) to the experiment:"))
        self.pushButtonCancel.setText(_translate("AddSubject", "Cancel"))
        self.pushButtonOk.setText(_translate("AddSubject", "Ok"))
        self.pushButtonRemove.setText(_translate("AddSubject", "Remove"))
        self.pushButtonBrowse.setText(_translate("AddSubject", "Browse..."))

