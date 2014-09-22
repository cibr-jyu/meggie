# coding: latin1

'''
Created on 19.9.2014

@author: Kari Aliranta

Module for code related to handling program wide preferences.
'''

import os
import ConfigParser
from ConfigParser import NoOptionError


class PreferencesHandler(object):
    '''
    Class for storing Meggie preferences and setting them into effect.
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
        self._working_directory = ''
        self._MNERoot = ''
        self._auto_load_last_open_experiment = None
        self._previous_experiment_path = ''

        self.readPreferencesFromDisk()
    

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
        config.set('MiscOptions', '_previous_experiment_path', 
                   self._previous_experiment_path)
        config.set('Workspace', 'workspaceDir', self._working_directory)           
        config.set('EnvVariables','MNERootDir', self._MNERoot)
        
        if self._auto_load_last_open_experiment is True:
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
        
        # If some preference is not present, just skip it (no exception
        # handling present).
        self._working_directory = config.get('Workspace', 'workspaceDir') 
        self._MNERoot = config.get('EnvVariables','MNERootDir')
        self._auto_load_last_open_experiment = config.set('MiscOptions', 
                                            'autoReloadPreviousExperiment')
        self._previous_experiment_path = config.get('MiscOptions', 
                                                 '_previous_experiment_path')
        
    
    def updatePreference(self, prefName, prefValue):
        """
        Changes the desired preference into value given. 
        
        Keyword arguments:
        
        TODO: write desc.
        
        TODO: Also probably should raise exception instead of returning boolean,
        but currently foreseeable preferences don't cause anything critical
        if not set.     
        """
        
        if prefName not in ['workDir', '_MNERoot', 'autoLoadPrevExp',
                            'prevExpPath']:
            return False
    
        if prefName is 'workDir': self._working_directory = prefValue
        if prefName is '_MNERoot': self._MNERoot = prefValue
        if prefName is 'autoLoadPrevExp': 
            self._auto_load_last_open_experiment = prefValue                                   
        if prefName is 'prevExpPath': self._previous_experiment_path = prefValue
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
   
    