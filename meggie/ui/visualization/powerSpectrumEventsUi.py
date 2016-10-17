# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powerSpectrumEventsUi.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Advanced(object):
    def setupUi(self, Advanced):
        Advanced.setObjectName(_fromUtf8("Advanced"))
        Advanced.resize(281, 177)
        self.gridLayout_2 = QtGui.QGridLayout(Advanced)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelGroup = QtGui.QLabel(Advanced)
        self.labelGroup.setObjectName(_fromUtf8("labelGroup"))
        self.gridLayout.addWidget(self.labelGroup, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Advanced)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.comboBoxAvgGroup = QtGui.QComboBox(Advanced)
        self.comboBoxAvgGroup.setObjectName(_fromUtf8("comboBoxAvgGroup"))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.comboBoxAvgGroup.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxAvgGroup, 0, 1, 1, 1)
        self.label = QtGui.QLabel(Advanced)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lineEditStart = QtGui.QLineEdit(Advanced)
        self.lineEditStart.setObjectName(_fromUtf8("lineEditStart"))
        self.gridLayout.addWidget(self.lineEditStart, 1, 1, 1, 1)
        self.lineEditEnd = QtGui.QLineEdit(Advanced)
        self.lineEditEnd.setObjectName(_fromUtf8("lineEditEnd"))
        self.gridLayout.addWidget(self.lineEditEnd, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtGui.QPushButton(Advanced)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtGui.QPushButton(Advanced)
        self.pushButtonAccept.setObjectName(_fromUtf8("pushButtonAccept"))
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Advanced)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Advanced.reject)
        QtCore.QObject.connect(self.pushButtonAccept, QtCore.SIGNAL(_fromUtf8("clicked()")), Advanced.accept)
        QtCore.QMetaObject.connectSlotsByName(Advanced)

    def retranslateUi(self, Advanced):
        Advanced.setWindowTitle(_translate("Advanced", "Events", None))
        self.labelGroup.setText(_translate("Advanced", "Average group:", None))
        self.label_2.setText(_translate("Advanced", "End ID:", None))
        self.comboBoxAvgGroup.setItemText(0, _translate("Advanced", "1", None))
        self.comboBoxAvgGroup.setItemText(1, _translate("Advanced", "2", None))
        self.comboBoxAvgGroup.setItemText(2, _translate("Advanced", "3", None))
        self.comboBoxAvgGroup.setItemText(3, _translate("Advanced", "4", None))
        self.comboBoxAvgGroup.setItemText(4, _translate("Advanced", "5", None))
        self.comboBoxAvgGroup.setItemText(5, _translate("Advanced", "6", None))
        self.comboBoxAvgGroup.setItemText(6, _translate("Advanced", "7", None))
        self.comboBoxAvgGroup.setItemText(7, _translate("Advanced", "8", None))
        self.label.setText(_translate("Advanced", "Start ID:", None))
        self.pushButtonCancel.setText(_translate("Advanced", "Cancel", None))
        self.pushButtonAccept.setText(_translate("Advanced", "Add", None))

