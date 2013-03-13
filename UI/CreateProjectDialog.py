# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createProjectDialog.ui'
#
# Created: Tue Mar 12 12:05:21 2013
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

class CreateProjectDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(514, 314)
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(270, 220, 176, 31))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.widget = QtGui.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(80, 20, 337, 136))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.splitter = QtGui.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.lineEdit = QtGui.QLineEdit(self.splitter)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton = QtGui.QPushButton(self.splitter)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.verticalLayout.addWidget(self.splitter)
        self.pushButton_2 = QtGui.QPushButton(self.widget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.verticalLayout.addWidget(self.pushButton_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.openFileChooserDialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def openFileChooserDialog(self):
        fname = QtGui.QFileDialog.getOpenFileName(Dialog, 'Open file', 
                '/home')    

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Create new project", None))
        self.label.setText(_translate("Dialog", "***project created in the same folder as picked file", None))
        self.pushButton.setText(_translate("Dialog", "Browse...", None))
        self.pushButton_2.setText(_translate("Dialog", "Show file info", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = CreateProjectDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

