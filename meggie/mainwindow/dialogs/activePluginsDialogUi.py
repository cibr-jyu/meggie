# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'activePluginsDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_activePluginsDialog(object):
    def setupUi(self, activePluginsDialog):
        activePluginsDialog.setObjectName("activePluginsDialog")
        activePluginsDialog.resize(414, 176)
        self.gridLayout = QtWidgets.QGridLayout(activePluginsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidgetPlugins = QtWidgets.QListWidget(activePluginsDialog)
        self.listWidgetPlugins.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listWidgetPlugins.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetPlugins.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidgetPlugins.setObjectName("listWidgetPlugins")
        self.gridLayout.addWidget(self.listWidgetPlugins, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(activePluginsDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(activePluginsDialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(activePluginsDialog)
        self.pushButtonAccept.clicked.connect(activePluginsDialog.accept)
        self.pushButtonCancel.clicked.connect(activePluginsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(activePluginsDialog)
        activePluginsDialog.setTabOrder(self.listWidgetPlugins, self.pushButtonCancel)
        activePluginsDialog.setTabOrder(self.pushButtonCancel, self.pushButtonAccept)

    def retranslateUi(self, activePluginsDialog):
        _translate = QtCore.QCoreApplication.translate
        activePluginsDialog.setWindowTitle(_translate("activePluginsDialog", "Meggie - Active plugins"))
        self.pushButtonCancel.setText(_translate("activePluginsDialog", "Cancel"))
        self.pushButtonAccept.setText(_translate("activePluginsDialog", "Accept"))
