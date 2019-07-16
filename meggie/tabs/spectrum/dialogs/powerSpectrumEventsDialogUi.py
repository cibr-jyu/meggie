# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../powerSpectrumEventsDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Advanced(object):
    def setupUi(self, Advanced):
        Advanced.setObjectName("Advanced")
        Advanced.resize(395, 166)
        self.gridLayout_2 = QtWidgets.QGridLayout(Advanced)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditStart = QtWidgets.QLineEdit(Advanced)
        self.lineEditStart.setObjectName("lineEditStart")
        self.gridLayout.addWidget(self.lineEditStart, 1, 1, 1, 1)
        self.lineEditEnd = QtWidgets.QLineEdit(Advanced)
        self.lineEditEnd.setObjectName("lineEditEnd")
        self.gridLayout.addWidget(self.lineEditEnd, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Advanced)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.comboBoxAvgGroup = QtWidgets.QComboBox(Advanced)
        self.comboBoxAvgGroup.setObjectName("comboBoxAvgGroup")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.gridLayout.addWidget(self.comboBoxAvgGroup, 0, 1, 1, 1)
        self.labelGroup = QtWidgets.QLabel(Advanced)
        self.labelGroup.setObjectName("labelGroup")
        self.gridLayout.addWidget(self.labelGroup, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(Advanced)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.pushButtonMaskStart = QtWidgets.QPushButton(Advanced)
        self.pushButtonMaskStart.setObjectName("pushButtonMaskStart")
        self.gridLayout.addWidget(self.pushButtonMaskStart, 1, 2, 1, 1)
        self.pushButtonMaskEnd = QtWidgets.QPushButton(Advanced)
        self.pushButtonMaskEnd.setObjectName("pushButtonMaskEnd")
        self.gridLayout.addWidget(self.pushButtonMaskEnd, 2, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(Advanced)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(Advanced)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Advanced)
        self.pushButtonCancel.clicked.connect(Advanced.reject)
        self.pushButtonAccept.clicked.connect(Advanced.accept)
        QtCore.QMetaObject.connectSlotsByName(Advanced)

    def retranslateUi(self, Advanced):
        _translate = QtCore.QCoreApplication.translate
        Advanced.setWindowTitle(_translate("Advanced", "Events"))
        self.label_2.setText(_translate("Advanced", "End ID:"))
        self.comboBoxAvgGroup.setItemText(0, _translate("Advanced", "1"))
        self.comboBoxAvgGroup.setItemText(1, _translate("Advanced", "2"))
        self.comboBoxAvgGroup.setItemText(2, _translate("Advanced", "3"))
        self.comboBoxAvgGroup.setItemText(3, _translate("Advanced", "4"))
        self.comboBoxAvgGroup.setItemText(4, _translate("Advanced", "5"))
        self.comboBoxAvgGroup.setItemText(5, _translate("Advanced", "6"))
        self.comboBoxAvgGroup.setItemText(6, _translate("Advanced", "7"))
        self.comboBoxAvgGroup.setItemText(7, _translate("Advanced", "8"))
        self.labelGroup.setText(_translate("Advanced", "Average group:"))
        self.label.setText(_translate("Advanced", "Start ID:"))
        self.pushButtonMaskStart.setText(_translate("Advanced", "Edit..."))
        self.pushButtonMaskEnd.setText(_translate("Advanced", "Edit..."))
        self.pushButtonCancel.setText(_translate("Advanced", "Cancel"))
        self.pushButtonAccept.setText(_translate("Advanced", "Add"))

