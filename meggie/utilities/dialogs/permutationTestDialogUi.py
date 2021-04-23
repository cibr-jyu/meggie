# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'permutationTestDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_permutationTestDialog(object):
    def setupUi(self, permutationTestDialog):
        permutationTestDialog.setObjectName("permutationTestDialog")
        permutationTestDialog.resize(419, 523)
        self.gridLayout = QtWidgets.QGridLayout(permutationTestDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(permutationTestDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 399, 472))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.groupBoxGroups = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxGroups.setObjectName("groupBoxGroups")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxGroups)
        self.formLayout.setObjectName("formLayout")
        self.pushButtonGroups = QtWidgets.QPushButton(self.groupBoxGroups)
        self.pushButtonGroups.setObjectName("pushButtonGroups")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.pushButtonGroups)
        self.listWidgetGroups = QtWidgets.QListWidget(self.groupBoxGroups)
        self.listWidgetGroups.setObjectName("listWidgetGroups")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.listWidgetGroups)
        self.gridLayout_2.addWidget(self.groupBoxGroups, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(permutationTestDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(permutationTestDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(permutationTestDialog)
        self.pushButtonCancel.clicked.connect(permutationTestDialog.reject)
        self.pushButtonApply.clicked.connect(permutationTestDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(permutationTestDialog)

    def retranslateUi(self, permutationTestDialog):
        _translate = QtCore.QCoreApplication.translate
        permutationTestDialog.setWindowTitle(_translate("permutationTestDialog", "Meggie - Permutation tests"))
        self.groupBoxGroups.setTitle(_translate("permutationTestDialog", "Groups"))
        self.pushButtonGroups.setText(_translate("permutationTestDialog", "Select groups.."))
        self.pushButtonCancel.setText(_translate("permutationTestDialog", "Cancel"))
        self.pushButtonApply.setText(_translate("permutationTestDialog", "Apply"))

