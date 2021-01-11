import os
import logging
import configparser

from meggie.utilities.filemanager import homepath


class PreferencesHandler(object):
    """ Class for storing and setting preferences
    """

    def __init__(self):
        """
        """
        self.prefs_path = ""
        self.workspace = ""
        self.previous_experiment_name = ""
        self.auto_load_last_open_experiment = False
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
        config.add_section('Tabs')

        # Sanity of these values is assumed to be checked by the calling method
        config.set('MiscOptions', 'previousExperimentName',
                   self.previous_experiment_name)
        config.set('Workspace', 'workspaceDir', self.workspace)

        if self.auto_load_last_open_experiment:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'True')
        else:
            config.set('MiscOptions', 'autoReloadPreviousExperiment', 'False')

        if self.save_bads:
            config.set('MiscOptions', 'saveBads', 'True')
        else:
            config.set('MiscOptions', 'saveBads', 'False')

        config.set('Tabs', 'enabledTabs', ','.join(self.enabled_tabs or []))
        config.set('Tabs', 'preset', self.tab_preset)

        path = self.prefs_path
        if not path:
            path = os.path.join(homepath(), '.meggieprefs')

        with open(path, 'w') as configfile:
            config.write(configfile)

    def read_preferences_from_disk(self):
        """
        Reads the preferences from disk into class attributes.
        """
        filename = os.path.join(homepath(), '.meggieprefs')
        if os.path.isfile(filename):
            config = configparser.RawConfigParser()
            config.read(filename)

        try:
            self.workspace = config.get('Workspace', 'workspaceDir')
        except Exception as exc:
            self.workspace = ''

        try:
            if config.get('MiscOptions',
                          'autoreloadpreviousexperiment') == 'True':
                self.auto_load_last_open_experiment = True
            else:
                self.auto_load_last_open_experiment = False
        except Exception as exc:
            self.auto_load_last_open_experiment = False

        try:
            self.previous_experiment_name = config.get(
                'MiscOptions', 'previousExperimentName')
        except Exception as exc:
            self.previous_experiment_name = ''

        try:
            self.enabled_tabs = config.get('Tabs', 'enabledTabs')
            self.enabled_tabs = self.enabled_tabs.split(',')
        except Exception as exc:
            self.enabled_tabs = ''
        try:
            self.tab_preset = config.get('Tabs', 'preset')
        except Exception as exc:
            self.tab_preset = ''

