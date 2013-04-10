# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameterDialog.ui'
#
# Created: Wed Apr 10 17:52:28 2013
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

class Ui_ParameterDialog(object):
    def setupUi(self, ParameterDialog):
        ParameterDialog.setObjectName(_fromUtf8("ParameterDialog"))
        ParameterDialog.setWindowModality(QtCore.Qt.WindowModal)
        ParameterDialog.resize(391, 319)
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(ParameterDialog)
        self.cancelOkButtonBox.setGeometry(QtCore.QRect(200, 270, 176, 31))
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.layoutWidget = QtGui.QWidget(ParameterDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 6, 351, 251))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelStimulus = QtGui.QLabel(self.layoutWidget)
        self.labelStimulus.setObjectName(_fromUtf8("labelStimulus"))
        self.horizontalLayout_2.addWidget(self.labelStimulus)
        self.comboBoxStimulus = QtGui.QComboBox(self.layoutWidget)
        self.comboBoxStimulus.setObjectName(_fromUtf8("comboBoxStimulus"))
        self.horizontalLayout_2.addWidget(self.comboBoxStimulus)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelEventID = QtGui.QLabel(self.layoutWidget)
        self.labelEventID.setObjectName(_fromUtf8("labelEventID"))
        self.horizontalLayout_7.addWidget(self.labelEventID)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem)
        self.spinBoxEventID = QtGui.QSpinBox(self.layoutWidget)
        self.spinBoxEventID.setMinimum(1)
        self.spinBoxEventID.setMaximum(65536)
        self.spinBoxEventID.setObjectName(_fromUtf8("spinBoxEventID"))
        self.horizontalLayout_7.addWidget(self.spinBoxEventID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.layoutWidget)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.doubleSpinBoxTmin = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxTmin.setMinimum(-10.0)
        self.doubleSpinBoxTmin.setSingleStep(0.1)
        self.doubleSpinBoxTmin.setProperty("value", -0.2)
        self.doubleSpinBoxTmin.setObjectName(_fromUtf8("doubleSpinBoxTmin"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxTmin)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelTmax = QtGui.QLabel(self.layoutWidget)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout_4.addWidget(self.labelTmax)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.doubleSpinBoxTmax = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxTmax.setObjectName(_fromUtf8("doubleSpinBoxTmax"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxTmax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelName = QtGui.QLabel(self.layoutWidget)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout_5.addWidget(self.labelName)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lineEditName = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.horizontalLayout_5.addWidget(self.lineEditName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBoxMag = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxMag.setObjectName(_fromUtf8("checkBoxMag"))
        self.horizontalLayout_6.addWidget(self.checkBoxMag)
        self.checkBoxGrad = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxGrad.setObjectName(_fromUtf8("checkBoxGrad"))
        self.horizontalLayout_6.addWidget(self.checkBoxGrad)
        self.checkBoxEeg = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxEeg.setObjectName(_fromUtf8("checkBoxEeg"))
        self.horizontalLayout_6.addWidget(self.checkBoxEeg)
        self.checkBoxStim = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxStim.setObjectName(_fromUtf8("checkBoxStim"))
        self.horizontalLayout_6.addWidget(self.checkBoxStim)
        self.checkBoxEog = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxEog.setObjectName(_fromUtf8("checkBoxEog"))
        self.horizontalLayout_6.addWidget(self.checkBoxEog)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.retranslateUi(ParameterDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ParameterDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ParameterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ParameterDialog)

    def retranslateUi(self, ParameterDialog):
        ParameterDialog.setWindowTitle(_translate("ParameterDialog", "Give parameters", None))
        self.labelStimulus.setText(_translate("ParameterDialog", "Stimulus channel:", None))
        self.labelEventID.setText(_translate("ParameterDialog", "Event ID:", None))
        self.labelTmin.setText(_translate("ParameterDialog", "Start time:", None))
        self.labelTmax.setText(_translate("ParameterDialog", "End time:", None))
        self.labelName.setText(_translate("ParameterDialog", "Epoch name:      ", None))
        self.checkBoxMag.setText(_translate("ParameterDialog", "mag", None))
        self.checkBoxGrad.setText(_translate("ParameterDialog", "grad", None))
        self.checkBoxEeg.setText(_translate("ParameterDialog", "eeg", None))
        self.checkBoxStim.setText(_translate("ParameterDialog", "stim", None))
        self.checkBoxEog.setText(_translate("ParameterDialog", "eog", None))

