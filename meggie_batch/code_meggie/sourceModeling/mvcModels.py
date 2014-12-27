# coding: latin1

'''
Created on 26.6.2014

@author: kpaliran

Contains models for views in various UI components, mainly MainWindow.
TODO Also contains methods for writing the models to disk (using fileManager module).
'''

from PyQt4 import QtCore
import os

import fileManager

class ForwardModelModel(QtCore.QAbstractTableModel):
    """
    Model class for forward model related views in MainWindow. Please don't get
    confused by the "model" and "forward model" -
    the former is model as in model-view-controller, the latter is an MNE term. 
    
    TODO pitäis varmaan kysyä heti initialisoidessa subjectilta, onko hakemistoa
    noille forward modeleille, ja sitten asettaa self.filename siihen
    hakemistoon
    """

    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self)
        self.parent = parent
        
        # Each dictionary in the list includes parameters for single forward
        # model.
        self.fmodelInfoList = []
        
        # Column headers i.e. names of parameters.
        self.__headers = ['name', 'spacing', 'ico', 'decimvalue', 'surfname',
                          'cps', 'atlas', 'triang. ico', 'homog', 'innershift',
                          'outershift','skullshift', 'brainc', 'skullc',
                          'scalpc', 'coregistered', 'fsolution', 'includeMEG',
                          'includeEEG', 'minDist', 'ignoreRef']

        # May well be None, if no experiment is loaded.
        if self.parent._experiment == None:
            return
        
        self._fmodels_directory = None
        
        # The experiment may not have an active subject, no need to try to
        # initialize model in that case.
        try:
            self._fmodels_directory = self.parent._experiment._active_subject.\
                      _forwardModels_directory
        except AttributeError:
            return
        
        self.initialize_model()
    
    
    def rowCount(self, parent):
        """
        The associated view should have as many rows as there are 
        forward model names.
        """
        return len(self.fmodelInfoList)
    
    
    def columnCount(self, parent):
        """
        The associated view should have as many columns as there are 
        header fields, if we want to show all information.
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
      
      
    def headerData(self, section, orientation, role):
        
        if role == QtCore.Qt.DisplayRole:
            
            if orientation == QtCore.Qt.Horizontal:
                
                if section < len(self.__headers):
                    return self.__headers[section]
                else:
                    return "not implemented"  
      
    
    def removeRows(self, position, rows=1, parent= QtCore.QModelIndex()):
        """
        Removal of a single row from the model. Also removes the corresponding
        directory from the disk.
        """
        self.beginRemoveRows(parent, position, position + rows - 1)
        singleFMitem = self.fmodelInfoList[position]
        
        subject = self.parent._experiment._active_subject
        fmname = singleFMitem[0]
        
        try:
            fileManager.remove_fModel_directory(fmname, subject)
            self.fmodelInfoList.remove(singleFMitem)
        except Exception: raise
        self.endRemoveRows()
            
        
    def initialize_model(self):
        """
        Reads the active subject's forwardModels directory and populates the
        data accordingly.
        """
        
        # This mostly checks whether or not there is an active subject.    
        if self.parent._experiment._active_subject == None:
            self._fmodels_directory = None
            del self.fmodelInfoList[:]
            self.layoutAboutToBeChanged.emit()
            self.layoutChanged.emit()
            return
        
        self._fmodels_directory = self.parent._experiment._active_subject.\
                      _forwardModels_directory
        fmsdir = self._fmodels_directory
        
        """
        # This really should not need checking nowadays, just exists for 
        # handling old style subject directories. 
        if not os.path.isdir(fmsdir):
            self._fmodels_directory = None
            del self.fmodelInfoList[:]
            self.layoutAboutToBeChanged.emit()
            self.layoutChanged.emit()
            return
        """
            
        # Best to empty the list anyway, otherwise the forward models 
        # from the previous active subject end up staying there.
        del self.fmodelInfoList[:]
            
        # The param files don't exist by default, so lots of trying here.
        for d in [name for name in os.listdir(fmsdir)
                    if os.path.isdir(os.path.join(fmsdir, name))]:
            
            pmlist = self.create_single_FM_param_list(fmsdir, d)                
            self.fmodelInfoList.append(pmlist)

        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()
        
        
    def create_single_FM_param_list(self, fmdir, fmname):
        """
        Creates a list of parameters corresponding to a single forward model.
        
        Keyword arguments:
        fmdir       -- the directory the forward models are located at.
        fmname      -- the name of the forward model.
        
        Returns the list, or None if there is no such model.
        
        """ 
        try: 
            sSpaceDict = fileManager.unpickle(os.path.join(fmdir, fmname, 
                                              'setupSourceSpace.param'))
        except Exception:
            sSpaceDict = dict()
            
        try:
            wshedDict = fileManager.unpickle(os.path.join(fmdir, fmname,
                                         'wshed.param'))
        except Exception:
            wshedDict = dict()
            
        try:
            setupFModelDict = fileManager.unpickle(os.path.join(fmdir, fmname, 
                                               'setupFModel.param'))
        except Exception:
            setupFModelDict = dict()
        
        try:
            fSolDict = fileManager.unpickle(os.path.join(fmdir, fmname, 
                                                         'fSolution.param'))
        except Exception:
            fSolDict = dict()
        
        # Check if forward model has coregistration and forward solution
        # files present (allows manual import of both from outside Meggie).
        transFilePath = os.path.join(fmdir, fmname, 'reconFiles', 
                                    'reconFiles-trans.fif')
        
        if os.path.isfile(transFilePath):
            isCoreg = 'yes'
        else:
            isCoreg = 'no'
        
        fsolFilePath = os.path.join(fmdir, fmname, 'reconFiles',
                                    'reconFiles-fwd.fif')
        
        if os.path.isfile(fsolFilePath):
            isFsol = 'yes'
        else:
            isFsol = 'no'
        
        mergedDict = dict([('fmname', fmname)] + sSpaceDict.items() + \
                          wshedDict.items() + \
                          setupFModelDict.items() + \
                          fSolDict.items() + \
                          [('coregistered', isCoreg)] + [('fsolution', isFsol)])
        
        # No need to crash on missing forward model parameters files, just don't
        # try to add anything to the list.
        try:
            fmDictList = self.fmodel_dict_to_list(mergedDict)
            return fmDictList
        except Exception:
            return None
    

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
        fmList.append(fmdict['coregistered'])
        fmList.append(fmdict['fsolution'])
        
        # If there are no forward solution parameters, add dummy ones.
        try:
            fmList.append(fmdict['includeMEG'])
        except Exception:
            fmList.append('--')
            
        try:
            fmList.append(fmdict['includeEEG'])
        except Exception:
            fmList.append('--')
        
        try:
            fmList.append(fmdict['mindist'])
        except Exception:
            fmList.append('--')
         
        try:   
            fmList.append(fmdict['ignoreref'])
        except Exception:
            fmList.append('--')
        
        return fmList
       
        
    def add_fmodel(self, fmlist):
        self.layoutAboutToBeChanged.emit()
        self.fmodelInfoList.append(fmlist)
        self.layoutChanged.emit()
        
        
        
# class CoregistrationModel(QAbstractTableModel):
    