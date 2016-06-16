# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layoutDialogUi.ui'
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

class Ui_Layout(object):
    def setupUi(self, Layout):
        Layout.setObjectName(_fromUtf8("Layout"))
        Layout.resize(532, 171)
        self.gridLayout = QtGui.QGridLayout(Layout)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.radioButtonSelectLayout = QtGui.QRadioButton(Layout)
        self.radioButtonSelectLayout.setChecked(True)
        self.radioButtonSelectLayout.setObjectName(_fromUtf8("radioButtonSelectLayout"))
        self.gridLayout_2.addWidget(self.radioButtonSelectLayout, 0, 0, 1, 1)
        self.pushButtonBrowseLayout = QtGui.QPushButton(Layout)
        self.pushButtonBrowseLayout.setEnabled(False)
        self.pushButtonBrowseLayout.setObjectName(_fromUtf8("pushButtonBrowseLayout"))
        self.gridLayout_2.addWidget(self.pushButtonBrowseLayout, 1, 1, 1, 1)
        self.radioButtonLayoutFromFile = QtGui.QRadioButton(Layout)
        self.radioButtonLayoutFromFile.setObjectName(_fromUtf8("radioButtonLayoutFromFile"))
        self.gridLayout_2.addWidget(self.radioButtonLayoutFromFile, 1, 0, 1, 1)
        self.comboBoxLayout = QtGui.QComboBox(Layout)
        self.comboBoxLayout.setObjectName(_fromUtf8("comboBoxLayout"))
        self.comboBoxLayout.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.comboBoxLayout, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Layout)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 2, 0, 1, 1)
        self.labelLayout = QtGui.QLabel(Layout)
        self.labelLayout.setObjectName(_fromUtf8("labelLayout"))
        self.gridLayout_2.addWidget(self.labelLayout, 2, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.line = QtGui.QFrame(Layout)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(Layout)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.labelLayoutActive = QtGui.QLabel(Layout)
        self.labelLayoutActive.setObjectName(_fromUtf8("labelLayoutActive"))
        self.horizontalLayout_3.addWidget(self.labelLayoutActive)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonReject_2 = QtGui.QPushButton(Layout)
        self.pushButtonReject_2.setObjectName(_fromUtf8("pushButtonReject_2"))
        self.horizontalLayout.addWidget(self.pushButtonReject_2)
        self.pushButtonAccept = QtGui.QPushButton(Layout)
        self.pushButtonAccept.setObjectName(_fromUtf8("pushButtonAccept"))
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Layout)
        QtCore.QObject.connect(self.radioButtonLayoutFromFile, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.pushButtonBrowseLayout.setEnabled)
        QtCore.QObject.connect(self.pushButtonReject_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Layout.reject)
        QtCore.QObject.connect(self.pushButtonAccept, QtCore.SIGNAL(_fromUtf8("clicked()")), Layout.accept)
        QtCore.QMetaObject.connectSlotsByName(Layout)

    def retranslateUi(self, Layout):
        Layout.setWindowTitle(_translate("Layout", "Meggie - Select layout", None))
        self.radioButtonSelectLayout.setText(_translate("Layout", "Select layout", None))
        self.pushButtonBrowseLayout.setText(_translate("Layout", "Browse...", None))
        self.radioButtonLayoutFromFile.setText(_translate("Layout", "Layout from file", None))
        self.comboBoxLayout.setItemText(0, _translate("Layout", "Infer from data", None))
        self.label_2.setText(_translate("Layout", "Change layout to:", None))
        self.labelLayout.setText(_translate("Layout", "Infer from data", None))
        self.label.setText(_translate("Layout", "Layout currently:", None))
        self.labelLayoutActive.setText(_translate("Layout", "Infer from data", None))
        self.pushButtonReject_2.setText(_translate("Layout", "Cancel", None))
        self.pushButtonAccept.setText(_translate("Layout", "Ok", None))

