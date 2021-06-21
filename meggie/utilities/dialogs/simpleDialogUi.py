""" UI layout for simple dialog
"""
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

class Ui_SimpleDialog(object):
    """ Contains layout of very simple reusable dialog
    """
    def setupUi(self, dialog):
        dialog.setObjectName("CreateEvokedDialog")
        dialog.resize(364, 530)

        self.gridLayout = QtWidgets.QGridLayout(dialog)
        self.gridLayout.setObjectName("gridLayout")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        self.horizontalLayoutButtons.addItem(spacerItem)

        self.pushButtonCancel = QtWidgets.QPushButton(dialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)

        self.pushButtonBatch = QtWidgets.QPushButton(dialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayoutButtons.addWidget(self.pushButtonBatch)

        self.pushButtonApply = QtWidgets.QPushButton(dialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayoutButtons.addWidget(self.pushButtonApply)

        self.gridLayout.addLayout(self.horizontalLayoutButtons, 2, 0, 1, 1)

        self.scrollArea = QtWidgets.QScrollArea(dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 344, 479))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.gridLayoutScrollArea = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayoutScrollArea.setObjectName("gridLayoutScrollArea")

        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutScrollArea.addWidget(self.groupBoxBatching, 1, 0, 1, 1)

        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setContentsMargins(9, 9, 9, 9)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")

        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)

        self.groupBoxInfo = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxInfo.setObjectName("groupBoxInfo")

        self.formLayout = QtWidgets.QFormLayout(self.groupBoxInfo)
        self.formLayout.setObjectName("formLayout")

        self.labelName = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelName.setObjectName("labelName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelName)

        self.lineEditName = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditName.setObjectName("lineEditName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditName)

        self.gridLayoutScrollArea.addWidget(self.groupBoxInfo, 0, 0, 1, 1)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayoutScrollArea.addItem(spacerItem, 2, 0, 1, 1)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(dialog)

        self.pushButtonCancel.clicked.connect(dialog.close)
        self.pushButtonApply.clicked.connect(dialog.accept)
        self.pushButtonBatch.clicked.connect(dialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("SimpleDialog", "Meggie - Simple dialog"))
        self.pushButtonCancel.setText(_translate("SimpleDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("SimpleDialog", "Batch"))
        self.pushButtonApply.setText(_translate("SimpleDialog", "Apply"))
        self.groupBoxBatching.setTitle(_translate("SimpleDialog", "Batching"))
        self.groupBoxInfo.setTitle(_translate("SimpleDialog", "Info"))
        self.labelName.setText(_translate("SimpleDialog", "Name:"))

