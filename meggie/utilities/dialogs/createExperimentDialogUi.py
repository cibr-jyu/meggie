# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../createExperimentDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateExperimentDialog(object):
    def setupUi(self, CreateExperimentDialog):
        CreateExperimentDialog.setObjectName("CreateExperimentDialog")
        CreateExperimentDialog.setWindowModality(QtCore.Qt.WindowModal)
        CreateExperimentDialog.resize(683, 604)
        self.gridLayout_3 = QtWidgets.QGridLayout(CreateExperimentDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(CreateExperimentDialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 665, 549))
        self.scrollAreaWidgetContents_2.setMinimumSize(QtCore.QSize(645, 540))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.layoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 2, 641, 522))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEditDescription = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEditDescription.setObjectName("textEditDescription")
        self.gridLayout_2.addWidget(self.textEditDescription, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelAuthor = QtWidgets.QLabel(self.groupBox_2)
        self.labelAuthor.setObjectName("labelAuthor")
        self.horizontalLayout.addWidget(self.labelAuthor)
        self.lineEditAuthor = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditAuthor.setObjectName("lineEditAuthor")
        self.horizontalLayout.addWidget(self.lineEditAuthor)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelExperimentName = QtWidgets.QLabel(self.groupBox_2)
        self.labelExperimentName.setObjectName("labelExperimentName")
        self.horizontalLayout_2.addWidget(self.labelExperimentName)
        self.lineEditExperimentName = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEditExperimentName.setObjectName("lineEditExperimentName")
        self.horizontalLayout_2.addWidget(self.lineEditExperimentName)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.labelDescription = QtWidgets.QLabel(self.groupBox_2)
        self.labelDescription.setObjectName("labelDescription")
        self.gridLayout_2.addWidget(self.labelDescription, 2, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
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
        CreateExperimentDialog.setTabOrder(self.scrollArea, self.lineEditExperimentName)
        CreateExperimentDialog.setTabOrder(self.lineEditExperimentName, self.lineEditAuthor)
        CreateExperimentDialog.setTabOrder(self.lineEditAuthor, self.textEditDescription)
        CreateExperimentDialog.setTabOrder(self.textEditDescription, self.cancelOkButtonBox)

    def retranslateUi(self, CreateExperimentDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateExperimentDialog.setWindowTitle(_translate("CreateExperimentDialog", "Meggie - Create new experiment"))
        self.groupBox_2.setTitle(_translate("CreateExperimentDialog", "Experiment information"))
        self.labelAuthor.setText(_translate("CreateExperimentDialog", "Experiment author:"))
        self.labelExperimentName.setText(_translate("CreateExperimentDialog", "Experiment name:"))
        self.labelDescription.setText(_translate("CreateExperimentDialog", "Experiment description:"))

