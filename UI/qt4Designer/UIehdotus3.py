# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIehdotus2.ui'
#
# Created: Thu Mar  7 15:27:56 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
import EOG

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1081, 707)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(30, 20, 256, 192))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(365, 0, 711, 651))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(10, 230, 341, 321))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 339, 319))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.comboBox_2 = QtGui.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 190, 85, 31))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox = QtGui.QComboBox(self.scrollAreaWidgetContents)
        self.comboBox.setGeometry(QtCore.QRect(80, 40, 85, 31))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.eventMarginalMin = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.eventMarginalMin.setGeometry(QtCore.QRect(60, 100, 51, 31))
        self.eventMarginalMin.setText(_fromUtf8(""))
        self.eventMarginalMin.setObjectName(_fromUtf8("eventMarginalMin"))
        self.eventMarginalMax = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.eventMarginalMax.setGeometry(QtCore.QRect(60, 140, 51, 31))
        self.eventMarginalMax.setObjectName(_fromUtf8("eventMarginalMax"))
        self.drawButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.drawButton.setGeometry(QtCore.QRect(220, 280, 95, 31))
        self.drawButton.setObjectName(_fromUtf8("drawButton"))
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(110, 10, 101, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(0, 190, 101, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 66, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 41, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 66, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setGeometry(QtCore.QRect(220, 30, 66, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.checkBox = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox.setGeometry(QtCore.QRect(210, 60, 93, 26))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox_2 = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_2.setGeometry(QtCore.QRect(210, 90, 93, 26))
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkBox_3 = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_3.setGeometry(QtCore.QRect(210, 120, 111, 26))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.checkBox_4 = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.checkBox_4.setGeometry(QtCore.QRect(210, 150, 121, 26))
        self.checkBox_4.setObjectName(_fromUtf8("checkBox_4"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 29))
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_file = QtGui.QAction(MainWindow)
        self.actionLoad_file.setObjectName(_fromUtf8("actionLoad_file"))
        self.actionSave_file = QtGui.QAction(MainWindow)
        self.actionSave_file.setObjectName(_fromUtf8("actionSave_file"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.menuFile.addAction(self.actionLoad_file)
        self.menuFile.addAction(self.actionSave_file)
        self.menuTools.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())


        self.drawButton.clicked.connect(self.drawEOGEpochs)        



        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
      
          
    def drawEOGEpochs(self):
        min = self.eventMarginalMin.text()
        max = self.eventMarginalMax.text()
        EOG.drawEOGEpochs(float(min), float(max), 'STI 001')
        

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "1", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Alkuperäinen raakatiedosto", None))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", " sss1 (parametrejä täällä)", None))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "sss2 (muita parametrejä)", None))
        self.treeWidget.topLevelItem(0).child(1).child(0).setText(0, _translate("MainWindow", "sss2 lisäkäsiteltynä (eog?)", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.drawButton.setText(_translate("MainWindow", "Draw", None))
        self.label.setText(_translate("MainWindow", "Epoch selector", None))
        self.label_2.setText(_translate("MainWindow", "Stim channel:", None))
        self.label_3.setText(_translate("MainWindow", "tmin", None))
        self.label_4.setText(_translate("MainWindow", "tmax", None))
        self.label_5.setText(_translate("MainWindow", "Preset", None))
        self.label_6.setText(_translate("MainWindow", "Show:", None))
        self.checkBox.setText(_translate("MainWindow", "EOG", None))
        self.checkBox_2.setText(_translate("MainWindow", "ECG", None))
        self.checkBox_3.setText(_translate("MainWindow", "StimChannel", None))
        self.checkBox_4.setText(_translate("MainWindow", "BadChannels", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.actionLoad_file.setText(_translate("MainWindow", "Load file", None))
        self.actionSave_file.setText(_translate("MainWindow", "Save file", None))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

