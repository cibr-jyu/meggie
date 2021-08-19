# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createExperimentDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CreateExperimentDialog(object):
    def setupUi(self, CreateExperimentDialog):
        CreateExperimentDialog.setObjectName("CreateExperimentDialog")
        CreateExperimentDialog.setWindowModality(QtCore.Qt.WindowModal)
        CreateExperimentDialog.resize(506, 373)
        self.gridLayout_3 = QtWidgets.QGridLayout(CreateExperimentDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(CreateExperimentDialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 488, 324))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.groupBoxInfo = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxInfo.setObjectName("groupBoxInfo")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxInfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelExperimentName = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelExperimentName.setObjectName("labelExperimentName")
        self.gridLayout_2.addWidget(self.labelExperimentName, 0, 0, 1, 1)
        self.lineEditExperimentName = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditExperimentName.setObjectName("lineEditExperimentName")
        self.gridLayout_2.addWidget(self.lineEditExperimentName, 0, 1, 1, 1)
        self.lineEditAuthor = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditAuthor.setObjectName("lineEditAuthor")
        self.gridLayout_2.addWidget(self.lineEditAuthor, 1, 1, 1, 1)
        self.labelAuthor = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelAuthor.setObjectName("labelAuthor")
        self.gridLayout_2.addWidget(self.labelAuthor, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxInfo, 0, 1, 1, 1)
        self.groupBoxPipeline = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxPipeline.setObjectName("groupBoxPipeline")
        self.gridLayoutPipeline = QtWidgets.QGridLayout(self.groupBoxPipeline)
        self.gridLayoutPipeline.setObjectName("gridLayoutPipeline")
        self.gridLayout.addWidget(self.groupBoxPipeline, 1, 1, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutButtons.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(CreateExperimentDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(CreateExperimentDialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayoutButtons.addWidget(self.pushButtonAccept)
        self.gridLayout_3.addLayout(self.horizontalLayoutButtons, 2, 0, 1, 1)

        self.retranslateUi(CreateExperimentDialog)
        self.pushButtonAccept.clicked.connect(CreateExperimentDialog.accept)
        self.pushButtonCancel.clicked.connect(CreateExperimentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateExperimentDialog)

    def retranslateUi(self, CreateExperimentDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateExperimentDialog.setWindowTitle(_translate("CreateExperimentDialog", "Meggie - Create new experiment"))
        self.groupBoxInfo.setTitle(_translate("CreateExperimentDialog", "Experiment information"))
        self.labelExperimentName.setText(_translate("CreateExperimentDialog", "Experiment name:"))
        self.labelAuthor.setText(_translate("CreateExperimentDialog", "Experiment author:"))
        self.groupBoxPipeline.setTitle(_translate("CreateExperimentDialog", "Select a pipeline for the analysis:"))
        self.pushButtonCancel.setText(_translate("CreateExperimentDialog", "Cancel"))
        self.pushButtonAccept.setText(_translate("CreateExperimentDialog", "Ok"))
