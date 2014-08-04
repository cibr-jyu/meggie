'''
Created on 26.6.2014

@author: kpaliran

Contains models for views in various UI components, mainly MainWindow.
TODO Also contains methods for writing the models to disk (using fileManager module).
'''

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import csv
import dialects
from csv import Dialect

class ForwardModelModel(QAbstractListModel):
    '''
    Model class for forward model related views in MainWindow. Please don't get
    confused by the "model" and "forward model" -
    the former is model as in model-view-controller, the latter is an MNE term. 
    '''

    def __init__(self, filename=QString()):
        # File that includes forward model names, their parameters and 
        # corresponding files. Use full path.
        # TODO tämä pitäisi luultavasti saada subjectilta.
        self.filename = filename
        self.dirty = False
        # Info of the forward models, read from the file with self.filename.
        # Includes information about generat
        # TODO sisältääkö generoidut tiedostot jo infoa fmodeleista, jolloin
        # tässä riittäisi pelkkä hakemiston polku?
        self.fmodelInfoList = [dict()]
        self.fmodelInfoListKeys = ["name","fpath"]
        
        # One could put column headers here
        # self.__headers = headers
        
    
    def rowCount(self, index=QModelIndex()):
        """
        The associated view should have as many rows as there are 
        forward model names.
        """
        return len(self.names)
    
    
    def columnCount(self, index=QModelIndex()):
        """
        The associated view only has one column, the one to show the name 
        of the forward model. Increase value to get more colums.
        """
        return 1
    
        
    def data(self, index, role):
        """
        Standard data method for the QAbstractTableModel.
        """
        if not index.isValid():
            return QVariant()
        
        # No need to use anything else but displayrole here. 
        if role == Qt.DisplayRole:
            row = index.row()
            # column = index.column() needed if shown more info than just name
            
            fmodel = self.fmodelInfo[row]
            fmname = fmodel["name"]
            return fmname
            
        else: return QVariant()
        
    
    def removeRows(self, position, rows=1, parent=QtCore.QModelIndex()):
        """
        Simple removal of a single row of fmodel.
        """
        self.beginRemoveRows(parent, position, position + rows - 1)
        value = self.fmodelInfo[position]
        self.fmodelInfo.remove(value)
        self.endRemoveRows()
        return True
        

    def writeModelToDisk(self):
        """
        Writes to disk the info related to the fmodel, currently name and
        the path to the directory of the fmodel.
        """
        
        dialect = Dialect()
        dialect.delimiter = ";"
        
        writer = csv.DictWriter(self.filename, self.fmodelInfoListKeys)
        writer = writer.writerows(self.fmodelInfoList)
        
        
    def readModelFromDisk(self):
        """
        Reads from disk the info related to fmodel, currently name and
        the path to the directory of the fmodel.
        """
        
        dialect = Dialect()
        dialect.delimiter = ";"
        
        fileReadDict = csv.DictReader(self.filename)
        self.fmodelInfoList = fileReadDict
        

    def initializeModel(self):
        """
        
        """
        
# class CoregistrationModel(QAbstractTableModel):
    