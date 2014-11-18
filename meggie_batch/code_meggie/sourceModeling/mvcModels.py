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
        self.fmodelDirectory = experiment._active_subject.\
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
        

    def createModel(self):
        """
        Reads the active subject's forwardModel directory and populates the
        data accor
        """
        
        # Parametrit ehkä suoraan filuista, kts. mne_setup_forward model ja mitä
        # se 5120 tarkoittaa filuissa. mne.surface-modulissa on metodi:
        # a =  mne.read_bem_surfaces("reconFiles-5120-bem-sol.fif")
        # ja sitten voi kysellä tyyliin:
        # a[0]['ntri'], joka palauttaa sen 5120:n.
        # shift-argumentit varmaan saa luettua filusta, että conductivityt?
        

    def writeModelToDisk(self):
        """
        Writes to disk the info related to the fmodel, currently name and
        the path to the directory of the fmodel.
        
        TODO: probably not needed, see readModelFromDisk.
        """
        
        dialect = Dialect()
        dialect.delimiter = ";"
        
        try:
            filename = os.path.join(self.fmodelDirectory, "fmodelModel")
            writer = csv.DictWriter(filename, self.fmodelInfoListKeys)
            writer = writer.writerows(self.fmodelInfoList)
        except IOError:
            raise Exception("Problem writing to desired directory")
        
        
    def readModelFromDisk(self):
        """
        Reads from disk the info related to fmodel, currently name and
        the path to the directory of the fmodel.
        
        TODO: should probably read the fmodel directories directly from disk and
        populate model from it, instead of trying to keep the model file in
        sync. If possible, just read fmodel directory names, and if parameters
        need showing, try to read them from files, too.
        """
        
        cdialect = Dialect()
        cdialect.delimiter = ";"
        
        try:
            fileReadDict = csv.DictReader(self.fmodelFile, dialect=cdialect)
            self.fmodelInfoList = fileReadDict  
        except IOError:
            self.fmodelInfoList = None
            raise Exception("No forward model model file found")
            
        
    def initializeModel(self):
        """
        Parse the fModelDirectory for 
        """
        
        
# class CoregistrationModel(QAbstractTableModel):
    