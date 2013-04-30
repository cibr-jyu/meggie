# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TFRfromEpochs.ui'
#
# Created: Fri Apr 26 16:03:58 2013
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_DialogEpochsTFR(object):
    def setupUi(self, DialogEpochsTFR):
        DialogEpochsTFR.setObjectName(_fromUtf8("DialogEpochsTFR"))
        DialogEpochsTFR.resize(321, 275)
        self.layoutWidget = QtGui.QWidget(DialogEpochsTFR)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 269, 191))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBoxFrequencies = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxFrequencies.setObjectName(_fromUtf8("groupBoxFrequencies"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBoxFrequencies)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 30, 211, 111))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.comboBoxChannels = QtGui.QComboBox(self.layoutWidget1)
        self.comboBoxChannels.setObjectName(_fromUtf8("comboBoxChannels"))
        self.verticalLayout_6.addWidget(self.comboBoxChannels)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.labelMinFreq = QtGui.QLabel(self.layoutWidget1)
        self.labelMinFreq.setObjectName(_fromUtf8("labelMinFreq"))
        self.horizontalLayout_13.addWidget(self.labelMinFreq)
        self.doubleSpinBoxMinFreq = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.doubleSpinBoxMinFreq.setObjectName(_fromUtf8("doubleSpinBoxMinFreq"))
        self.horizontalLayout_13.addWidget(self.doubleSpinBoxMinFreq)
        self.verticalLayout_6.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.labelMaxFreq = QtGui.QLabel(self.layoutWidget1)
        self.labelMaxFreq.setObjectName(_fromUtf8("labelMaxFreq"))
        self.horizontalLayout_12.addWidget(self.labelMaxFreq)
        self.doubleSpinBoxMaxFreq = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.doubleSpinBoxMaxFreq.setObjectName(_fromUtf8("doubleSpinBoxMaxFreq"))
        self.horizontalLayout_12.addWidget(self.doubleSpinBoxMaxFreq)
        self.verticalLayout_6.addLayout(self.horizontalLayout_12)
        self.verticalLayout.addWidget(self.groupBoxFrequencies)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DialogEpochsTFR)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogEpochsTFR.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogEpochsTFR.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogEpochsTFR)

    def retranslateUi(self, DialogEpochsTFR):
        DialogEpochsTFR.setWindowTitle(_translate("DialogEpochsTFR", "TFR from epochs", None))
        self.groupBoxFrequencies.setTitle(_translate("DialogEpochsTFR", "Frequency window", None))
        self.labelMinFreq.setText(_translate("DialogEpochsTFR", "Minimum frequency:", None))
        self.labelMaxFreq.setText(_translate("DialogEpochsTFR", "Maximum frequency:", None))

