# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt4Designer/createProjectDialog.ui'
#
# Created: Fri Mar 15 14:29:14 2013
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

class Ui_CreateProjectDialog(object):
    def setupUi(self, CreateProjectDialog):
        CreateProjectDialog.setObjectName(_fromUtf8("CreateProjectDialog"))
        CreateProjectDialog.setWindowModality(QtCore.Qt.WindowModal)
        CreateProjectDialog.resize(382, 399)
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(CreateProjectDialog)
        self.cancelOkButtonBox.setGeometry(QtCore.QRect(20, 350, 176, 31))
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.widget = QtGui.QWidget(CreateProjectDialog)
        self.widget.setGeometry(QtCore.QRect(20, 10, 341, 331))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.splitter = QtGui.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.FilePathLineEdit = QtGui.QLineEdit(self.splitter)
        self.FilePathLineEdit.setObjectName(_fromUtf8("FilePathLineEdit"))
        self.browseButton = QtGui.QPushButton(self.splitter)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.verticalLayout.addWidget(self.splitter)
        self.showFileInfoButton = QtGui.QPushButton(self.widget)
        self.showFileInfoButton.setObjectName(_fromUtf8("showFileInfoButton"))
        self.verticalLayout.addWidget(self.showFileInfoButton)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelProjectName = QtGui.QLabel(self.widget)
        self.labelProjectName.setObjectName(_fromUtf8("labelProjectName"))
        self.horizontalLayout_2.addWidget(self.labelProjectName)
        self.lineEditProjectName = QtGui.QLineEdit(self.widget)
        self.lineEditProjectName.setObjectName(_fromUtf8("lineEditProjectName"))
        self.horizontalLayout_2.addWidget(self.lineEditProjectName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelAuthor = QtGui.QLabel(self.widget)
        self.labelAuthor.setObjectName(_fromUtf8("labelAuthor"))
        self.horizontalLayout.addWidget(self.labelAuthor)
        self.lineEditAuthor = QtGui.QLineEdit(self.widget)
        self.lineEditAuthor.setObjectName(_fromUtf8("lineEditAuthor"))
        self.horizontalLayout.addWidget(self.lineEditAuthor)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.labelDescritption = QtGui.QLabel(self.widget)
        self.labelDescritption.setObjectName(_fromUtf8("labelDescritption"))
        self.verticalLayout_2.addWidget(self.labelDescritption)
        self.textEditDescription = QtGui.QTextEdit(self.widget)
        self.textEditDescription.setObjectName(_fromUtf8("textEditDescription"))
        self.verticalLayout_2.addWidget(self.textEditDescription)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.retranslateUi(CreateProjectDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CreateProjectDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CreateProjectDialog.reject)
        #QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CreateProjectDialog.openFileChooserDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateProjectDialog)

    def retranslateUi(self, CreateProjectDialog):
        CreateProjectDialog.setWindowTitle(_translate("CreateProjectDialog", "Create new project", None))
        self.label.setText(_translate("CreateProjectDialog", "***project created in the same folder as picked file", None))
        self.browseButton.setText(_translate("CreateProjectDialog", "Browse...", None))
        self.showFileInfoButton.setText(_translate("CreateProjectDialog", "Show file info", None))
        self.labelProjectName.setText(_translate("CreateProjectDialog", "Project name:", None))
        self.labelAuthor.setText(_translate("CreateProjectDialog", "Author:", None))
        self.labelDescritption.setText(_translate("CreateProjectDialog", "Description:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CreateProjectDialog = QtGui.QDialog()
    ui = Ui_CreateProjectDialog()
    ui.setupUi(CreateProjectDialog)
    CreateProjectDialog.show()
    sys.exit(app.exec_())

