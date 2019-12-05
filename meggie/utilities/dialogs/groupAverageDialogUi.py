# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupAverageDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_groupAverageDialog(object):
    def setupUi(self, groupAverageDialog):
        groupAverageDialog.setObjectName("groupAverageDialog")
        groupAverageDialog.resize(402, 605)
        self.verticalLayout = QtWidgets.QVBoxLayout(groupAverageDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(groupAverageDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 382, 554))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxAverageGroups = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxAverageGroups.setMinimumSize(QtCore.QSize(350, 0))
        self.groupBoxAverageGroups.setObjectName("groupBoxAverageGroups")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxAverageGroups)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addWidget(self.groupBoxAverageGroups, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.groupBoxGeneral = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxGeneral.setObjectName("groupBoxGeneral")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxGeneral)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelName = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelName.setObjectName("labelName")
        self.gridLayout_3.addWidget(self.labelName, 0, 0, 1, 1)
        self.lineEditName = QtWidgets.QLineEdit(self.groupBoxGeneral)
        self.lineEditName.setObjectName("lineEditName")
        self.gridLayout_3.addWidget(self.lineEditName, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxGeneral, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(groupAverageDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonCompute = QtWidgets.QPushButton(groupAverageDialog)
        self.pushButtonCompute.setObjectName("pushButtonCompute")
        self.horizontalLayout.addWidget(self.pushButtonCompute)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(groupAverageDialog)
        self.pushButtonCancel.clicked.connect(groupAverageDialog.reject)
        self.pushButtonCompute.clicked.connect(groupAverageDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(groupAverageDialog)

    def retranslateUi(self, groupAverageDialog):
        _translate = QtCore.QCoreApplication.translate
        groupAverageDialog.setWindowTitle(_translate("groupAverageDialog", "Group average"))
        self.groupBoxAverageGroups.setTitle(_translate("groupAverageDialog", "Average groups:"))
        self.groupBoxGeneral.setTitle(_translate("groupAverageDialog", "General"))
        self.labelName.setText(_translate("groupAverageDialog", "Name:"))
        self.pushButtonCancel.setText(_translate("groupAverageDialog", "Cancel"))
        self.pushButtonCompute.setText(_translate("groupAverageDialog", "Accept"))

