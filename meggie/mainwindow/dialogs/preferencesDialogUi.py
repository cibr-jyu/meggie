# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferencesDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogPreferences(object):
    def setupUi(self, DialogPreferences):
        DialogPreferences.setObjectName("DialogPreferences")
        DialogPreferences.resize(507, 482)
        self.gridLayout_3 = QtWidgets.QGridLayout(DialogPreferences)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(DialogPreferences)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(DialogPreferences)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout_2.addWidget(self.pushButtonAccept)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(DialogPreferences)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 487, 431))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBoxMisc = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxMisc.setObjectName("groupBoxMisc")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxMisc)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.checkBoxAutomaticOpenPreviousExperiment = QtWidgets.QCheckBox(self.groupBoxMisc)
        self.checkBoxAutomaticOpenPreviousExperiment.setObjectName("checkBoxAutomaticOpenPreviousExperiment")
        self.gridLayout_4.addWidget(self.checkBoxAutomaticOpenPreviousExperiment, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBoxMisc, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_5.addItem(spacerItem1, 3, 0, 1, 1)
        self.groupBoxWorkspace = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxWorkspace.setObjectName("groupBoxWorkspace")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxWorkspace)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.LineEditFilePath = QtWidgets.QLineEdit(self.groupBoxWorkspace)
        self.LineEditFilePath.setObjectName("LineEditFilePath")
        self.gridLayout_2.addWidget(self.LineEditFilePath, 0, 0, 1, 1)
        self.ButtonBrowseWorkingDir = QtWidgets.QPushButton(self.groupBoxWorkspace)
        self.ButtonBrowseWorkingDir.setObjectName("ButtonBrowseWorkingDir")
        self.gridLayout_2.addWidget(self.ButtonBrowseWorkingDir, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBoxWorkspace, 0, 0, 1, 1)
        self.groupBoxPlugins = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxPlugins.setObjectName("groupBoxPlugins")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxPlugins)
        self.formLayout.setObjectName("formLayout")
        self.pushButtonPlugins = QtWidgets.QPushButton(self.groupBoxPlugins)
        self.pushButtonPlugins.setObjectName("pushButtonPlugins")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.pushButtonPlugins)
        self.gridLayout_5.addWidget(self.groupBoxPlugins, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(DialogPreferences)
        self.pushButtonCancel.clicked.connect(DialogPreferences.reject)
        self.pushButtonAccept.clicked.connect(DialogPreferences.accept)
        QtCore.QMetaObject.connectSlotsByName(DialogPreferences)

    def retranslateUi(self, DialogPreferences):
        _translate = QtCore.QCoreApplication.translate
        DialogPreferences.setWindowTitle(_translate("DialogPreferences", "Meggie - Preferences"))
        self.pushButtonCancel.setText(_translate("DialogPreferences", "Cancel"))
        self.pushButtonAccept.setText(_translate("DialogPreferences", "Ok"))
        self.groupBoxMisc.setTitle(_translate("DialogPreferences", "Miscellaneous:"))
        self.checkBoxAutomaticOpenPreviousExperiment.setText(_translate("DialogPreferences", "Automatically open previous experiment upon application startup"))
        self.groupBoxWorkspace.setTitle(_translate("DialogPreferences", "Workspace:"))
        self.ButtonBrowseWorkingDir.setText(_translate("DialogPreferences", "Browse..."))
        self.groupBoxPlugins.setTitle(_translate("DialogPreferences", "Plugins:"))
        self.pushButtonPlugins.setText(_translate("DialogPreferences", "Select active plugins..."))
