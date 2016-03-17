"""
Created on Sep 22, 2013

@author: atmiraut
"""

from PyQt4 import QtGui, QtCore

class ListWidget(QtGui.QListWidget):
    """
    classdocs
    """
    def __init__(self, parent = None):
        QtGui.QListWidget.__init__(self, parent)