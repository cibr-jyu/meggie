# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './meggie/meggie/actions/evoked_plot_topomap/dialogs/evokedTopomapDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_evokedTopomapDialog(object):
    def setupUi(self, evokedTopomapDialog):
        evokedTopomapDialog.setObjectName("evokedTopomapDialog")
        evokedTopomapDialog.resize(406, 540)
        self.gridLayout = QtWidgets.QGridLayout(evokedTopomapDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(evokedTopomapDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 386, 489))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxSettings = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxSettings.setObjectName("groupBoxSettings")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxSettings)
        self.formLayout.setObjectName("formLayout")
        self.labelStart = QtWidgets.QLabel(self.groupBoxSettings)
        self.labelStart.setObjectName("labelStart")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelStart)
        self.doubleSpinBoxStart = QtWidgets.QDoubleSpinBox(self.groupBoxSettings)
        self.doubleSpinBoxStart.setMinimum(-99.0)
        self.doubleSpinBoxStart.setSingleStep(0.05)
        self.doubleSpinBoxStart.setProperty("value", -0.2)
        self.doubleSpinBoxStart.setObjectName("doubleSpinBoxStart")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxStart)
        self.labelEnd = QtWidgets.QLabel(self.groupBoxSettings)
        self.labelEnd.setObjectName("labelEnd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelEnd)
        self.doubleSpinBoxEnd = QtWidgets.QDoubleSpinBox(self.groupBoxSettings)
        self.doubleSpinBoxEnd.setMinimum(-99.0)
        self.doubleSpinBoxEnd.setSingleStep(0.05)
        self.doubleSpinBoxEnd.setProperty("value", 0.5)
        self.doubleSpinBoxEnd.setObjectName("doubleSpinBoxEnd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxEnd)
        self.labelStep = QtWidgets.QLabel(self.groupBoxSettings)
        self.labelStep.setObjectName("labelStep")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelStep)
        self.doubleSpinBoxStep = QtWidgets.QDoubleSpinBox(self.groupBoxSettings)
        self.doubleSpinBoxStep.setMaximum(1.0)
        self.doubleSpinBoxStep.setSingleStep(0.05)
        self.doubleSpinBoxStep.setProperty("value", 0.1)
        self.doubleSpinBoxStep.setObjectName("doubleSpinBoxStep")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxStep)
        self.checkBoxRadius = QtWidgets.QCheckBox(self.groupBoxSettings)
        self.checkBoxRadius.setObjectName("checkBoxRadius")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.checkBoxRadius)
        self.doubleSpinBoxRadius = QtWidgets.QDoubleSpinBox(self.groupBoxSettings)
        self.doubleSpinBoxRadius.setEnabled(False)
        self.doubleSpinBoxRadius.setDecimals(3)
        self.doubleSpinBoxRadius.setMaximum(10.0)
        self.doubleSpinBoxRadius.setSingleStep(0.01)
        self.doubleSpinBoxRadius.setProperty("value", 0.15)
        self.doubleSpinBoxRadius.setObjectName("doubleSpinBoxRadius")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxRadius)
        self.gridLayout_2.addWidget(self.groupBoxSettings, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(evokedTopomapDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(evokedTopomapDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(evokedTopomapDialog)
        self.pushButtonCancel.clicked.connect(evokedTopomapDialog.reject) # type: ignore
        self.pushButtonApply.clicked.connect(evokedTopomapDialog.accept) # type: ignore
        self.checkBoxRadius.toggled['bool'].connect(self.doubleSpinBoxRadius.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(evokedTopomapDialog)

    def retranslateUi(self, evokedTopomapDialog):
        _translate = QtCore.QCoreApplication.translate
        evokedTopomapDialog.setWindowTitle(_translate("evokedTopomapDialog", "Meggie - Evoked topomaps"))
        self.groupBoxSettings.setTitle(_translate("evokedTopomapDialog", "Settings:"))
        self.labelStart.setText(_translate("evokedTopomapDialog", "Start:"))
        self.doubleSpinBoxStart.setSuffix(_translate("evokedTopomapDialog", "s"))
        self.labelEnd.setText(_translate("evokedTopomapDialog", "End:"))
        self.doubleSpinBoxEnd.setSuffix(_translate("evokedTopomapDialog", "s"))
        self.labelStep.setText(_translate("evokedTopomapDialog", "Step:"))
        self.doubleSpinBoxStep.setSuffix(_translate("evokedTopomapDialog", "s"))
        self.checkBoxRadius.setText(_translate("evokedTopomapDialog", "Radius:"))
        self.pushButtonCancel.setText(_translate("evokedTopomapDialog", "Cancel"))
        self.pushButtonApply.setText(_translate("evokedTopomapDialog", "Apply"))
