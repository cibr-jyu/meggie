# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batchingWidgetUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_BatchingWidget(object):
    def setupUi(self, BatchingWidget):
        BatchingWidget.setObjectName("BatchingWidget")
        BatchingWidget.resize(291, 276)
        self.layoutWidget = QtWidgets.QWidget(BatchingWidget)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 289, 31))
        self.layoutWidget.setObjectName("layoutWidget")
        self.headingLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.headingLayout.setContentsMargins(0, 0, 0, 0)
        self.headingLayout.setObjectName("headingLayout")
        self.checkBoxBatch = QtWidgets.QCheckBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.checkBoxBatch.sizePolicy().hasHeightForWidth()
        )
        self.checkBoxBatch.setSizePolicy(sizePolicy)
        self.checkBoxBatch.setObjectName("checkBoxBatch")
        self.headingLayout.addWidget(self.checkBoxBatch)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.headingLayout.addItem(spacerItem)
        self.functionalityWidget = QtWidgets.QWidget(BatchingWidget)
        self.functionalityWidget.setGeometry(QtCore.QRect(0, 30, 289, 241))
        self.functionalityWidget.setObjectName("functionalityWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.functionalityWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.functionalityLayout = QtWidgets.QGridLayout()
        self.functionalityLayout.setObjectName("functionalityLayout")
        self.applyButtonsLayout = QtWidgets.QVBoxLayout()
        self.applyButtonsLayout.setObjectName("applyButtonsLayout")
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.pushButtonApplyAll = QtWidgets.QPushButton(self.functionalityWidget)
        self.pushButtonApplyAll.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButtonApplyAll.sizePolicy().hasHeightForWidth()
        )
        self.pushButtonApplyAll.setSizePolicy(sizePolicy)
        self.pushButtonApplyAll.setMinimumSize(QtCore.QSize(90, 0))
        self.pushButtonApplyAll.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonApplyAll.setObjectName("pushButtonApplyAll")
        self.horizontalLayout_31.addWidget(self.pushButtonApplyAll)
        self.label_7 = QtWidgets.QLabel(self.functionalityWidget)
        self.label_7.setEnabled(True)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_31.addWidget(self.label_7)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_31.addItem(spacerItem1)
        self.applyButtonsLayout.addLayout(self.horizontalLayout_31)
        self.functionalityLayout.addLayout(self.applyButtonsLayout, 1, 0, 1, 1)
        self.subjectListLayout = QtWidgets.QVBoxLayout()
        self.subjectListLayout.setObjectName("subjectListLayout")
        self.labelSubjects = QtWidgets.QLabel(self.functionalityWidget)
        self.labelSubjects.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.labelSubjects.sizePolicy().hasHeightForWidth()
        )
        self.labelSubjects.setSizePolicy(sizePolicy)
        self.labelSubjects.setObjectName("labelSubjects")
        self.subjectListLayout.addWidget(self.labelSubjects)
        self.listWidgetSubjects = QtWidgets.QListWidget(self.functionalityWidget)
        self.listWidgetSubjects.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listWidgetSubjects.sizePolicy().hasHeightForWidth()
        )
        self.listWidgetSubjects.setSizePolicy(sizePolicy)
        self.listWidgetSubjects.setObjectName("listWidgetSubjects")
        self.subjectListLayout.addWidget(self.listWidgetSubjects)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.subjectListLayout.addLayout(self.horizontalLayout_17)
        self.functionalityLayout.addLayout(self.subjectListLayout, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.functionalityLayout)

        self.retranslateUi(BatchingWidget)
        self.checkBoxBatch.toggled["bool"].connect(BatchingWidget.showWidget)
        QtCore.QMetaObject.connectSlotsByName(BatchingWidget)

    def retranslateUi(self, BatchingWidget):
        _translate = QtCore.QCoreApplication.translate
        BatchingWidget.setWindowTitle(
            _translate("BatchingWidget", "Meggie - Batch processing")
        )
        self.checkBoxBatch.setText(_translate("BatchingWidget", "Batch processing"))
        self.pushButtonApplyAll.setText(_translate("BatchingWidget", "Select all"))
        self.label_7.setText(_translate("BatchingWidget", "subjects on the list"))
        self.labelSubjects.setText(
            _translate("BatchingWidget", "Select subjects to include in batch")
        )
