"""Contains a class for handling reading and storing of
global preferences such as the previous experiment and
the tab settings.
"""

import os
import configparser
import logging

from meggie.utilities.filemanager import configpath
from meggie.utilities.filemanager import datapath


class PreferencesHandler(object):
    """Class for storing and setting preferences."""

    def __init__(self, prefs_path=""):

        if prefs_path:
            self.prefs_path = prefs_path
        else:
            self.prefs_path = os.path.join(configpath(), "preferences.cfg")

        self.workspace = datapath()

        self.previous_experiment_name = ""
        self.auto_load_last_open_experiment = False
        self.active_plugins = []

        self.read_preferences_from_disk()

    def read_config(self):
        """Reads the config file from file system"""
        config = configparser.RawConfigParser()
        if os.path.isfile(self.prefs_path):
            config.read(self.prefs_path)
        return config

    def write_preferences_to_disk(self):
        """Writes the preferences to file system, in INI style."""
        # Base the new config on the old one.
        config = self.read_config()
        try:
            config.add_section("MiscOptions")
            config.add_section("Workspace")
        except configparser.DuplicateSectionError:
            pass

        # Sanity of these values is assumed to be checked by the calling method

        config.set("Workspace", "workspaceDir", self.workspace)
        logging.getLogger("ui_logger").info("Workspace: " + self.workspace)

        config.set(
            "MiscOptions", "previousExperimentName", self.previous_experiment_name
        )
        logging.getLogger("ui_logger").info(
            "Previous experiment: " + self.previous_experiment_name
        )

        if self.auto_load_last_open_experiment:
            config.set("MiscOptions", "autoReloadPreviousExperiment", "True")
        else:
            config.set("MiscOptions", "autoReloadPreviousExperiment", "False")
        logging.getLogger("ui_logger").info(
            "Auto reload previous experiment: "
            + str(self.auto_load_last_open_experiment)
        )

        config.set("MiscOptions", "activePlugins", ",".join(self.active_plugins))
        logging.getLogger("ui_logger").info(
            "Active plugins: " + str(self.active_plugins)
        )

        try:
            os.makedirs(os.path.dirname(self.prefs_path))
        except PermissionError:
            logging.getLogger("ui_logger").exception(
                "Could not save the configuration file."
            )
        except FileExistsError:
            pass

        with open(self.prefs_path, "w") as configfile:
            config.write(configfile)

    def read_preferences_from_disk(self):
        """Reads the preferences from file system into attributes."""
        config = self.read_config()

        try:
            self.workspace = config.get("Workspace", "workspaceDir")
        except Exception:
            pass

        try:
            auto_reload = config.get("MiscOptions", "autoReloadPreviousExperiment")
            if auto_reload == "True":
                self.auto_load_last_open_experiment = True
        except Exception:
            pass

        try:
            self.previous_experiment_name = config.get(
                "MiscOptions", "previousExperimentName"
            )
        except Exception:
            pass

        try:
            active_plugins = config.get("MiscOptions", "activePlugins")
            self.active_plugins = active_plugins.split(",")
        except Exception:
            pass
