# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIehdotus10.ui'
#
# Created: Sat Apr 13 15:16:48 2013
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(892, 701)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabBlank = QtGui.QWidget()
        self.tabBlank.setObjectName(_fromUtf8("tabBlank"))
        self.tabWidget.addTab(self.tabBlank, _fromUtf8(""))
        self.tabRaw = QtGui.QWidget()
        self.tabRaw.setObjectName(_fromUtf8("tabRaw"))
        self.gridLayout = QtGui.QGridLayout(self.tabRaw)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.metaBox = QtGui.QGroupBox(self.tabRaw)
        self.metaBox.setObjectName(_fromUtf8("metaBox"))
        self.layoutWidget_2 = QtGui.QWidget(self.metaBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(26, 35, 221, 54))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.labelDate = QtGui.QLabel(self.layoutWidget_2)
        self.labelDate.setObjectName(_fromUtf8("labelDate"))
        self.gridLayout_5.addWidget(self.labelDate, 0, 0, 1, 1)
        self.labelDateValue = QtGui.QLabel(self.layoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelDateValue.sizePolicy().hasHeightForWidth())
        self.labelDateValue.setSizePolicy(sizePolicy)
        self.labelDateValue.setObjectName(_fromUtf8("labelDateValue"))
        self.gridLayout_5.addWidget(self.labelDateValue, 0, 1, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelSubject = QtGui.QLabel(self.layoutWidget_2)
        self.labelSubject.setObjectName(_fromUtf8("labelSubject"))
        self.horizontalLayout.addWidget(self.labelSubject)
        self.labelSubjectValue = QtGui.QLabel(self.layoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSubjectValue.sizePolicy().hasHeightForWidth())
        self.labelSubjectValue.setSizePolicy(sizePolicy)
        self.labelSubjectValue.setObjectName(_fromUtf8("labelSubjectValue"))
        self.horizontalLayout.addWidget(self.labelSubjectValue)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addWidget(self.metaBox)
        self.channelsBox = QtGui.QGroupBox(self.tabRaw)
        self.channelsBox.setObjectName(_fromUtf8("channelsBox"))
        self.layoutWidget_7 = QtGui.QWidget(self.channelsBox)
        self.layoutWidget_7.setGeometry(QtCore.QRect(30, 30, 251, 112))
        self.layoutWidget_7.setObjectName(_fromUtf8("layoutWidget_7"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.layoutWidget_7)
        self.verticalLayout_8.setMargin(0)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.labelEEG = QtGui.QLabel(self.layoutWidget_7)
        self.labelEEG.setObjectName(_fromUtf8("labelEEG"))
        self.horizontalLayout_6.addWidget(self.labelEEG)
        self.labelEEGValue = QtGui.QLabel(self.layoutWidget_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelEEGValue.sizePolicy().hasHeightForWidth())
        self.labelEEGValue.setSizePolicy(sizePolicy)
        self.labelEEGValue.setObjectName(_fromUtf8("labelEEGValue"))
        self.horizontalLayout_6.addWidget(self.labelEEGValue)
        self.verticalLayout_8.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelGradMEG = QtGui.QLabel(self.layoutWidget_7)
        self.labelGradMEG.setObjectName(_fromUtf8("labelGradMEG"))
        self.horizontalLayout_7.addWidget(self.labelGradMEG)
        self.labelGradMEGValue = QtGui.QLabel(self.layoutWidget_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelGradMEGValue.sizePolicy().hasHeightForWidth())
        self.labelGradMEGValue.setSizePolicy(sizePolicy)
        self.labelGradMEGValue.setObjectName(_fromUtf8("labelGradMEGValue"))
        self.horizontalLayout_7.addWidget(self.labelGradMEGValue)
        self.verticalLayout_8.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.labelMagMEG = QtGui.QLabel(self.layoutWidget_7)
        self.labelMagMEG.setObjectName(_fromUtf8("labelMagMEG"))
        self.horizontalLayout_8.addWidget(self.labelMagMEG)
        self.labelMagMEGValue = QtGui.QLabel(self.layoutWidget_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMagMEGValue.sizePolicy().hasHeightForWidth())
        self.labelMagMEGValue.setSizePolicy(sizePolicy)
        self.labelMagMEGValue.setObjectName(_fromUtf8("labelMagMEGValue"))
        self.horizontalLayout_8.addWidget(self.labelMagMEGValue)
        self.verticalLayout_8.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.labelSamples = QtGui.QLabel(self.layoutWidget_7)
        self.labelSamples.setObjectName(_fromUtf8("labelSamples"))
        self.horizontalLayout_9.addWidget(self.labelSamples)
        self.labelSamplesValue = QtGui.QLabel(self.layoutWidget_7)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSamplesValue.sizePolicy().hasHeightForWidth())
        self.labelSamplesValue.setSizePolicy(sizePolicy)
        self.labelSamplesValue.setObjectName(_fromUtf8("labelSamplesValue"))
        self.horizontalLayout_9.addWidget(self.labelSamplesValue)
        self.verticalLayout_8.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_3.addWidget(self.channelsBox)
        self.filtersBox = QtGui.QGroupBox(self.tabRaw)
        self.filtersBox.setObjectName(_fromUtf8("filtersBox"))
        self.layoutWidget_6 = QtGui.QWidget(self.filtersBox)
        self.layoutWidget_6.setGeometry(QtCore.QRect(24, 32, 221, 65))
        self.layoutWidget_6.setObjectName(_fromUtf8("layoutWidget_6"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelLow = QtGui.QLabel(self.layoutWidget_6)
        self.labelLow.setLineWidth(1)
        self.labelLow.setScaledContents(True)
        self.labelLow.setObjectName(_fromUtf8("labelLow"))
        self.horizontalLayout_4.addWidget(self.labelLow)
        self.labelLowValue = QtGui.QLabel(self.layoutWidget_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLowValue.sizePolicy().hasHeightForWidth())
        self.labelLowValue.setSizePolicy(sizePolicy)
        self.labelLowValue.setObjectName(_fromUtf8("labelLowValue"))
        self.horizontalLayout_4.addWidget(self.labelLowValue)
        self.verticalLayout_7.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelHigh = QtGui.QLabel(self.layoutWidget_6)
        self.labelHigh.setObjectName(_fromUtf8("labelHigh"))
        self.horizontalLayout_5.addWidget(self.labelHigh)
        self.labelHighValue = QtGui.QLabel(self.layoutWidget_6)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHighValue.sizePolicy().hasHeightForWidth())
        self.labelHighValue.setSizePolicy(sizePolicy)
        self.labelHighValue.setObjectName(_fromUtf8("labelHighValue"))
        self.horizontalLayout_5.addWidget(self.labelHighValue)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3.addWidget(self.filtersBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.triggersBox = QtGui.QGroupBox(self.tabRaw)
        self.triggersBox.setObjectName(_fromUtf8("triggersBox"))
        self.listWidget = QtGui.QListWidget(self.triggersBox)
        self.listWidget.setGeometry(QtCore.QRect(10, 30, 241, 141))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.verticalLayout_4.addWidget(self.triggersBox)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonMNE_Browse_Raw = QtGui.QPushButton(self.tabRaw)
        self.pushButtonMNE_Browse_Raw.setObjectName(_fromUtf8("pushButtonMNE_Browse_Raw"))
        self.verticalLayout.addWidget(self.pushButtonMNE_Browse_Raw)
        self.pushButtonMaxFilter = QtGui.QPushButton(self.tabRaw)
        self.pushButtonMaxFilter.setObjectName(_fromUtf8("pushButtonMaxFilter"))
        self.verticalLayout.addWidget(self.pushButtonMaxFilter)
        self.horizontalLayout_11.addLayout(self.verticalLayout)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.pushButtonEOG = QtGui.QPushButton(self.tabRaw)
        self.pushButtonEOG.setObjectName(_fromUtf8("pushButtonEOG"))
        self.verticalLayout_5.addWidget(self.pushButtonEOG)
        self.pushButtonECG = QtGui.QPushButton(self.tabRaw)
        self.pushButtonECG.setObjectName(_fromUtf8("pushButtonECG"))
        self.verticalLayout_5.addWidget(self.pushButtonECG)
        self.horizontalLayout_11.addLayout(self.verticalLayout_5)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButtonEpoch = QtGui.QPushButton(self.tabRaw)
        self.pushButtonEpoch.setObjectName(_fromUtf8("pushButtonEpoch"))
        self.verticalLayout_2.addWidget(self.pushButtonEpoch)
        self.pushButtonAverage = QtGui.QPushButton(self.tabRaw)
        self.pushButtonAverage.setObjectName(_fromUtf8("pushButtonAverage"))
        self.verticalLayout_2.addWidget(self.pushButtonAverage)
        self.pushButtonVisualize = QtGui.QPushButton(self.tabRaw)
        self.pushButtonVisualize.setObjectName(_fromUtf8("pushButtonVisualize"))
        self.verticalLayout_2.addWidget(self.pushButtonVisualize)
        self.horizontalLayout_11.addLayout(self.verticalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem2)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabRaw, _fromUtf8(""))
        self.tabPreprocessing = QtGui.QWidget()
        self.tabPreprocessing.setObjectName(_fromUtf8("tabPreprocessing"))
        self.tabWidget.addTab(self.tabPreprocessing, _fromUtf8(""))
        self.verticalLayout_3.addWidget(self.tabWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 892, 29))
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
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionCreate_experiment = QtGui.QAction(MainWindow)
        self.actionCreate_experiment.setObjectName(_fromUtf8("actionCreate_experiment"))
        self.actionOpen_experiment = QtGui.QAction(MainWindow)
        self.actionOpen_experiment.setObjectName(_fromUtf8("actionOpen_experiment"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.menuFile.addAction(self.actionCreate_experiment)
        self.menuFile.addAction(self.actionOpen_experiment)
        self.menuTools.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.toolBar.addAction(self.actionCreate_experiment)
        self.toolBar.addAction(self.actionOpen_experiment)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.metaBox.setTitle(_translate("MainWindow", "Background", None))
        self.labelDate.setText(_translate("MainWindow", "Date:", None))
        self.labelDateValue.setText(_translate("MainWindow", "DateValue", None))
        self.labelSubject.setText(_translate("MainWindow", "Subject:", None))
        self.labelSubjectValue.setText(_translate("MainWindow", "TextLabel", None))
        self.channelsBox.setTitle(_translate("MainWindow", "Channels", None))
        self.labelEEG.setText(_translate("MainWindow", "EEG channels:", None))
        self.labelEEGValue.setText(_translate("MainWindow", "EEG value", None))
        self.labelGradMEG.setText(_translate("MainWindow", "Gradiometers:", None))
        self.labelGradMEGValue.setText(_translate("MainWindow", "Grad. MEG value", None))
        self.labelMagMEG.setText(_translate("MainWindow", "Magnetometers:", None))
        self.labelMagMEGValue.setText(_translate("MainWindow", "Mag. MEG value", None))
        self.labelSamples.setText(_translate("MainWindow", "Sampling frequency:", None))
        self.labelSamplesValue.setText(_translate("MainWindow", "SamplesValue", None))
        self.filtersBox.setTitle(_translate("MainWindow", "Filters", None))
        self.labelLow.setText(_translate("MainWindow", "Low-pass:", None))
        self.labelLowValue.setText(_translate("MainWindow", "Low-pass value", None))
        self.labelHigh.setText(_translate("MainWindow", "High-pass:", None))
        self.labelHighValue.setText(_translate("MainWindow", "High-pass value", None))
        self.triggersBox.setTitle(_translate("MainWindow", "Triggers", None))
        self.pushButtonMNE_Browse_Raw.setText(_translate("MainWindow", "MNE_Browse_Raw", None))
        self.pushButtonMaxFilter.setText(_translate("MainWindow", "MaxFilter", None))
        self.pushButtonEOG.setText(_translate("MainWindow", "Calculate EOG projections", None))
        self.pushButtonECG.setText(_translate("MainWindow", "Calculate ECG projections", None))
        self.pushButtonEpoch.setText(_translate("MainWindow", "Epoch", None))
        self.pushButtonAverage.setText(_translate("MainWindow", "Average", None))
        self.pushButtonVisualize.setText(_translate("MainWindow", "Visualize", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabRaw), _translate("MainWindow", "Raw", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabPreprocessing), _translate("MainWindow", "Preprocessing", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.actionCreate_experiment.setText(_translate("MainWindow", "Create new experiment...", None))
        self.actionOpen_experiment.setText(_translate("MainWindow", "Open experiment...", None))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences", None))

