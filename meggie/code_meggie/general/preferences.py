# coding: utf-8

'''
Created on 19.9.2014

@author: Kari Aliranta

Module for code related to handling program wide preferences.
'''

import os
import ConfigParser
from ConfigParser import NoOptionError
from meggie.code_meggie.utils.files import home_filepath


class PreferencesHandler(object):
    '''
    Class for storing Meggie preferences and setting them into effect.
    '''


    def __init__(self):
        '''Constructor'''
        self.working_directory = ''
        self.n_jobs = 3
        self.MNERoot = ''
        self.FreeSurferHome = ''
        self.auto_load_last_open_experiment = False
        self.previous_experiment_name = ''
        self.confirm_quit = False
        self.read_preferences_from_disk()

    def write_preferences_to_disk(self):
        """
        Writes the preferences to disk, in an easily readable form.
        """
        config = ConfigParser.RawConfigParser()
        config.add_section('MiscOptions')
        config.add_section('Workspace')
        config.add_section('EnvVariables')

        # Sanity of these values is assumed to be checked by the calling method
        # (should only be preferencesDialog).
        config.set('MiscOptions', 'previous_experiment_name', 
                   self.previous_experiment_name)
        config.set('MiscOptions', 'n_jobs', self.n_jobs)       
        config.set('Workspace', 'workspaceDir', self.working_directory)
        config.set('EnvVariables','MNERootDir', self.MNERoot)
        config.set('EnvVariables', 'FreeSurferHomeDir', self.FreeSurferHome)

        if self.auto_load_last_open_experiment == True:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'True')
        else:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'False')
    
        if self.confirm_quit == True:
            config.set('MiscOptions', 'confirmQuit', 'True')
        else:
            config.set('MiscOptions', 'confirmQuit', 'False')

        with open(home_filepath('.meggieprefs'), 'wb') as configfile:
            config.write(configfile)
        
        
    def read_preferences_from_disk(self):
        """
        Reads the preferences from disk into class attributes.
        """
        filename = home_filepath('.meggieprefs')
        if os.path.isfile(filename):
            config = ConfigParser.RawConfigParser()
            config.read(filename)
        else: return
        
        # If some preference is not present yet, just skip it (it will be set
        # right next time). 
        try:
            self.working_directory = config.get('Workspace', 'workspaceDir') 
            self.MNERoot = config.get('EnvVariables','MNERootDir')
            self.FreeSurferHome = config.get('EnvVariables', 'FreeSurferHomeDir')
            
            # No automatic typecasting to boolean here, so have to do this.
            if config.get('MiscOptions', 'autoreloadpreviousexperiment') == 'True':
                self.auto_load_last_open_experiment = True
            else: self.auto_load_last_open_experiment = False
            
            if config.get('MiscOptions', 'confirmQuit') == 'True':
                self.confirm_quit = True
            else: self.confirm_quit = False
            
            self.previous_experiment_name = config.get('MiscOptions', 
                                                     'previous_experiment_name')
            self.n_jobs = int(config.get('MiscOptions', 'n_jobs'))
        except NoOptionError:
            pass
            
    
    def set_env_variables(self):
        """
        Set various shell environment variables needed by MNE-C scripts and
        FreeSurfer.
        """
        print 'Meggie: setting environment variables needed by MNE and ' + \
              'Freesurfer ... \n'

        os.environ['MNE_ROOT'] = self.MNERoot

        # Let's set stuff that mne_setup_sh and mne_setup usually handle, to
        # avoid problems with different shells and passing env variables around
        # to subprocesses.
        mneBinPath = os.path.join(self.MNERoot, 'bin')
        mneLibPath = os.path.join(self.MNERoot, 'lib')
        mneUserFileSearchPath = os.path.join(self.MNERoot,
                                             'share/app-defaults/%N')
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

        # Also set environment directly for FreeSurfer.
        freeSurferBinPath = os.path.join(self.FreeSurferHome, 'bin')
        freeSurferTktoolsPath = os.path.join(self.FreeSurferHome, 'tktools')
        os.environ['FREESURFER_HOME'] = self.FreeSurferHome
        os.environ['PATH'] += os.pathsep + freeSurferBinPath
        os.environ['PATH'] += os.pathsep + freeSurferTktoolsPath

        # To make graphical MNE-Python utilities use QT4 backend instead of wx.
        os.environ['ETS_TOOLKIT'] = "qt4"

        print 'Meggie: environment variables set successfully! \n'
