# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameterDialog.ui'
#
# Created: Tue Mar 19 14:49:13 2013
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
        ParameterDialog.resize(391, 322)
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(ParameterDialog)
        self.cancelOkButtonBox.setGeometry(QtCore.QRect(20, 270, 176, 31))
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.widget = QtGui.QWidget(ParameterDialog)
        self.widget.setGeometry(QtCore.QRect(21, 11, 351, 62))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelEventFile = QtGui.QLabel(self.widget)
        self.labelEventFile.setObjectName(_fromUtf8("labelEventFile"))
        self.verticalLayout.addWidget(self.labelEventFile)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.FilePathLineEdit = QtGui.QLineEdit(self.widget)
        self.FilePathLineEdit.setObjectName(_fromUtf8("FilePathLineEdit"))
        self.horizontalLayout_3.addWidget(self.FilePathLineEdit)
        self.browseButton = QtGui.QPushButton(self.widget)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.horizontalLayout_3.addWidget(self.browseButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.widget1 = QtGui.QWidget(ParameterDialog)
        self.widget1.setGeometry(QtCore.QRect(20, 80, 351, 188))
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelEventID = QtGui.QLabel(self.widget1)
        self.labelEventID.setObjectName(_fromUtf8("labelEventID"))
        self.horizontalLayout_2.addWidget(self.labelEventID)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.lineEditEventID = QtGui.QLineEdit(self.widget1)
        self.lineEditEventID.setObjectName(_fromUtf8("lineEditEventID"))
        self.horizontalLayout_2.addWidget(self.lineEditEventID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.widget1)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.lineEditTmin = QtGui.QLineEdit(self.widget1)
        self.lineEditTmin.setObjectName(_fromUtf8("lineEditTmin"))
        self.horizontalLayout.addWidget(self.lineEditTmin)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelTmax = QtGui.QLabel(self.widget1)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout_4.addWidget(self.labelTmax)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.lineEditTmax = QtGui.QLineEdit(self.widget1)
        self.lineEditTmax.setObjectName(_fromUtf8("lineEditTmax"))
        self.horizontalLayout_4.addWidget(self.lineEditTmax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelReject = QtGui.QLabel(self.widget1)
        self.labelReject.setObjectName(_fromUtf8("labelReject"))
        self.horizontalLayout_5.addWidget(self.labelReject)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.lineEditReject = QtGui.QLineEdit(self.widget1)
        self.lineEditReject.setObjectName(_fromUtf8("lineEditReject"))
        self.horizontalLayout_5.addWidget(self.lineEditReject)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBoxMeg = QtGui.QCheckBox(self.widget1)
        self.checkBoxMeg.setObjectName(_fromUtf8("checkBoxMeg"))
        self.horizontalLayout_6.addWidget(self.checkBoxMeg)
        self.checkBoxEeg = QtGui.QCheckBox(self.widget1)
        self.checkBoxEeg.setObjectName(_fromUtf8("checkBoxEeg"))
        self.horizontalLayout_6.addWidget(self.checkBoxEeg)
        self.checkBoxStim = QtGui.QCheckBox(self.widget1)
        self.checkBoxStim.setObjectName(_fromUtf8("checkBoxStim"))
        self.horizontalLayout_6.addWidget(self.checkBoxStim)
        self.checkBox_4 = QtGui.QCheckBox(self.widget1)
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.horizontalLayout_6.addWidget(self.checkBox_4)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.retranslateUi(ParameterDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ParameterDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ParameterDialog.reject)
        #QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), ParameterDialog.openFileChooserDialog)
        QtCore.QMetaObject.connectSlotsByName(ParameterDialog)

    def retranslateUi(self, ParameterDialog):
        ParameterDialog.setWindowTitle(_translate("ParameterDialog", "Give parameters", None))
        self.labelEventFile.setText(_translate("ParameterDialog", "Event file:", None))
        self.browseButton.setText(_translate("ParameterDialog", "Browse...", None))
        self.labelEventID.setText(_translate("ParameterDialog", "Project name:", None))
        self.labelTmin.setText(_translate("ParameterDialog", "Start time:", None))
        self.labelTmax.setText(_translate("ParameterDialog", "End time:", None))
        self.labelReject.setText(_translate("ParameterDialog", "Reject:      ", None))
        self.checkBoxMeg.setText(_translate("ParameterDialog", "meg", None))
        self.checkBoxEeg.setText(_translate("ParameterDialog", "eeg", None))
        self.checkBoxStim.setText(_translate("ParameterDialog", "stim", None))
        self.checkBox_4.setText(_translate("ParameterDialog", "eog", None))

