# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../badChannelsDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(368, 706)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidgetBads = QtWidgets.QListWidget(Dialog)
        self.listWidgetBads.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidgetBads.setObjectName("listWidgetBads")
        self.gridLayout.addWidget(self.listWidgetBads, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonReject = QtWidgets.QPushButton(Dialog)
        self.pushButtonReject.setObjectName("pushButtonReject")
        self.horizontalLayout.addWidget(self.pushButtonReject)
        self.pushButtonAccept = QtWidgets.QPushButton(Dialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButtonSelectAll = QtWidgets.QPushButton(Dialog)
        self.pushButtonSelectAll.setObjectName("pushButtonSelectAll")
        self.horizontalLayout_2.addWidget(self.pushButtonSelectAll)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonPlot = QtWidgets.QPushButton(Dialog)
        self.pushButtonPlot.setObjectName("pushButtonPlot")
        self.horizontalLayout_2.addWidget(self.pushButtonPlot)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.pushButtonReject.clicked.connect(Dialog.reject)
        self.pushButtonAccept.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Customize channels"))
        self.pushButtonReject.setText(_translate("Dialog", "Cancel"))
        self.pushButtonAccept.setText(_translate("Dialog", "Ok"))
        self.pushButtonSelectAll.setText(_translate("Dialog", "Select all"))
        self.pushButtonPlot.setText(_translate("Dialog", "Select from plot..."))

