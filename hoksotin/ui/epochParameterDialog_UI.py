# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameterDialog.ui'
#
# Created: Fri Apr 12 15:14:46 2013
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
        ParameterDialog.resize(577, 331)
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(ParameterDialog)
        self.cancelOkButtonBox.setEnabled(True)
        self.cancelOkButtonBox.setGeometry(QtCore.QRect(390, 300, 176, 31))
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.pushButtonAdd = QtGui.QPushButton(ParameterDialog)
        self.pushButtonAdd.setGeometry(QtCore.QRect(230, 300, 95, 31))
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.widget = QtGui.QWidget(ParameterDialog)
        self.widget.setGeometry(QtCore.QRect(20, 10, 541, 281))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelStimulus = QtGui.QLabel(self.widget)
        self.labelStimulus.setObjectName(_fromUtf8("labelStimulus"))
        self.horizontalLayout_2.addWidget(self.labelStimulus)
        self.comboBoxStimulus = QtGui.QComboBox(self.widget)
        self.comboBoxStimulus.setObjectName(_fromUtf8("comboBoxStimulus"))
        self.horizontalLayout_2.addWidget(self.comboBoxStimulus)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelEventID = QtGui.QLabel(self.widget)
        self.labelEventID.setObjectName(_fromUtf8("labelEventID"))
        self.horizontalLayout_7.addWidget(self.labelEventID)
        self.comboBoxEventID = QtGui.QComboBox(self.widget)
        self.comboBoxEventID.setObjectName(_fromUtf8("comboBoxEventID"))
        self.horizontalLayout_7.addWidget(self.comboBoxEventID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.widget)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        self.doubleSpinBoxTmin = QtGui.QDoubleSpinBox(self.widget)
        self.doubleSpinBoxTmin.setMinimum(-10.0)
        self.doubleSpinBoxTmin.setSingleStep(0.1)
        self.doubleSpinBoxTmin.setProperty("value", -0.2)
        self.doubleSpinBoxTmin.setObjectName(_fromUtf8("doubleSpinBoxTmin"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxTmin)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelTmax = QtGui.QLabel(self.widget)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout_4.addWidget(self.labelTmax)
        self.doubleSpinBoxTmax = QtGui.QDoubleSpinBox(self.widget)
        self.doubleSpinBoxTmax.setMaximum(9.9)
        self.doubleSpinBoxTmax.setSingleStep(0.1)
        self.doubleSpinBoxTmax.setProperty("value", 0.5)
        self.doubleSpinBoxTmax.setObjectName(_fromUtf8("doubleSpinBoxTmax"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxTmax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelName = QtGui.QLabel(self.widget)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout_5.addWidget(self.labelName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.lineEditName = QtGui.QLineEdit(self.widget)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.horizontalLayout_5.addWidget(self.lineEditName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBoxMag = QtGui.QCheckBox(self.widget)
        self.checkBoxMag.setObjectName(_fromUtf8("checkBoxMag"))
        self.horizontalLayout_6.addWidget(self.checkBoxMag)
        self.checkBoxGrad = QtGui.QCheckBox(self.widget)
        self.checkBoxGrad.setObjectName(_fromUtf8("checkBoxGrad"))
        self.horizontalLayout_6.addWidget(self.checkBoxGrad)
        self.checkBoxEeg = QtGui.QCheckBox(self.widget)
        self.checkBoxEeg.setObjectName(_fromUtf8("checkBoxEeg"))
        self.horizontalLayout_6.addWidget(self.checkBoxEeg)
        self.checkBoxStim = QtGui.QCheckBox(self.widget)
        self.checkBoxStim.setObjectName(_fromUtf8("checkBoxStim"))
        self.horizontalLayout_6.addWidget(self.checkBoxStim)
        self.checkBoxEog = QtGui.QCheckBox(self.widget)
        self.checkBoxEog.setObjectName(_fromUtf8("checkBoxEog"))
        self.horizontalLayout_6.addWidget(self.checkBoxEog)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.listWidgetEvents = QtGui.QListWidget(self.widget)
        self.listWidgetEvents.setObjectName(_fromUtf8("listWidgetEvents"))
        self.horizontalLayout_3.addWidget(self.listWidgetEvents)

        self.retranslateUi(ParameterDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ParameterDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ParameterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ParameterDialog)

    def retranslateUi(self, ParameterDialog):
        ParameterDialog.setWindowTitle(_translate("ParameterDialog", "Give parameters", None))
        self.pushButtonAdd.setText(_translate("ParameterDialog", "Add to list >>", None))
        self.labelStimulus.setText(_translate("ParameterDialog", "Stimulus channel:", None))
        self.labelEventID.setText(_translate("ParameterDialog", "Event ID:", None))
        self.labelTmin.setText(_translate("ParameterDialog", "Start time:", None))
        self.labelTmax.setText(_translate("ParameterDialog", "End time:", None))
        self.labelName.setText(_translate("ParameterDialog", "Event name:      ", None))
        self.label.setText(_translate("ParameterDialog", "Include:", None))
        self.checkBoxMag.setText(_translate("ParameterDialog", "mag", None))
        self.checkBoxGrad.setText(_translate("ParameterDialog", "grad", None))
        self.checkBoxEeg.setText(_translate("ParameterDialog", "eeg", None))
        self.checkBoxStim.setText(_translate("ParameterDialog", "stim", None))
        self.checkBoxEog.setText(_translate("ParameterDialog", "eog", None))

