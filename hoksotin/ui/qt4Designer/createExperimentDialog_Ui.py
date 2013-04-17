# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createExperimentDialog.ui'
#
# Created: Wed Apr 17 19:09:15 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CreateExperimentDialog(object):
    def setupUi(self, CreateExperimentDialog):
        CreateExperimentDialog.setObjectName(_fromUtf8("CreateExperimentDialog"))
        CreateExperimentDialog.setWindowModality(QtCore.Qt.WindowModal)
        CreateExperimentDialog.resize(733, 810)
        self.gridLayout_3 = QtGui.QGridLayout(CreateExperimentDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(CreateExperimentDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.showFileInfoButton = QtGui.QPushButton(self.groupBox)
        self.showFileInfoButton.setObjectName(_fromUtf8("showFileInfoButton"))
        self.horizontalLayout_3.addWidget(self.showFileInfoButton)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.splitter = QtGui.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.FilePathLineEdit = QtGui.QLineEdit(self.splitter)
        self.FilePathLineEdit.setObjectName(_fromUtf8("FilePathLineEdit"))
        self.browseButton = QtGui.QPushButton(self.splitter)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(CreateExperimentDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelAuthor = QtGui.QLabel(self.groupBox_2)
        self.labelAuthor.setObjectName(_fromUtf8("labelAuthor"))
        self.horizontalLayout.addWidget(self.labelAuthor)
        self.lineEditAuthor = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditAuthor.setObjectName(_fromUtf8("lineEditAuthor"))
        self.horizontalLayout.addWidget(self.lineEditAuthor)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelExperimentName = QtGui.QLabel(self.groupBox_2)
        self.labelExperimentName.setObjectName(_fromUtf8("labelExperimentName"))
        self.horizontalLayout_2.addWidget(self.labelExperimentName)
        self.lineEditProjectName = QtGui.QLineEdit(self.groupBox_2)
        self.lineEditProjectName.setObjectName(_fromUtf8("lineEditProjectName"))
        self.horizontalLayout_2.addWidget(self.lineEditProjectName)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.labelDescription = QtGui.QLabel(self.groupBox_2)
        self.labelDescription.setObjectName(_fromUtf8("labelDescription"))
        self.gridLayout_2.addWidget(self.labelDescription, 2, 0, 1, 1)
        self.textEditDescription = QtGui.QTextEdit(self.groupBox_2)
        self.textEditDescription.setObjectName(_fromUtf8("textEditDescription"))
        self.gridLayout_2.addWidget(self.textEditDescription, 3, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(CreateExperimentDialog)
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.gridLayout_3.addWidget(self.cancelOkButtonBox, 2, 0, 1, 1)
        self.frameProgressBar = QtGui.QFrame(CreateExperimentDialog)
        self.frameProgressBar.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frameProgressBar.setFrameShadow(QtGui.QFrame.Raised)
        self.frameProgressBar.setObjectName(_fromUtf8("frameProgressBar"))
        self.gridLayout_3.addWidget(self.frameProgressBar, 3, 0, 1, 1)

        self.retranslateUi(CreateExperimentDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CreateExperimentDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CreateExperimentDialog.reject)
        QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CreateExperimentDialog.openFileChooserDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateExperimentDialog)

    def retranslateUi(self, CreateExperimentDialog):
        CreateExperimentDialog.setWindowTitle(_translate("CreateExperimentDialog", "Create new experiment", None))
        self.groupBox.setTitle(_translate("CreateExperimentDialog", "Experiment base file", None))
        self.showFileInfoButton.setText(_translate("CreateExperimentDialog", "Show file info", None))
        self.browseButton.setText(_translate("CreateExperimentDialog", "Browse...", None))
        self.label.setText(_translate("CreateExperimentDialog", "Select raw file for the experiment:", None))
        self.groupBox_2.setTitle(_translate("CreateExperimentDialog", "Experiment information", None))
        self.labelAuthor.setText(_translate("CreateExperimentDialog", "Experiment author:", None))
        self.labelExperimentName.setText(_translate("CreateExperimentDialog", "Experiment name:", None))
        self.labelDescription.setText(_translate("CreateExperimentDialog", "Experiment description:", None))

