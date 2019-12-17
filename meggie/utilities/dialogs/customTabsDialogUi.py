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
        customTabsDialog.resize(188, 280)
        self.gridLayout = QtWidgets.QGridLayout(customTabsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(customTabsDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.listWidgetTabs = QtWidgets.QListWidget(customTabsDialog)
        self.listWidgetTabs.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidgetTabs.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetTabs.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidgetTabs.setObjectName("listWidgetTabs")
        self.gridLayout.addWidget(self.listWidgetTabs, 0, 0, 1, 1)

        self.retranslateUi(customTabsDialog)
        self.buttonBox.accepted.connect(customTabsDialog.accept)
        self.buttonBox.rejected.connect(customTabsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(customTabsDialog)

    def retranslateUi(self, customTabsDialog):
        _translate = QtCore.QCoreApplication.translate
        customTabsDialog.setWindowTitle(_translate("customTabsDialog", "Meggie - Custom tabs"))

