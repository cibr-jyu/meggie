# coding: latin1

'''
Created on 26.6.2014

@author: kpaliran

Contains models for views in various UI components, mainly MainWindow.
TODO Also contains methods for writing the models to disk (using fileManager module).
'''

from PyQt4 import QtCore, QtGui
import os

import fileManager

class ForwardModelModel(QtCore.QAbstractTableModel):
    '''
    Model class for forward model related views in MainWindow. Please don't get
    confused by the "model" and "forward model" -
    the former is model as in model-view-controller, the latter is an MNE term. 
    
    TODO pitäis varmaan kysyä heti initialisoidessa subjectilta, onko hakemistoa
    noille forward modeleille, ja sitten asettaa self.filename siihen
    hakemistoon
    '''

    def __init__(self, experiment, parent=None):
        QtCore.QAbstractTableModel.__init__(self)
        self.fmodelsDirectory = experiment._active_subject.\
                      _forwardModels_directory
                      
        # File that includes forward model names, their parameters and 
        # corresponding files. Full path needed, hence the directory.
        
        # Actually not needed, as the model is not editable via GUI.
        self.dirty = False
        
        # Each dictionary in the list includes parameters
        self.fmodelInfoList = []
        
        # Column headers i.e. names of parameters.
        self.__headers = ['name', 'spacing', 'ico', 'surfname', 'cps', 'atlas',
                          'triang. ico', 'homog', 'innershift', 'outershift',
                          'skullshift', 'brainc', 'skullc', 'scalpc']
        
        self.initializeModel()
        
    
    def rowCount(self, parent):
        """
        The associated view should have as many rows as there are 
        forward model names.
        """
        return len(self.fmodelInfoList)
    
    
    def columnCount(self, parent):
        """
        The associated view only has one column, the one to show the name 
        of the forward model. Increase value to get more colums.
        """
        return len(self.__headers)
    
        
    def data(self, index, role):
        """
        Standard data method for the QAbstractTableModel.
        """
        if not index.isValid():
            return QtCore.QVariant()
        
        # No need to use anything else but displayrole here. 
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.fmodelInfoList[row][column]
            return value
            
        else: return QtCore.QVariant()
      
      
    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"  
      
    
    def removeRows(self, position, rows=1, parent= QtCore.QModelIndex()):
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
        """
        
        # The param files don't exist by default, so lots of trying here.
        fmdir = self.fmodelsDirectory
        
        if os.path.isdir(fmdir):
            for d in [name for name in os.listdir(fmdir)
                        if os.path.isdir(os.path.join(fmdir, name))]:
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
                
                mergedDict = dict([('fmname', d)] + sSpaceDict.items() + \
                                  wshedDict.items() + \
                                  setupFModelDict.items())
                
                # No need to crash on missing parameters files, just don't
                # try to add anything to the list.
                try:
                    fmlist = self.fmodel_dict_to_list(mergedDict)
                except:
                    continue
                
                self.fmodelInfoList.append(fmlist)


    def fmodel_dict_to_list(self, fmdict):
        """
        TODO: desc
        """
        
        fmList = []
        
        # TODO: compartModel and decimMethod need some shortening
        fmList.append(fmdict['fmname'])
        fmList.append(fmdict['spacing'])
        fmList.append(fmdict['surfaceDecimMethod'])
        fmList.append(fmdict['surfaceDecimValue'])
        fmList.append(fmdict['surfaceName'])
        fmList.append(fmdict['computeCorticalStats'])
        fmList.append(fmdict['useAtlas'])
        fmList.append(fmdict['triangFilesIco'])
        fmList.append(fmdict['compartModel'])
        fmList.append(fmdict['innerShift'])
        fmList.append(fmdict['outerShift'])
        fmList.append(fmdict['skullShift'])
        fmList.append(fmdict['brainc'])
        fmList.append(fmdict['skullc'])
        fmList.append(fmdict['scalpc'])
        
        return fmList
        

# class CoregistrationModel(QAbstractTableModel):
    