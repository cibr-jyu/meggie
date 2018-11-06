# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../epochWidgetUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(402, 281)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout()
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.groupBoxEpochs = QtWidgets.QGroupBox(Form)
        self.groupBoxEpochs.setObjectName("groupBoxEpochs")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxEpochs)
        self.gridLayout.setObjectName("gridLayout")
        self.listWidgetEpochs = QtWidgets.QListWidget(self.groupBoxEpochs)
        self.listWidgetEpochs.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.listWidgetEpochs.setObjectName("listWidgetEpochs")
        self.gridLayout.addWidget(self.listWidgetEpochs, 0, 0, 1, 1)
        self.listWidgetEvents = QtWidgets.QListWidget(self.groupBoxEpochs)
        self.listWidgetEvents.setEnabled(True)
        self.listWidgetEvents.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidgetEvents.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.listWidgetEvents.setObjectName("listWidgetEvents")
        self.gridLayout.addWidget(self.listWidgetEvents, 2, 0, 1, 1)
        self.labelInfo = QtWidgets.QLabel(self.groupBoxEpochs)
        self.labelInfo.setObjectName("labelInfo")
        self.gridLayout.addWidget(self.labelInfo, 1, 0, 1, 1)
        self.verticalLayout_14.addWidget(self.groupBoxEpochs)
        self.gridLayout_2.addLayout(self.verticalLayout_14, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBoxEpochs.setTitle(_translate("Form", "Epoch collections:"))
        self.labelInfo.setText(_translate("Form", "Info:"))

