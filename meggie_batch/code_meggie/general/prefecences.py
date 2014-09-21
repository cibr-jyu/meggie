# coding: latin1

'''
Created on 19.9.2014

@author: Kari Aliranta

Module for code related to handling program wide preferences.
'''

import os
import ConfigParser
from cloud.util.configmanager import NoOptionError



class PreferencesHandler(object):
    '''
    Class for storing Meggie preferences and setting them into effect.
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
        self._workingDirectory = ''
        self._MNERoot = ''
        self._autoLoadLastOpenExperiment = None
        self._previousExperimentPath = ''

        self.readPreferencesFromDisk()

    def getWorkingDirectory(self):
        return self.__workingDirectory


    def getMNERoot(self):
        return self.__MNERoot


    def getAutoLoadLastOpenExperiment(self):
        return self.__autoLoadLastOpenExperiment


    def getPreviousExperimentPath(self):
        return self.__previousExperimentPath


    def setWorkingDirectory(self, value):
        self.__workingDirectory = value


    def setMNERoot(self, value):
        self.__MNERoot = value


    def setAutoLoadLastOpenExperiment(self, value):
        self.__autoLoadLastOpenExperiment = value


    def setPreviousExperimentPath(self, value):
        self.__previousExperimentPath = value


    workingDirectory = property(get_working_directory, set_working_directory, None, None)
    MNERoot = property(get_mneroot, set_mneroot, None, None)
    autoLoadLastOpenExperiment = property(get_auto_load_last_open_experiment, set_auto_load_last_open_experiment, None, None)
    previousExperimentPath = property(get_previous_experiment_path, set_previous_experiment_path, None, None)
    workingDirectory = property(getWorkingDirectory, setWorkingDirectory, None, None)
    MNERoot = property(getMNERoot, setMNERoot, None, None)
    autoLoadLastOpenExperiment = property(getAutoLoadLastOpenExperiment, setAutoLoadLastOpenExperiment, None, None)
    previousExperimentPath = property(getPreviousExperimentPath, setPreviousExperimentPath, None, None)

    """
    Pile of getters and setters for attributes.
    """
    


    
    
    
    def writePreferencesToDisk(self):
        """
        Writes the preferences to disk, in an easily readable form.
        """
        config = ConfigParser.RawConfigParser()
        config.add_section('MiscOptions')
        config.add_section('Workspace')
        config.add_section('EnvVariables')
        
        # Sanity of these values is assumed to be checked by the caller (should
        # only be preferencesDialog).
        config.set('MiscOptions', '_previousExperimentPath', 
                   self._previousExperimentPath)
        config.set('Workspace', 'workspaceDir', self._workingDirectory)           
        config.set('EnvVariables','MNERootDir', self._MNERoot)
        
        if self._autoLoadLastOpenExperiment is True:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'True')
        else:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'False')
    
        with open('preferences.cfg', 'wb') as configfile:
            config.write(configfile)
        
        
    def readPreferencesFromDisk(self):
        """
        Reads the preferences from disk into class attributes.
        """
        if os.path.isfile('preferences.cfg'):
            config = ConfigParser.RawConfigParser('preferences.cfg')
        else: return
        
        try:
            self._workingDirectory = config.get('Workspace', 'workspaceDir') 
            self._MNERoot = config.get('EnvVariables','MNERootDir')
            self._autoLoadLastOpenExperiment = config.set('MiscOptions', 
                                                'autoReloadPreviousExperiment')
            self._previousExperimentPath = config.get('MiscOptions', 
                                                     '_previousExperimentPath')
        except NoOptionError:
            return
        
        
    
    def updatePreference(self, prefName, prefValue):
        """
        Changes the desired preference 
        
        Keyword arguments:
        
        TODO: write desc.
        
        Also probably should raise exception instead of returning boolean.     
        """
        
        if prefName not in ['workDir', '_MNERoot', 'autoLoadPrevExp',
                            'prevExpPath']:
            return False
    
        if prefName is 'workDir': self._workingDirectory = prefValue
        if prefName is '_MNERoot': self._MNERoot = prefValue
        if prefName is 'autoLoadPrevExp': 
            self._autoLoadLastOpenExperiment = prefValue                                   
        if prefName is 'prevExpPath': self._previousExperimentPath = prefValue
        return True
    
    
    def setEnvVariables(self):
        """
        Set various shell environment variables needed by MNE-C scripts and
        other command line programs.
        """
        os.environ['MNE_ROOT'] = self._MNERoot
    
   
    """ 
    Keyword arguments:
        
        workingDirPath        -- path to Meggie working directory
        MNERootPath           -- path to MNE root directory
        autoLoadLastOpenExp   -- Should the previous experiment be loaded
                                 automatically when starting Meggie, or not.
                                 
                                 
     if os.path.isfile('settings.cfg'):
        configp = ConfigParser.RawConfigParser()
        configp.read('settings.cfg')
        
        if configp.has_option('_MNERoot', 'MNERootDir'):
            MNERootPath = configp.get('_MNERoot', 'MNERootDir')
            os.environ['MNE_ROOT'] = MNERootPath
    
                                 
    """ 
   
    