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
        groupAverageDialog.resize(359, 464)
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
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 350, 1000))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(350, 1000))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout_2 = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout_2.setObjectName("formLayout_2")
        self.groupBoxAverageGroups = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxAverageGroups.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBoxAverageGroups.setObjectName("groupBoxAverageGroups")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxAverageGroups)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.groupBoxAverageGroups)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
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
        self.pushButtonCancel.setText(_translate("groupAverageDialog", "Cancel"))
        self.pushButtonCompute.setText(_translate("groupAverageDialog", "Accept"))

