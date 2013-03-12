
from PyQt4 import QtGui, QtCore
import sys, os, random


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

'''

'''
class epochScrollArea(QtGui.QScrollArea):

    def __init__(self, parent):
        super(epochScrollArea, self).__init__(parent)

        #self.scrollArea = QtGui.QScrollArea(self.centralwidget)
        #self.scrollArea.setGeometry(QtCore.QRect(10, 230, 341, 321))
        self.setWidgetResizable(True)
        self.setObjectName(_fromUtf8("scrollArea"))
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
        
        self.setWidget(self.scrollAreaWidgetContents)
        
        
'''
Simple example of custom widget
'''        
class FormWidget(QtGui.QWidget):

    def __init__(self, parent):        
        super(FormWidget, self).__init__(parent)
        self.layout = QtGui.QVBoxLayout(self)

        self.button1 = QtGui.QPushButton("Button 1")
        self.layout.addWidget(self.button1)

        self.button2 = QtGui.QPushButton("Button 2")
        self.layout.addWidget(self.button2)
        
    