# Form implementation generated from reading ui file './meggie/mainwindow/dialogs/actionDialogUi.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_ActionDialog(object):
    def setupUi(self, ActionDialog):
        ActionDialog.setObjectName("ActionDialog")
        ActionDialog.resize(518, 440)
        self.gridLayoutDialog = QtWidgets.QGridLayout(ActionDialog)
        self.gridLayoutDialog.setObjectName("gridLayoutDialog")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonClose = QtWidgets.QPushButton(parent=ActionDialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.gridLayoutDialog.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.treeWidgetActions = QtWidgets.QTreeWidget(parent=ActionDialog)
        self.treeWidgetActions.setSelectionMode(
            QtWidgets.QAbstractItemView.SelectionMode.NoSelection
        )
        self.treeWidgetActions.setAnimated(True)
        self.treeWidgetActions.setObjectName("treeWidgetActions")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetActions)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidgetActions)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.treeWidgetActions.topLevelItem(1).child(2).setText(0, "create_spectrum")
        item_1.setToolTip(0, "")
        item_1.setStatusTip(0, "")
        item_1.setWhatsThis(0, "")
        item_1.setFlags(QtCore.Qt.ItemFlag.ItemIsEnabled)
        self.treeWidgetActions.header().setVisible(False)
        self.gridLayoutDialog.addWidget(self.treeWidgetActions, 0, 0, 1, 1)

        self.retranslateUi(ActionDialog)
        self.pushButtonClose.clicked.connect(ActionDialog.accept)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(ActionDialog)

    def retranslateUi(self, ActionDialog):
        _translate = QtCore.QCoreApplication.translate
        ActionDialog.setWindowTitle(_translate("ActionDialog", "Meggie - Actions"))
        self.pushButtonClose.setText(_translate("ActionDialog", "Close"))
        self.treeWidgetActions.headerItem().setText(
            0, _translate("ActionDialog", "Action")
        )
        __sortingEnabled = self.treeWidgetActions.isSortingEnabled()
        self.treeWidgetActions.setSortingEnabled(False)
        self.treeWidgetActions.topLevelItem(0).setText(
            0, _translate("ActionDialog", "subject_001")
        )
        self.treeWidgetActions.topLevelItem(0).child(0).setText(
            0, _translate("ActionDialog", "ica")
        )
        self.treeWidgetActions.topLevelItem(0).child(1).setText(
            0, _translate("ActionDialog", "filter")
        )
        self.treeWidgetActions.topLevelItem(1).setText(
            0, _translate("ActionDialog", "subject_002")
        )
        self.treeWidgetActions.topLevelItem(1).child(0).setText(
            0, _translate("ActionDialog", "ica")
        )
        self.treeWidgetActions.topLevelItem(1).child(1).setText(
            0, _translate("ActionDialog", "filter")
        )
        self.treeWidgetActions.setSortingEnabled(__sortingEnabled)
