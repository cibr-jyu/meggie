# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forwardSolutionDialogUi.ui'
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

class Ui_DialogCreateFSolution(object):
    def setupUi(self, DialogCreateFSolution):
        DialogCreateFSolution.setObjectName(_fromUtf8("DialogCreateFSolution"))
        DialogCreateFSolution.resize(497, 200)
        self.gridLayout = QtGui.QGridLayout(DialogCreateFSolution)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.frame = QtGui.QFrame(DialogCreateFSolution)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.formLayout = QtGui.QFormLayout(self.frame)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelIncludeMEG = QtGui.QLabel(self.frame)
        self.labelIncludeMEG.setObjectName(_fromUtf8("labelIncludeMEG"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelIncludeMEG)
        self.checkBoxIncludeMEG = QtGui.QCheckBox(self.frame)
        self.checkBoxIncludeMEG.setText(_fromUtf8(""))
        self.checkBoxIncludeMEG.setChecked(True)
        self.checkBoxIncludeMEG.setObjectName(_fromUtf8("checkBoxIncludeMEG"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.checkBoxIncludeMEG)
        self.labelIncludEEG = QtGui.QLabel(self.frame)
        self.labelIncludEEG.setObjectName(_fromUtf8("labelIncludEEG"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelIncludEEG)
        self.checkBoxIncludeEEG = QtGui.QCheckBox(self.frame)
        self.checkBoxIncludeEEG.setText(_fromUtf8(""))
        self.checkBoxIncludeEEG.setChecked(True)
        self.checkBoxIncludeEEG.setObjectName(_fromUtf8("checkBoxIncludeEEG"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.checkBoxIncludeEEG)
        self.labelMinDist = QtGui.QLabel(self.frame)
        self.labelMinDist.setObjectName(_fromUtf8("labelMinDist"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelMinDist)
        self.doubleSpinBoxMinDist = QtGui.QDoubleSpinBox(self.frame)
        self.doubleSpinBoxMinDist.setDecimals(1)
        self.doubleSpinBoxMinDist.setObjectName(_fromUtf8("doubleSpinBoxMinDist"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxMinDist)
        self.labelIgnoreRef = QtGui.QLabel(self.frame)
        self.labelIgnoreRef.setObjectName(_fromUtf8("labelIgnoreRef"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelIgnoreRef)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButtonIgnoreNo = QtGui.QRadioButton(self.frame)
        self.radioButtonIgnoreNo.setChecked(True)
        self.radioButtonIgnoreNo.setObjectName(_fromUtf8("radioButtonIgnoreNo"))
        self.buttonGroupIgnoreRef = QtGui.QButtonGroup(DialogCreateFSolution)
        self.buttonGroupIgnoreRef.setObjectName(_fromUtf8("buttonGroupIgnoreRef"))
        self.buttonGroupIgnoreRef.addButton(self.radioButtonIgnoreNo)
        self.horizontalLayout.addWidget(self.radioButtonIgnoreNo)
        self.radioButtonIgnoreYes = QtGui.QRadioButton(self.frame)
        self.radioButtonIgnoreYes.setObjectName(_fromUtf8("radioButtonIgnoreYes"))
        self.buttonGroupIgnoreRef.addButton(self.radioButtonIgnoreYes)
        self.horizontalLayout.addWidget(self.radioButtonIgnoreYes)
        self.formLayout.setLayout(3, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DialogCreateFSolution)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(DialogCreateFSolution)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogCreateFSolution.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogCreateFSolution.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogCreateFSolution)

    def retranslateUi(self, DialogCreateFSolution):
        DialogCreateFSolution.setWindowTitle(_translate("DialogCreateFSolution", "Create forward solution", None))
        self.labelIncludeMEG.setText(_translate("DialogCreateFSolution", "Include MEG computations:", None))
        self.labelIncludEEG.setText(_translate("DialogCreateFSolution", "Include EEG computations:", None))
        self.labelMinDist.setText(_translate("DialogCreateFSolution", "<html><head/><body><p>Minimum distance:</p></body></html>", None))
        self.doubleSpinBoxMinDist.setSuffix(_translate("DialogCreateFSolution", " mm", None))
        self.labelIgnoreRef.setText(_translate("DialogCreateFSolution", "Ignore reference channels for compensation:", None))
        self.radioButtonIgnoreNo.setText(_translate("DialogCreateFSolution", "no (default)", None))
        self.radioButtonIgnoreYes.setText(_translate("DialogCreateFSolution", "yes", None))

