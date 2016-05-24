# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TFRfromRawDialogUi.ui'
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

class Ui_DialogRawTFR(object):
    def setupUi(self, DialogRawTFR):
        DialogRawTFR.setObjectName(_fromUtf8("DialogRawTFR"))
        DialogRawTFR.resize(281, 218)
        self.gridLayout = QtGui.QGridLayout(DialogRawTFR)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.labelMinFreq = QtGui.QLabel(DialogRawTFR)
        self.labelMinFreq.setObjectName(_fromUtf8("labelMinFreq"))
        self.horizontalLayout_13.addWidget(self.labelMinFreq)
        self.doubleSpinBoxMinFreq = QtGui.QDoubleSpinBox(DialogRawTFR)
        self.doubleSpinBoxMinFreq.setMinimum(0.1)
        self.doubleSpinBoxMinFreq.setMaximum(200.0)
        self.doubleSpinBoxMinFreq.setProperty("value", 7.0)
        self.doubleSpinBoxMinFreq.setObjectName(_fromUtf8("doubleSpinBoxMinFreq"))
        self.horizontalLayout_13.addWidget(self.doubleSpinBoxMinFreq)
        self.verticalLayout_6.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.labelMaxFreq = QtGui.QLabel(DialogRawTFR)
        self.labelMaxFreq.setObjectName(_fromUtf8("labelMaxFreq"))
        self.horizontalLayout_12.addWidget(self.labelMaxFreq)
        self.doubleSpinBoxMaxFreq = QtGui.QDoubleSpinBox(DialogRawTFR)
        self.doubleSpinBoxMaxFreq.setMinimum(7.0)
        self.doubleSpinBoxMaxFreq.setMaximum(600.0)
        self.doubleSpinBoxMaxFreq.setProperty("value", 30.0)
        self.doubleSpinBoxMaxFreq.setObjectName(_fromUtf8("doubleSpinBoxMaxFreq"))
        self.horizontalLayout_12.addWidget(self.doubleSpinBoxMaxFreq)
        self.verticalLayout_6.addLayout(self.horizontalLayout_12)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelFrequencyInterval = QtGui.QLabel(DialogRawTFR)
        self.labelFrequencyInterval.setObjectName(_fromUtf8("labelFrequencyInterval"))
        self.horizontalLayout.addWidget(self.labelFrequencyInterval)
        self.doubleSpinBoxFreqInterval = QtGui.QDoubleSpinBox(DialogRawTFR)
        self.doubleSpinBoxFreqInterval.setMinimum(0.1)
        self.doubleSpinBoxFreqInterval.setMaximum(99.99)
        self.doubleSpinBoxFreqInterval.setProperty("value", 3.0)
        self.doubleSpinBoxFreqInterval.setObjectName(_fromUtf8("doubleSpinBoxFreqInterval"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxFreqInterval)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DialogRawTFR)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(DialogRawTFR)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogRawTFR.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogRawTFR.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogRawTFR)

    def retranslateUi(self, DialogRawTFR):
        DialogRawTFR.setWindowTitle(_translate("DialogRawTFR", "Meggie - TFR from raw", None))
        self.labelMinFreq.setText(_translate("DialogRawTFR", "Minimum frequency:", None))
        self.doubleSpinBoxMinFreq.setSuffix(_translate("DialogRawTFR", " Hz", None))
        self.labelMaxFreq.setText(_translate("DialogRawTFR", "Maximum frequency:", None))
        self.doubleSpinBoxMaxFreq.setSuffix(_translate("DialogRawTFR", " Hz", None))
        self.labelFrequencyInterval.setText(_translate("DialogRawTFR", "Frequency interval:", None))
        self.doubleSpinBoxFreqInterval.setSuffix(_translate("DialogRawTFR", " Hz", None))

