# coding: latin1

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
import os
from csv import Dialect

class ForwardModelModel(QAbstractListModel):
    '''
    Model class for forward model related views in MainWindow. Please don't get
    confused by the "model" and "forward model" -
    the former is model as in model-view-controller, the latter is an MNE term. 
    
    TODO pitäis varmaan kysyä heti initialisoidessa subjectilta, onko hakemistoa
    noille forward modeleille, ja sitten asettaa self.filename siihen
    hakemistoon
    '''

    def __init__(self, experiment):
        # File that includes forward model names, their parameters and 
        # corresponding files. Use full path.
        # TODO tämä pitäisi luultavasti saada subjectilta.
        self.fmodelDirectory = experiment._active_subject.\
                      _forwardModels_directory
        self.fmodelFile = getCurrentFmodelModelFile(experiment)
        self.dirty = False
        # Info of the forward models, read from the file with self.filename.
        # TODO sisältääkö generoidut tiedostot jo infoa fmodeleista, jolloin
        # tässä riittäisi pelkkä hakemiston polku?
        self.fmodelInfoList = [dict()]
        self.fmodelInfoListKeys = ["name","fpath"]
        
        # One could put column headers here
        # self.__headers = headers
        
        
    def getCurrentFmodelModelFile(self):
        filename = os.path.join(self.fmodelDirectory, "fmodelModel")
            
        if os.path.isfile(filename):
            return filename
        
        return None
        
    
    def rowCount(self, index=QModelIndex()):
        """
        The associated view should have as many rows as there are 
        forward model names.
        """
        return len(self.fmodelInfoList)
    
    
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
        
    
    def removeRows(self, position, rows=1, parent=QModelIndex()):
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
        
        try:
            writer = csv.DictWriter(self.filename, self.fmodelInfoListKeys)
            writer = writer.writerows(self.fmodelInfoList)
        except IOError:
            raise Exception("Problem writing to desired directory")
        
        
    def readModelFromDisk(self):
        """
        Reads from disk the info related to fmodel, currently name and
        the path to the directory of the fmodel.
        """
        
        dialect = Dialect()
        dialect.delimiter = ";"
        
        try:
            fileReadDict = csv.DictReader(self.filename)
            self.fmodelInfoList = fileReadDict  
        except IOError:
            raise Exception("No forward model model file found")
        
        

    def initializeModel(self):
        """
        
        """
        
# class CoregistrationModel(QAbstractTableModel):
    