# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/preferencesDialog.ui'
#
# Created: Mon Aug 25 16:55:42 2014
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
        DialogPreferences.resize(537, 385)
        self.verticalLayout_3 = QtGui.QVBoxLayout(DialogPreferences)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.scrollArea = QtGui.QScrollArea(DialogPreferences)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 519, 334))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(394, 92))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.formLayout_2 = QtGui.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.groupBoxWorkingDirectory = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxWorkingDirectory.setObjectName(_fromUtf8("groupBoxWorkingDirectory"))
        self.formLayout = QtGui.QFormLayout(self.groupBoxWorkingDirectory)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
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
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.verticalLayout_2)
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.groupBoxWorkingDirectory)
        self.groupBoxEnv = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxEnv.setObjectName(_fromUtf8("groupBoxEnv"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBoxEnv)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
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
        self.formLayout_3.setLayout(0, QtGui.QFormLayout.LabelRole, self.verticalLayout_4)
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.groupBoxEnv)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.buttonBox = QtGui.QDialogButtonBox(DialogPreferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_3.addWidget(self.buttonBox)

        self.retranslateUi(DialogPreferences)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogPreferences.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogPreferences.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogPreferences)
        DialogPreferences.setTabOrder(self.scrollArea, self.LineEditFilePath)
        DialogPreferences.setTabOrder(self.LineEditFilePath, self.ButtonBrowseWorkingDir)
        DialogPreferences.setTabOrder(self.ButtonBrowseWorkingDir, self.buttonBox)

    def retranslateUi(self, DialogPreferences):
        DialogPreferences.setWindowTitle(_translate("DialogPreferences", "Preferences", None))
        self.groupBoxWorkingDirectory.setTitle(_translate("DialogPreferences", "Working directory:", None))
        self.label.setText(_translate("DialogPreferences", "Select a working directory (compulsory):", None))
        self.ButtonBrowseWorkingDir.setText(_translate("DialogPreferences", "Browse...", None))
        self.groupBoxEnv.setTitle(_translate("DialogPreferences", "Environment variables:", None))
        self.labelMNERoot.setText(_translate("DialogPreferences", "Select MNEROOT directory (needed for source analysis):", None))
        self.pushButtonBrowseMNERoot.setText(_translate("DialogPreferences", "Browse...", None))

