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
        DialogRawTFR.resize(453, 219)
        self.gridLayout = QtGui.QGridLayout(DialogRawTFR)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(DialogRawTFR)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(DialogRawTFR)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.spinBoxWsize = QtGui.QSpinBox(DialogRawTFR)
        self.spinBoxWsize.setMaximum(100)
        self.spinBoxWsize.setSingleStep(1)
        self.spinBoxWsize.setProperty("value", 4)
        self.spinBoxWsize.setObjectName(_fromUtf8("spinBoxWsize"))
        self.horizontalLayout.addWidget(self.spinBoxWsize)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(DialogRawTFR)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.checkBoxTstep = QtGui.QCheckBox(DialogRawTFR)
        self.checkBoxTstep.setChecked(True)
        self.checkBoxTstep.setObjectName(_fromUtf8("checkBoxTstep"))
        self.verticalLayout.addWidget(self.checkBoxTstep)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(DialogRawTFR)
        self.label_2.setEnabled(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.spinBoxTstep = QtGui.QSpinBox(DialogRawTFR)
        self.spinBoxTstep.setEnabled(False)
        self.spinBoxTstep.setMaximum(50)
        self.spinBoxTstep.setSingleStep(1)
        self.spinBoxTstep.setProperty("value", 2)
        self.spinBoxTstep.setObjectName(_fromUtf8("spinBoxTstep"))
        self.horizontalLayout_2.addWidget(self.spinBoxTstep)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line_2 = QtGui.QFrame(DialogRawTFR)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(DialogRawTFR)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogRawTFR.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogRawTFR.reject)
        QtCore.QObject.connect(self.checkBoxTstep, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.spinBoxTstep.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(DialogRawTFR)

    def retranslateUi(self, DialogRawTFR):
        DialogRawTFR.setWindowTitle(_translate("DialogRawTFR", "Meggie - TFR from raw", None))
        self.label.setText(_translate("DialogRawTFR", "Length of the STFT window in samples:", None))
        self.checkBoxTstep.setText(_translate("DialogRawTFR", "Use default step (=window length / 2)", None))
        self.label_2.setText(_translate("DialogRawTFR", "Step between successive windows in samples:", None))

