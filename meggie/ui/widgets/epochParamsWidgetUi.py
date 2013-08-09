# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'epochParamsWidget.ui'
#
# Created: Fri Aug  9 09:26:26 2013
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(469, 244)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(9, 9, 451, 231))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.groupBox)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        self.labelTmax = QtGui.QLabel(self.groupBox)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout.addWidget(self.labelTmax)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBoxMag = QtGui.QCheckBox(self.groupBox)
        self.checkBoxMag.setEnabled(False)
        self.checkBoxMag.setCheckable(True)
        self.checkBoxMag.setChecked(False)
        self.checkBoxMag.setObjectName(_fromUtf8("checkBoxMag"))
        self.horizontalLayout_6.addWidget(self.checkBoxMag)
        self.checkBoxGrad = QtGui.QCheckBox(self.groupBox)
        self.checkBoxGrad.setEnabled(False)
        self.checkBoxGrad.setChecked(False)
        self.checkBoxGrad.setObjectName(_fromUtf8("checkBoxGrad"))
        self.horizontalLayout_6.addWidget(self.checkBoxGrad)
        self.checkBoxEeg = QtGui.QCheckBox(self.groupBox)
        self.checkBoxEeg.setEnabled(False)
        self.checkBoxEeg.setChecked(False)
        self.checkBoxEeg.setObjectName(_fromUtf8("checkBoxEeg"))
        self.horizontalLayout_6.addWidget(self.checkBoxEeg)
        self.checkBoxStim = QtGui.QCheckBox(self.groupBox)
        self.checkBoxStim.setEnabled(False)
        self.checkBoxStim.setChecked(False)
        self.checkBoxStim.setObjectName(_fromUtf8("checkBoxStim"))
        self.horizontalLayout_6.addWidget(self.checkBoxStim)
        self.checkBoxEog = QtGui.QCheckBox(self.groupBox)
        self.checkBoxEog.setEnabled(False)
        self.checkBoxEog.setChecked(False)
        self.checkBoxEog.setObjectName(_fromUtf8("checkBoxEog"))
        self.horizontalLayout_6.addWidget(self.checkBoxEog)
        self.gridLayout.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelGradReject_3 = QtGui.QLabel(self.groupBox)
        self.labelGradReject_3.setObjectName(_fromUtf8("labelGradReject_3"))
        self.horizontalLayout_2.addWidget(self.labelGradReject_3)
        self.labelMagReject_3 = QtGui.QLabel(self.groupBox)
        self.labelMagReject_3.setObjectName(_fromUtf8("labelMagReject_3"))
        self.horizontalLayout_2.addWidget(self.labelMagReject_3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelEegReject_3 = QtGui.QLabel(self.groupBox)
        self.labelEegReject_3.setObjectName(_fromUtf8("labelEegReject_3"))
        self.horizontalLayout_3.addWidget(self.labelEegReject_3)
        self.labelEogReject_3 = QtGui.QLabel(self.groupBox)
        self.labelEogReject_3.setObjectName(_fromUtf8("labelEogReject_3"))
        self.horizontalLayout_3.addWidget(self.labelEogReject_3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Epoch parameters:", None))
        self.labelTmin.setText(_translate("Form", "Start time:", None))
        self.labelTmax.setText(_translate("Form", "End time:", None))
        self.checkBoxMag.setText(_translate("Form", "mag", None))
        self.checkBoxGrad.setText(_translate("Form", "grad", None))
        self.checkBoxEeg.setText(_translate("Form", "eeg", None))
        self.checkBoxStim.setText(_translate("Form", "stim", None))
        self.checkBoxEog.setText(_translate("Form", "eog", None))
        self.labelGradReject_3.setText(_translate("Form", "Grad:", None))
        self.labelMagReject_3.setText(_translate("Form", "Mag:", None))
        self.labelEegReject_3.setText(_translate("Form", "EEG:", None))
        self.labelEogReject_3.setText(_translate("Form", "EOG:", None))

