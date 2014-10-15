# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/preferencesDialog.ui'
#
# Created: Wed Oct 15 18:43:20 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_DialogPreferences(object):
    def setupUi(self, DialogPreferences):
        DialogPreferences.setObjectName(_fromUtf8("DialogPreferences"))
        DialogPreferences.resize(493, 404)
        self.gridLayout_3 = QtGui.QGridLayout(DialogPreferences)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBoxWorkingDirectory = QtGui.QGroupBox(DialogPreferences)
        self.groupBoxWorkingDirectory.setObjectName(_fromUtf8("groupBoxWorkingDirectory"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxWorkingDirectory)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.groupBoxWorkingDirectory)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.LineEditFilePath = QtGui.QLineEdit(self.groupBoxWorkingDirectory)
        self.LineEditFilePath.setObjectName(_fromUtf8("LineEditFilePath"))
        self.horizontalLayout.addWidget(self.LineEditFilePath)
        self.ButtonBrowseWorkingDir = QtGui.QPushButton(self.groupBoxWorkingDirectory)
        self.ButtonBrowseWorkingDir.setObjectName(_fromUtf8("ButtonBrowseWorkingDir"))
        self.horizontalLayout.addWidget(self.ButtonBrowseWorkingDir)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxWorkingDirectory, 0, 0, 1, 1)
        self.groupBoxEnv = QtGui.QGroupBox(DialogPreferences)
        self.groupBoxEnv.setObjectName(_fromUtf8("groupBoxEnv"))
        self.gridLayout = QtGui.QGridLayout(self.groupBoxEnv)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.labelMNERoot = QtGui.QLabel(self.groupBoxEnv)
        self.labelMNERoot.setObjectName(_fromUtf8("labelMNERoot"))
        self.verticalLayout_4.addWidget(self.labelMNERoot)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEditMNERoot = QtGui.QLineEdit(self.groupBoxEnv)
        self.lineEditMNERoot.setObjectName(_fromUtf8("lineEditMNERoot"))
        self.horizontalLayout_2.addWidget(self.lineEditMNERoot)
        self.pushButtonBrowseMNERoot = QtGui.QPushButton(self.groupBoxEnv)
        self.pushButtonBrowseMNERoot.setObjectName(_fromUtf8("pushButtonBrowseMNERoot"))
        self.horizontalLayout_2.addWidget(self.pushButtonBrowseMNERoot)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.labelFreeSurferHome = QtGui.QLabel(self.groupBoxEnv)
        self.labelFreeSurferHome.setObjectName(_fromUtf8("labelFreeSurferHome"))
        self.verticalLayout_6.addWidget(self.labelFreeSurferHome)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.lineEditFreeSurferHome = QtGui.QLineEdit(self.groupBoxEnv)
        self.lineEditFreeSurferHome.setObjectName(_fromUtf8("lineEditFreeSurferHome"))
        self.horizontalLayout_4.addWidget(self.lineEditFreeSurferHome)
        self.pushButtonBrowseFreeSurferHome = QtGui.QPushButton(self.groupBoxEnv)
        self.pushButtonBrowseFreeSurferHome.setObjectName(_fromUtf8("pushButtonBrowseFreeSurferHome"))
        self.horizontalLayout_4.addWidget(self.pushButtonBrowseFreeSurferHome)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_6, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBoxEnv, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(DialogPreferences)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.checkBoxAutomaticOpenPreviousExperiment = QtGui.QCheckBox(self.groupBox)
        self.checkBoxAutomaticOpenPreviousExperiment.setObjectName(_fromUtf8("checkBoxAutomaticOpenPreviousExperiment"))
        self.gridLayout_4.addWidget(self.checkBoxAutomaticOpenPreviousExperiment, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 2, 0, 1, 1)
        self.checkBoxConfirmQuit = QtGui.QCheckBox(self.groupBox)
        self.checkBoxConfirmQuit.setObjectName(_fromUtf8("checkBoxConfirmQuit"))
        self.gridLayout_4.addWidget(self.checkBoxConfirmQuit, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(DialogPreferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(DialogPreferences)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogPreferences.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogPreferences.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogPreferences)
        DialogPreferences.setTabOrder(self.LineEditFilePath, self.ButtonBrowseWorkingDir)

    def retranslateUi(self, DialogPreferences):
        DialogPreferences.setWindowTitle(_translate("DialogPreferences", "Preferences", None))
        self.groupBoxWorkingDirectory.setTitle(_translate("DialogPreferences", "Working directory:", None))
        self.label.setText(_translate("DialogPreferences", "Select a working directory (compulsory):", None))
        self.ButtonBrowseWorkingDir.setText(_translate("DialogPreferences", "Browse...", None))
        self.groupBoxEnv.setTitle(_translate("DialogPreferences", "Environment variables:", None))
        self.labelMNERoot.setText(_translate("DialogPreferences", "Select MNEROOT directory (needed for source analysis):", None))
        self.pushButtonBrowseMNERoot.setText(_translate("DialogPreferences", "Browse...", None))
        self.labelFreeSurferHome.setText(_translate("DialogPreferences", "Select FREESURFER_HOME directory (needed for source analysis):", None))
        self.pushButtonBrowseFreeSurferHome.setText(_translate("DialogPreferences", "Browse...", None))
        self.groupBox.setTitle(_translate("DialogPreferences", "Miscellaneous preferences:", None))
        self.checkBoxAutomaticOpenPreviousExperiment.setText(_translate("DialogPreferences", "Automatically open previous experiment upon application startup", None))
        self.checkBoxConfirmQuit.setText(_translate("DialogPreferences", "Show confirmation dialog on Meggie quit", None))

