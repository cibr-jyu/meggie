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
import fileManager

class ForwardModelModel(QAbstractTableModel):
    '''
    Model class for forward model related views in MainWindow. Please don't get
    confused by the "model" and "forward model" -
    the former is model as in model-view-controller, the latter is an MNE term. 
    
    TODO pitäis varmaan kysyä heti initialisoidessa subjectilta, onko hakemistoa
    noille forward modeleille, ja sitten asettaa self.filename siihen
    hakemistoon
    '''

    def __init__(self, experiment):
        self.fmodelsDirectory = experiment._active_subject.\
                      _forwardModels_directory
                      
        # File that includes forward model names, their parameters and 
        # corresponding files. Full path needed, hence the directory.
        
        # Actually not needed, as the model is not editable via GUI.
        self.dirty = False
        
        # Each dictionary in the list includes parameters
        self.fmodelInfoList = [dict()]
        self.fmodelInfoListKeys = ["name",]
        
        # Column headers i.e. names of parameters.
        self.__headers = ['name', 'spacing', 'ico', 'surfname', 'cps', 'atlas',
                          'triang. ico', 'homog', 'innershift', 'outershift'
                          'skullshift', 'brainc', 'skullc', 'scalpc']
        
    
    
    def getCurrentFmodelModelFile(self):
        filename = os.path.join(self.fmodelsDirectory, "fmodelModel")
            
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
            column = index.column()
            
            fmodel = self.fmodelInfoList[row]
            fmname = fmodel["name"]
            
            # TODO tähän palauttamaan ne parametrit
            return fmname
            
        else: return QVariant()
        
    
    def removeRows(self, position, rows=1, parent=QModelIndex()):
        """
        Simple removal of a single row of fmodel.
        """
        self.beginRemoveRows(parent, position, position + rows - 1)
        value = self.fmodelInfo[position]
        self.fmodelInfo.remove(value)
        # TODO also remember to delete actual directory on the disk
        self.endRemoveRows()
        return True
        
            
        
    def initializeModel(self):
        """
        Reads the active subject's forwardModels directory and populates the
        data accordingly.
        
        Eli:
        
        1. Lue forwardModels-hakemistot ja ota kustakin param-filu
        2. Parsi kustakin param-filusta parametrit ja laita ne fModelInfoList,
        listaan dicteinä.
        """
        
        if os.path.isdir(self.fmodelsDirectory):
            for d in self.fmodelsDirectory:
                try: 
                    sSpaceDict = fileManager.unpickle(os.path.join(d, 
                                                  'setupSourceSpace.param'))
                except:
                    sSpaceDict = dict()
                    
                try:
                    wshedDict = fileManager.unpickle(os.path.join(d,
                                                 'wshed.param'))
                except:
                    wshedDict = dict()
                    
                try:
                    setupFModelDict = fileManager.unpickle(os.path.join(d, 
                                                       'setupFModel.param'))
                except:
                    setupFModelDict = dict()
                
                mergedDict = dict(sSpaceDict.items() + wshedDict.items() + 
                                  setupFModelDict.items())
                self.fmodelInfoList.append(mergedDict)


# class CoregistrationModel(QAbstractTableModel):
    