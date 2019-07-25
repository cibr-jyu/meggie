# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createExperimentDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateExperimentDialog(object):
    def setupUi(self, CreateExperimentDialog):
        CreateExperimentDialog.setObjectName("CreateExperimentDialog")
        CreateExperimentDialog.setWindowModality(QtCore.Qt.WindowModal)
        CreateExperimentDialog.resize(683, 272)
        self.gridLayout_3 = QtWidgets.QGridLayout(CreateExperimentDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(CreateExperimentDialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 665, 224))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxInfo = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxInfo.setObjectName("groupBoxInfo")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxInfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelExperimentName = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelExperimentName.setObjectName("labelExperimentName")
        self.gridLayout_2.addWidget(self.labelExperimentName, 0, 0, 1, 1)
        self.labelDescription = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelDescription.setObjectName("labelDescription")
        self.gridLayout_2.addWidget(self.labelDescription, 2, 0, 1, 1)
        self.lineEditExperimentName = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditExperimentName.setObjectName("lineEditExperimentName")
        self.gridLayout_2.addWidget(self.lineEditExperimentName, 0, 1, 1, 1)
        self.lineEditAuthor = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditAuthor.setObjectName("lineEditAuthor")
        self.gridLayout_2.addWidget(self.lineEditAuthor, 1, 1, 1, 1)
        self.labelAuthor = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelAuthor.setObjectName("labelAuthor")
        self.gridLayout_2.addWidget(self.labelAuthor, 1, 0, 1, 1)
        self.textEditDescription = QtWidgets.QTextEdit(self.groupBoxInfo)
        self.textEditDescription.setMinimumSize(QtCore.QSize(0, 100))
        self.textEditDescription.setObjectName("textEditDescription")
        self.gridLayout_2.addWidget(self.textEditDescription, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBoxInfo, 0, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.cancelOkButtonBox = QtWidgets.QDialogButtonBox(CreateExperimentDialog)
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName("cancelOkButtonBox")
        self.gridLayout_3.addWidget(self.cancelOkButtonBox, 1, 0, 1, 1)

        self.retranslateUi(CreateExperimentDialog)
        self.cancelOkButtonBox.accepted.connect(CreateExperimentDialog.accept)
        self.cancelOkButtonBox.rejected.connect(CreateExperimentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateExperimentDialog)
        CreateExperimentDialog.setTabOrder(self.scrollArea, self.cancelOkButtonBox)

    def retranslateUi(self, CreateExperimentDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateExperimentDialog.setWindowTitle(_translate("CreateExperimentDialog", "Meggie - Create new experiment"))
        self.groupBoxInfo.setTitle(_translate("CreateExperimentDialog", "Experiment information"))
        self.labelExperimentName.setText(_translate("CreateExperimentDialog", "Experiment name:"))
        self.labelDescription.setText(_translate("CreateExperimentDialog", "Experiment description:"))
        self.labelAuthor.setText(_translate("CreateExperimentDialog", "Experiment author:"))

