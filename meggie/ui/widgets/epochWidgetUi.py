# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'epochWidget.ui'
#
# Created: Tue Aug 25 01:40:04 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(409, 334)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_14 = QtGui.QVBoxLayout()
        self.verticalLayout_14.setObjectName(_fromUtf8("verticalLayout_14"))
        self.groupBoxEpochs = QtGui.QGroupBox(Form)
        self.groupBoxEpochs.setObjectName(_fromUtf8("groupBoxEpochs"))
        self.listWidgetEpochs = QtGui.QListWidget(self.groupBoxEpochs)
        self.listWidgetEpochs.setGeometry(QtCore.QRect(10, 30, 361, 121))
        self.listWidgetEpochs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.listWidgetEpochs.setObjectName(_fromUtf8("listWidgetEpochs"))
        self.groupBoxEvents = QtGui.QGroupBox(self.groupBoxEpochs)
        self.groupBoxEvents.setGeometry(QtCore.QRect(0, 150, 391, 151))
        self.groupBoxEvents.setObjectName(_fromUtf8("groupBoxEvents"))
        self.listWidgetEvents = QtGui.QListWidget(self.groupBoxEvents)
        self.listWidgetEvents.setEnabled(True)
        self.listWidgetEvents.setGeometry(QtCore.QRect(10, 30, 361, 111))
        self.listWidgetEvents.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.listWidgetEvents.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.listWidgetEvents.setObjectName(_fromUtf8("listWidgetEvents"))
        item = QtGui.QListWidgetItem()
        self.listWidgetEvents.addItem(item)
        item = QtGui.QListWidgetItem()
        self.listWidgetEvents.addItem(item)
        self.verticalLayout_14.addWidget(self.groupBoxEpochs)
        self.gridLayout_2.addLayout(self.verticalLayout_14, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBoxEpochs.setTitle(_translate("Form", "Epoch collections:", None))
        self.groupBoxEvents.setTitle(_translate("Form", "Events in currently selected epoch collection:", None))
        __sortingEnabled = self.listWidgetEvents.isSortingEnabled()
        self.listWidgetEvents.setSortingEnabled(False)
        self.listWidgetEvents.setSortingEnabled(__sortingEnabled)

