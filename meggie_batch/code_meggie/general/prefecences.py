# coding: latin1

'''
Created on 19.9.2014

@author: Kari Aliranta

Module for code related to handling program wide preferences.
'''

import os
import ConfigParser
from ConfigParser import NoOptionError
import subprocess


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
        self._auto_load_last_open_experiment = False
        self._previous_experiment_name = ''

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
        config.set('MiscOptions', 'previous_experiment_name', 
                   self._previous_experiment_name)
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
            config = ConfigParser.RawConfigParser()
            config.read('preferences.cfg')
        else: return
        
        # If some preference is not present, just skip it (no exception
        # handling present).
        self._working_directory = config.get('Workspace', 'workspaceDir') 
        self._MNERoot = config.get('EnvVariables','MNERootDir')
        
        # No automatic typecasting to boolean here, so have to do this.
        if config.get('MiscOptions', 'autoreloadpreviousexperiment') == 'True':
            self._auto_load_last_open_experiment = True
        else: self._auto_load_last_open_experiment = False
        
        self._previous_experiment_name = config.get('MiscOptions', 
                                                 'previous_experiment_name')
    
    
    def set_env_variables(self):
        """
        Set various shell environment variables
        needed by MNE-C scripts and other command line programs.
        """
        
        print 'Meggie: setting environment variables needed by MNE and ' + \
              'Freesurfer ... \n'
        
        # TODO: check that this actually is right (in pref. dialog?) 
        # and alert user if not
        os.environ['MNE_ROOT'] = self._MNERoot
        
        # Let's set stuff that mne_setup_sh and mne_setup usually handle, to
        # avoid problems with different shells and passing env variables around
        # to subprocesses.
        mneBinPath = os.path.join(self._MNERoot, 'bin')
        mneLibPath = os.path.join(self._MNERoot, 'lib')
        mneUserFileSearchPath = os.path.join(self._MNERoot, 'share/app-defaults/%N')
        os.environ['PATH'] += os.pathsep + mneBinPath
        
        if os.environ.get('LD_LIBRARY_PATH') == None:
            os.environ['LD_LIBRARY_PATH'] = mneLibPath
        else:
            os.environ['LD_LIBRARY_PATH'] += os.pathsep + mneLibPath
        
        if os.environ.get('XUSERFILESEARCHPATH') == None:
            os.environ['XUSERFILESEARCHPATH'] = mneUserFileSearchPath
        else:
            os.environ['XUSERFILESEARCHPATH'] += os.pathsep + \
                                                 mneUserFileSearchPath
        
        print 'Meggie: environment variables set succesfully! \n'