# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameterDialog.ui'
#
# Created: Thu Mar 21 15:40:24 2013
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
        self.cancelOkButtonBox.setGeometry(QtCore.QRect(20, 270, 176, 31))
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
        self.lineEditEventID = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditEventID.setObjectName(_fromUtf8("lineEditEventID"))
        self.horizontalLayout_7.addWidget(self.lineEditEventID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.layoutWidget)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.lineEditTmin = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditTmin.setObjectName(_fromUtf8("lineEditTmin"))
        self.horizontalLayout.addWidget(self.lineEditTmin)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelTmax = QtGui.QLabel(self.layoutWidget)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout_4.addWidget(self.labelTmax)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.lineEditTmax = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditTmax.setObjectName(_fromUtf8("lineEditTmax"))
        self.horizontalLayout_4.addWidget(self.lineEditTmax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelReject = QtGui.QLabel(self.layoutWidget)
        self.labelReject.setObjectName(_fromUtf8("labelReject"))
        self.horizontalLayout_5.addWidget(self.labelReject)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lineEditReject = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditReject.setObjectName(_fromUtf8("lineEditReject"))
        self.horizontalLayout_5.addWidget(self.lineEditReject)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBoxMeg = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxMeg.setObjectName(_fromUtf8("checkBoxMeg"))
        self.horizontalLayout_6.addWidget(self.checkBoxMeg)
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
        self.labelReject.setText(_translate("ParameterDialog", "Reject:      ", None))
        self.checkBoxMeg.setText(_translate("ParameterDialog", "meg", None))
        self.checkBoxEeg.setText(_translate("ParameterDialog", "eeg", None))
        self.checkBoxStim.setText(_translate("ParameterDialog", "stim", None))
        self.checkBoxEog.setText(_translate("ParameterDialog", "eog", None))

