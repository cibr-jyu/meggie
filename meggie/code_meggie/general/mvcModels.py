# coding: utf-8

'''
Created on 26.6.2014

@author: kpaliran

Contains models for views in various UI components, mainly MainWindow.
'''

from PyQt4 import QtCore
from PyQt4.QtGui import QFont
import os

from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import fileManager


class ForwardModelModel(QtCore.QAbstractTableModel):
    """
    Model class for forward model related views in MainWindow. Please don't get
    confused by the "model" and "forward model" -
    the former is model as in model-view-controller, the latter is an MNE term.
    """
    caller = Caller.Instance()

    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self)
        self.parent = parent
        
        # Each dictionary in the list includes parameters for single forward
        # model.
        self.fmodelInfoList = []
        
        # Column headers i.e. names of parameters.
        self.__headers = ['name', 'decim. method' , 'spacing', 'ico value', 
                          'surfname', 'cps', 'atlas', 'triang. ico', 'homog',
                          'innershift','outershift','skullshift', 'brainc',
                          'skullc', 'scalpc', 'coregistered', 'fsolution',
                          'includeMEG', 'includeEEG', 'minDist', 'ignoreRef']

        # May well be None, if no experiment is loaded.
        if self.caller.experiment == None:
            return
        
        self._fmodels_directory = None
        
        # The experiment may not have an active subject, no need to try to
        # initialize model in that case.
        try:
            self._fmodels_directory = self.caller._experiment._active_subject.\
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
    
        
    def data(self, index, role=QtCore.Qt.DisplayRole):
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
        Removal of a single row from the model.
        """
        self.beginRemoveRows(parent, position, position + rows - 1)
        singleFMitem = self.fmodelInfoList[position]
        self.fmodelInfoList.remove(singleFMitem)
        self.endRemoveRows()
            
        
    def initialize_model(self):
        """
        Reads the active subject's forwardModels directory and populates the
        data accordingly.
        """
        activeSubject = self.caller._experiment._active_subject
        if activeSubject == None:
            self._fmodels_directory = None
            self.layoutAboutToBeChanged.emit()
            del self.fmodelInfoList[:]
            self.layoutChanged.emit()
            return
        
        self._fmodels_directory = activeSubject._forwardModels_directory
        fmsdir = self._fmodels_directory
        
        self.layoutAboutToBeChanged.emit()
        
        # Best to empty the list anyway, otherwise the forward models 
        # from the previous active subject end up staying there.
        del self.fmodelInfoList[:]
            
        for d in [name for name in os.listdir(fmsdir)
                    if os.path.isdir(os.path.join(fmsdir, name))]:
            
            pmlist = self.create_single_FM_param_list(fmsdir, d)                
            self.fmodelInfoList.append(pmlist)

        self.layoutChanged.emit()
        
        
    def create_single_FM_param_list(self, fmdir, fmname):
        """
        Creates a list of parameters corresponding to a single forward model.
        
        Keyword arguments:
        fmdir       -- the directory the forward models are located at.
        fmname      -- the name of the forward model.
        
        Returns the list, or None if there is no such model.
        
        """ 
        
        # The param files don't exist by default, so lots of trying here.
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
        
        fmList.append(fmdict['surfaceDecimMethod'])
        
        if fmdict['surfaceDecimMethod'] == 'traditional (default)':
            fmList.append(fmdict['spacing'])
        else: fmList.append('--')
        
        if fmdict['surfaceDecimMethod'] == 'traditional (default)':
            fmList.append('--')
        else: fmList.append(fmdict['surfaceDecimValue'])
        
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
        
        
        
class SubjectListModel(QtCore.QAbstractListModel):
    """
    Simple model class for storing data for subject lists.
    """
    caller = Caller.Instance()
    
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self)
        self.parent = parent
        
        # Each dictionary in the list includes name of a single subject. 
        self.subjectNameList = []
        self.initialize_model()
    
    
    def rowCount(self, parent):
        """
        The associated view should have as many rows as there are 
        subject names.
        """
        return len(self.subjectNameList)
    
        
    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Standard data method for the QAbstractListModel.
        """
        if not index.isValid():
            return QtCore.QVariant()
        
        try:
            activeSubjectName = self.caller._experiment._active_subject.\
            _subject_name
        except Exception as e:
            activeSubjectName = None
         
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            value = self.subjectNameList[row]
            return value
                            
        if role == QtCore.Qt.FontRole:  
            row = index.row()
            subjectName = self.subjectNameList[row]
            if activeSubjectName != None:
                if subjectName == activeSubjectName:
                    itemFont = QFont('defaultFamily')
                    itemFont.setBold(True)
                    return itemFont
            else:
                return None
                
    
    def removeRows(self, position, rows=1, parent= QtCore.QModelIndex()):
        """
        Removal of a single row from the model.
        """
        self.beginRemoveRows(parent, position, position + rows - 1)
        singleItem = self.subjectNameList[position]
        self.subjectNameList.remove(singleItem)
        self.endRemoveRows()
        
    
    def initialize_model(self):
        """
        Reads the experiment directory and populates the
        subjectNameList accordingly.
        """
        self.layoutAboutToBeChanged.emit()
        del self.subjectNameList[:]
        
        if self.caller.experiment == None:
            self.layoutChanged.emit()
            return
        
        subjects = self.caller.experiment.get_subjects()
        
        if len(subjects) > 0:
            for subject in subjects:
                self.subjectNameList.append(subject.subject_name)
        self.layoutChanged.emit()
        
