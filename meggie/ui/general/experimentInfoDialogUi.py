# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../experimentInfoDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_experimentInfoDialog(object):
    def setupUi(self, experimentInfoDialog):
        experimentInfoDialog.setObjectName("experimentInfoDialog")
        experimentInfoDialog.resize(584, 530)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(experimentInfoDialog.sizePolicy().hasHeightForWidth())
        experimentInfoDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(experimentInfoDialog)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.groupBoxExperimentInfo = QtWidgets.QGroupBox(experimentInfoDialog)
        self.groupBoxExperimentInfo.setObjectName("groupBoxExperimentInfo")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxExperimentInfo)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelExperiment = QtWidgets.QLabel(self.groupBoxExperimentInfo)
        self.labelExperiment.setObjectName("labelExperiment")
        self.gridLayout.addWidget(self.labelExperiment, 0, 0, 1, 1)
        self.lineEditExperimentName = QtWidgets.QLineEdit(self.groupBoxExperimentInfo)
        self.lineEditExperimentName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditExperimentName.setReadOnly(True)
        self.lineEditExperimentName.setObjectName("lineEditExperimentName")
        self.gridLayout.addWidget(self.lineEditExperimentName, 0, 1, 1, 1)
        self.labelAuthor = QtWidgets.QLabel(self.groupBoxExperimentInfo)
        self.labelAuthor.setObjectName("labelAuthor")
        self.gridLayout.addWidget(self.labelAuthor, 1, 0, 1, 1)
        self.lineEditExperimentAuthor = QtWidgets.QLineEdit(self.groupBoxExperimentInfo)
        self.lineEditExperimentAuthor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditExperimentAuthor.setReadOnly(True)
        self.lineEditExperimentAuthor.setObjectName("lineEditExperimentAuthor")
        self.gridLayout.addWidget(self.lineEditExperimentAuthor, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(self.groupBoxExperimentInfo)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.labelDescription = QtWidgets.QLabel(self.groupBoxExperimentInfo)
        self.labelDescription.setObjectName("labelDescription")
        self.gridLayout_2.addWidget(self.labelDescription, 2, 0, 1, 1)
        self.textBrowserExperimentDescription = QtWidgets.QTextBrowser(self.groupBoxExperimentInfo)
        self.textBrowserExperimentDescription.setObjectName("textBrowserExperimentDescription")
        self.gridLayout_2.addWidget(self.textBrowserExperimentDescription, 3, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBoxExperimentInfo)
        self.ButtonClose = QtWidgets.QPushButton(experimentInfoDialog)
        self.ButtonClose.setObjectName("ButtonClose")
        self.verticalLayout_6.addWidget(self.ButtonClose)

        self.retranslateUi(experimentInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(experimentInfoDialog)

    def retranslateUi(self, experimentInfoDialog):
        _translate = QtCore.QCoreApplication.translate
        experimentInfoDialog.setWindowTitle(_translate("experimentInfoDialog", "Experiment info"))
        self.groupBoxExperimentInfo.setTitle(_translate("experimentInfoDialog", "Experiment info"))
        self.labelExperiment.setText(_translate("experimentInfoDialog", "Name:"))
        self.labelAuthor.setText(_translate("experimentInfoDialog", "Author:"))
        self.labelDescription.setText(_translate("experimentInfoDialog", "Description:"))
        self.ButtonClose.setText(_translate("experimentInfoDialog", "Close"))

