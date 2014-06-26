'''
Created on 26.6.2014

@author: kpaliran

Contains modules for views in various UI components, mainly MainWindow.

'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys

class ForwardModelModel(QAbstractTableModel):
    '''
    Model class for forward model relates views in MainWindow. Please don't get
    confused by the "model" and "forward model" -
    the former is model as in model-view-controller, the latter is an MNE term. 
    '''

    def __init__(self, filename=QString()):
        # File that includes forward model names, their parameters and 
        # corresponding files.
        self.filename = filename
        self.dirty = False
        # Names of the forward models, read from the file with self.filename.
        self.names = []
        
    
    def rowCount(self, index=QModelIndex()):
        """
        The associated view should have as many rows as there are 
        forward model names.
        """
        return len(self.names)
    
    def columnCount(self, index=QModelIndex()):
        """
        The associated view only has one column, the one to show the name 
        of the forward model.
        """
        return 1
        
    def data(self, index, role):
        """
        Standard data method for the QAbstractTableModel.
        """
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.names(index.row()))
        
        
class CoregistrationModel(QAbstractTableModel):
    