# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powerSpectrumEpochsDialogUi.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(772, 344)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 752, 287))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(740, 260))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_3 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBoxConditions = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxConditions.setObjectName(_fromUtf8("groupBoxConditions"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxConditions)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.formLayout_2 = QtGui.QFormLayout()
        self.formLayout_2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.labelFmin = QtGui.QLabel(self.groupBoxConditions)
        self.labelFmin.setObjectName(_fromUtf8("labelFmin"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelFmin)
        self.spinBoxFmin = QtGui.QSpinBox(self.groupBoxConditions)
        self.spinBoxFmin.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxFmin.setObjectName(_fromUtf8("spinBoxFmin"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBoxFmin)
        self.labelFmax = QtGui.QLabel(self.groupBoxConditions)
        self.labelFmax.setObjectName(_fromUtf8("labelFmax"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelFmax)
        self.spinBoxFmax = QtGui.QSpinBox(self.groupBoxConditions)
        self.spinBoxFmax.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxFmax.setMaximum(150)
        self.spinBoxFmax.setProperty("value", 40)
        self.spinBoxFmax.setObjectName(_fromUtf8("spinBoxFmax"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBoxFmax)
        self.horizontalLayout_5.addLayout(self.formLayout_2)
        self.formLayout_6 = QtGui.QFormLayout()
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.labelNfft = QtGui.QLabel(self.groupBoxConditions)
        self.labelNfft.setObjectName(_fromUtf8("labelNfft"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelNfft)
        self.spinBoxNfft = QtGui.QSpinBox(self.groupBoxConditions)
        self.spinBoxNfft.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxNfft.setMaximum(10000)
        self.spinBoxNfft.setProperty("value", 2048)
        self.spinBoxNfft.setObjectName(_fromUtf8("spinBoxNfft"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBoxNfft)
        self.labelOverlap = QtGui.QLabel(self.groupBoxConditions)
        self.labelOverlap.setObjectName(_fromUtf8("labelOverlap"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelOverlap)
        self.spinBoxOverlap = QtGui.QSpinBox(self.groupBoxConditions)
        self.spinBoxOverlap.setMaximum(10000)
        self.spinBoxOverlap.setProperty("value", 1024)
        self.spinBoxOverlap.setObjectName(_fromUtf8("spinBoxOverlap"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBoxOverlap)
        self.checkBoxLogarithm = QtGui.QCheckBox(self.groupBoxConditions)
        self.checkBoxLogarithm.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkBoxLogarithm.setAutoFillBackground(False)
        self.checkBoxLogarithm.setChecked(True)
        self.checkBoxLogarithm.setObjectName(_fromUtf8("checkBoxLogarithm"))
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.LabelRole, self.checkBoxLogarithm)
        self.horizontalLayout_5.addLayout(self.formLayout_6)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxConditions, 0, 0, 1, 1)
        self.checkBoxAverage = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBoxAverage.setChecked(False)
        self.checkBoxAverage.setObjectName(_fromUtf8("checkBoxAverage"))
        self.gridLayout_3.addWidget(self.checkBoxAverage, 1, 0, 1, 1)
        self.line = QtGui.QFrame(self.scrollAreaWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_3.addWidget(self.line, 2, 0, 1, 1)
        self.checkBoxSaveData = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBoxSaveData.setObjectName(_fromUtf8("checkBoxSaveData"))
        self.gridLayout_3.addWidget(self.checkBoxSaveData, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Meggie - Power spectrum epochs", None))
        self.groupBoxConditions.setTitle(_translate("Dialog", "Conditions", None))
        self.labelFmin.setToolTip(_translate("Dialog", "Set the lower limit for the frequencies.", None))
        self.labelFmin.setText(_translate("Dialog", "Min frequency of interest:", None))
        self.spinBoxFmin.setToolTip(_translate("Dialog", "Set the lower limit for the frequencies.", None))
        self.spinBoxFmin.setSuffix(_translate("Dialog", "Hz", None))
        self.labelFmax.setToolTip(_translate("Dialog", "Set the upper limit for the frequencies.", None))
        self.labelFmax.setText(_translate("Dialog", "Max frequency of interest:", None))
        self.spinBoxFmax.setToolTip(_translate("Dialog", "Set the upper limit for the frequencies.", None))
        self.spinBoxFmax.setSuffix(_translate("Dialog", "Hz", None))
        self.labelNfft.setToolTip(_translate("Dialog", "<html><head/><body><p>The length of the tapers ie. the windows (hanning). The smaller it is the smoother are the PSDs.</p></body></html>", None))
        self.labelNfft.setText(_translate("Dialog", "Length of the tapers (ie. the windows):", None))
        self.spinBoxNfft.setToolTip(_translate("Dialog", "<html><head/><body><p>The length of the tapers ie. the windows (hanning). The smaller it is the smoother are the PSDs.</p></body></html>", None))
        self.labelOverlap.setToolTip(_translate("Dialog", "<html><head/><body><p>Number of overlapping points between the blocks.</p></body></html>", None))
        self.labelOverlap.setText(_translate("Dialog", "Overlap", None))
        self.spinBoxOverlap.setToolTip(_translate("Dialog", "<html><head/><body><p>Number of overlapping points between the blocks.</p></body></html>", None))
        self.checkBoxLogarithm.setToolTip(_translate("Dialog", "Use logarithmic scale.", None))
        self.checkBoxLogarithm.setText(_translate("Dialog", "Use logarithmic scale", None))
        self.checkBoxAverage.setText(_translate("Dialog", "Average the selected collections together", None))
        self.checkBoxSaveData.setText(_translate("Dialog", "Save data to file", None))

