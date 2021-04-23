# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'customTabsDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_customTabsDialog(object):
    def setupUi(self, customTabsDialog):
        customTabsDialog.setObjectName("customTabsDialog")
        customTabsDialog.resize(250, 280)
        self.gridLayout = QtWidgets.QGridLayout(customTabsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidgetTabs = QtWidgets.QListWidget(customTabsDialog)
        self.listWidgetTabs.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidgetTabs.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetTabs.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidgetTabs.setObjectName("listWidgetTabs")
        self.gridLayout.addWidget(self.listWidgetTabs, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(customTabsDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(customTabsDialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(customTabsDialog)
        self.pushButtonAccept.clicked.connect(customTabsDialog.accept)
        self.pushButtonCancel.clicked.connect(customTabsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(customTabsDialog)
        customTabsDialog.setTabOrder(self.listWidgetTabs, self.pushButtonCancel)
        customTabsDialog.setTabOrder(self.pushButtonCancel, self.pushButtonAccept)

    def retranslateUi(self, customTabsDialog):
        _translate = QtCore.QCoreApplication.translate
        customTabsDialog.setWindowTitle(_translate("customTabsDialog", "Meggie - Custom tabs"))
        self.pushButtonCancel.setText(_translate("customTabsDialog", "Cancel"))
        self.pushButtonAccept.setText(_translate("customTabsDialog", "Accept"))

