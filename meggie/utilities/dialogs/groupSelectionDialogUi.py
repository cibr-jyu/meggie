# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'groupSelectionDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_groupSelectionDialog(object):
    def setupUi(self, groupSelectionDialog):
        groupSelectionDialog.setObjectName("groupSelectionDialog")
        groupSelectionDialog.resize(402, 605)
        self.verticalLayout = QtWidgets.QVBoxLayout(groupSelectionDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(groupSelectionDialog)
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
        self.groupBoxGroups = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxGroups.setMinimumSize(QtCore.QSize(350, 0))
        self.groupBoxGroups.setObjectName("groupBoxGroups")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxGroups)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addWidget(self.groupBoxGroups, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(groupSelectionDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonCompute = QtWidgets.QPushButton(groupSelectionDialog)
        self.pushButtonCompute.setObjectName("pushButtonCompute")
        self.horizontalLayout.addWidget(self.pushButtonCompute)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(groupSelectionDialog)
        self.pushButtonCancel.clicked.connect(groupSelectionDialog.reject)
        self.pushButtonCompute.clicked.connect(groupSelectionDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(groupSelectionDialog)

    def retranslateUi(self, groupSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        groupSelectionDialog.setWindowTitle(_translate("groupSelectionDialog", "Meggie - Group selection"))
        self.groupBoxGroups.setTitle(_translate("groupSelectionDialog", "Groups:"))
        self.pushButtonCancel.setText(_translate("groupSelectionDialog", "Cancel"))
        self.pushButtonCompute.setText(_translate("groupSelectionDialog", "Accept"))
