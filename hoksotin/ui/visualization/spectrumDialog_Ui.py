# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectrumDialog.ui'
#
# Created: Wed May 15 15:21:44 2013
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

class Ui_DialogSpectrum(object):
    def setupUi(self, DialogSpectrum):
        DialogSpectrum.setObjectName(_fromUtf8("DialogSpectrum"))
        DialogSpectrum.resize(270, 159)
        self.gridLayout = QtGui.QGridLayout(DialogSpectrum)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(DialogSpectrum)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.comboBoxChannel = QtGui.QComboBox(DialogSpectrum)
        self.comboBoxChannel.setObjectName(_fromUtf8("comboBoxChannel"))
        self.verticalLayout.addWidget(self.comboBoxChannel)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DialogSpectrum)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(DialogSpectrum)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogSpectrum.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogSpectrum.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogSpectrum)

    def retranslateUi(self, DialogSpectrum):
        DialogSpectrum.setWindowTitle(_translate("DialogSpectrum", "Dialog", None))
        self.label.setText(_translate("DialogSpectrum", "Select a channel", None))

