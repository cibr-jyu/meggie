# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupAverageTFR.ui'
#
# Created: Wed Apr  1 08:19:42 2015
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_DialogGroupTFR(object):
    def setupUi(self, DialogGroupTFR):
        DialogGroupTFR.setObjectName(_fromUtf8("DialogGroupTFR"))
        DialogGroupTFR.resize(712, 273)
        self.gridLayout = QtGui.QGridLayout(DialogGroupTFR)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(DialogGroupTFR)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBoxSavePlot = QtGui.QCheckBox(self.groupBox)
        self.checkBoxSavePlot.setObjectName(_fromUtf8("checkBoxSavePlot"))
        self.verticalLayout.addWidget(self.checkBoxSavePlot)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.listWidgetChannels = QtGui.QListWidget(self.groupBox)
        self.listWidgetChannels.setEnabled(False)
        self.listWidgetChannels.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.listWidgetChannels.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.listWidgetChannels.setFlow(QtGui.QListView.LeftToRight)
        self.listWidgetChannels.setObjectName(_fromUtf8("listWidgetChannels"))
        self.verticalLayout_2.addWidget(self.listWidgetChannels)
        self.pushButtonModify = QtGui.QPushButton(self.groupBox)
        self.pushButtonModify.setEnabled(False)
        self.pushButtonModify.setObjectName(_fromUtf8("pushButtonModify"))
        self.verticalLayout_2.addWidget(self.pushButtonModify)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.checkBoxSaveTopo = QtGui.QCheckBox(DialogGroupTFR)
        self.checkBoxSaveTopo.setObjectName(_fromUtf8("checkBoxSaveTopo"))
        self.verticalLayout_3.addWidget(self.checkBoxSaveTopo)
        self.gridLayout.addLayout(self.verticalLayout_3, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DialogGroupTFR)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(DialogGroupTFR)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.comboBoxFormat = QtGui.QComboBox(DialogGroupTFR)
        self.comboBoxFormat.setObjectName(_fromUtf8("comboBoxFormat"))
        self.comboBoxFormat.addItem(_fromUtf8(""))
        self.comboBoxFormat.addItem(_fromUtf8(""))
        self.comboBoxFormat.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBoxFormat)
        self.line = QtGui.QFrame(DialogGroupTFR)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout_2.addWidget(self.line)
        self.label = QtGui.QLabel(DialogGroupTFR)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.spinBoxDpi = QtGui.QSpinBox(DialogGroupTFR)
        self.spinBoxDpi.setMinimum(100)
        self.spinBoxDpi.setMaximum(1200)
        self.spinBoxDpi.setSingleStep(10)
        self.spinBoxDpi.setProperty("value", 600)
        self.spinBoxDpi.setObjectName(_fromUtf8("spinBoxDpi"))
        self.horizontalLayout_2.addWidget(self.spinBoxDpi)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(DialogGroupTFR)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogGroupTFR.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogGroupTFR.reject)
        QtCore.QObject.connect(self.checkBoxSavePlot, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.listWidgetChannels.setEnabled)
        QtCore.QObject.connect(self.checkBoxSavePlot, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.pushButtonModify.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(DialogGroupTFR)
        DialogGroupTFR.setTabOrder(self.comboBoxFormat, self.spinBoxDpi)
        DialogGroupTFR.setTabOrder(self.spinBoxDpi, self.checkBoxSavePlot)
        DialogGroupTFR.setTabOrder(self.checkBoxSavePlot, self.listWidgetChannels)
        DialogGroupTFR.setTabOrder(self.listWidgetChannels, self.pushButtonModify)
        DialogGroupTFR.setTabOrder(self.pushButtonModify, self.checkBoxSaveTopo)
        DialogGroupTFR.setTabOrder(self.checkBoxSaveTopo, self.buttonBox)

    def retranslateUi(self, DialogGroupTFR):
        DialogGroupTFR.setWindowTitle(_translate("DialogGroupTFR", "Group average TFR", None))
        self.groupBox.setTitle(_translate("DialogGroupTFR", "Channels of interest.", None))
        self.checkBoxSavePlot.setText(_translate("DialogGroupTFR", "Save plot figures for each subject.", None))
        self.pushButtonModify.setText(_translate("DialogGroupTFR", "Modify...", None))
        self.checkBoxSaveTopo.setText(_translate("DialogGroupTFR", "Save topo plot of group average.", None))
        self.label_2.setText(_translate("DialogGroupTFR", "Picture format:", None))
        self.comboBoxFormat.setItemText(0, _translate("DialogGroupTFR", "png", None))
        self.comboBoxFormat.setItemText(1, _translate("DialogGroupTFR", "svg", None))
        self.comboBoxFormat.setItemText(2, _translate("DialogGroupTFR", "pdf", None))
        self.label.setText(_translate("DialogGroupTFR", "Dots per inch (dpi):", None))

