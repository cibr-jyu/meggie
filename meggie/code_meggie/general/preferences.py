# coding: utf-8

"""
"""

import os
import logging
import configparser

from meggie.code_meggie.utils.files import home_filepath


class PreferencesHandler(object):
    '''
    Class for storing Meggie preferences and setting them into effect.
    '''


    def __init__(self):
        '''Constructor'''
        self.working_directory = ''
        self.n_jobs = 3
        self.FreeSurferHome = ''
        self.previous_experiment_name = ''
        self.auto_load_last_open_experiment = False
        self.confirm_quit = False
        self.save_bads = False
        self.read_preferences_from_disk()

    def write_preferences_to_disk(self):
        """
        Writes the preferences to disk, in an easily readable form.
        """
        config = configparser.RawConfigParser()
        config.add_section('MiscOptions')
        config.add_section('Workspace')
        config.add_section('EnvVariables')

        # Sanity of these values is assumed to be checked by the calling method
        # (should only be preferencesDialog).
        config.set('MiscOptions', 'previous_experiment_name', 
                   self.previous_experiment_name)
        config.set('MiscOptions', 'n_jobs', self.n_jobs)       
        config.set('Workspace', 'workspaceDir', self.working_directory)
        config.set('EnvVariables', 'FreeSurferHomeDir', self.FreeSurferHome)

        if self.auto_load_last_open_experiment == True:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'True')
        else:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'False')
    
        if self.confirm_quit == True:
            config.set('MiscOptions', 'confirmQuit', 'True')
        else:
            config.set('MiscOptions', 'confirmQuit', 'False')
            
        if self.save_bads == True:
            config.set('MiscOptions', 'saveBads', 'True')
        else:
            config.set('MiscOptions', 'saveBads', 'False')

        with open(home_filepath('.meggieprefs'), 'w') as configfile:
            config.write(configfile)
        
        
    def read_preferences_from_disk(self):
        """
        Reads the preferences from disk into class attributes.
        """
        filename = home_filepath('.meggieprefs')
        if os.path.isfile(filename):
            config = configparser.RawConfigParser()
            config.read(filename)
        else: return
        
        # If some preference is not present yet, just skip it (it will be set
        # right next time). 
        try:
            self.working_directory = config.get('Workspace', 'workspaceDir') 
            self.FreeSurferHome = config.get('EnvVariables', 'FreeSurferHomeDir')
            
            # No automatic typecasting to boolean here, so have to do this.
            if config.get('MiscOptions', 'autoreloadpreviousexperiment') == 'True':
                self.auto_load_last_open_experiment = True
            else: 
                self.auto_load_last_open_experiment = False
            
            if config.get('MiscOptions', 'confirmQuit') == 'True':
                self.confirm_quit = True
            else: 
                self.confirm_quit = False
            
            if config.get('MiscOptions', 'saveBads') == 'True':
                self.save_bads = True
            else: 
                self.save_bads = False
            
            self.previous_experiment_name = config.get(
                'MiscOptions', 'previous_experiment_name')

            self.n_jobs = int(config.get('MiscOptions', 'n_jobs'))
        except configparser.NoOptionError:
            pass
            
    
    def set_env_variables(self):
        """
        """
        message = ('Setting environment variables...')
        logging.getLogger('ui_logger').info(message)

        # Set environment directly for FreeSurfer.
        if self.FreeSurferHome:
            freeSurferBinPath = os.path.join(self.FreeSurferHome, 'bin')
            freeSurferTktoolsPath = os.path.join(self.FreeSurferHome, 'tktools')
            os.environ['FREESURFER_HOME'] = self.FreeSurferHome
            os.environ['PATH'] += os.pathsep + freeSurferBinPath
            os.environ['PATH'] += os.pathsep + freeSurferTktoolsPath

        # to make graphical MNE-Python utilities 
        # use QT4 backend instead of wx.
        os.environ['ETS_TOOLKIT'] = "qt4"

