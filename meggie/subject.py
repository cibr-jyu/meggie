# coding: utf-8

"""
"""

import os
import json
import shutil
import glob
import pkg_resources

import numpy as np

import meggie.utilities.filemanager as filemanager

from meggie.utilities.events import Events


class Subject(object):

    def __init__(self, experiment, name, raw_fname,
                 ica_applied=False, rereferenced=False):
        """
        """
        self.name = name
        self.raw_fname = raw_fname

        self._raw = None

        self.ica_applied = ica_applied
        self.rereferenced = rereferenced

        self.path = os.path.join(experiment.workspace,
                                 experiment.name,
                                 name)

        datatype_path = pkg_resources.resource_filename('meggie', 'datatypes')
        for package in os.listdir(datatype_path):
            config_path = os.path.join(
                datatype_path, package, 'configuration.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    datatype = config['id']
                    dir_ = config['dir']

                    # for example: self.epochs
                    setattr(self, datatype, dict())
                    # for example: self.epochs_directory
                    setattr(self, datatype + '_directory',
                            os.path.join(self.path, dir_))

    def add(self, dataobject, datatype):
        container = getattr(self, datatype)
        name = dataobject.name
        container[name] = dataobject

    def remove(self, name, datatype):
        container = getattr(self, datatype)
        dataobject = container.pop(name, None)
        try:
            dataobject.delete_content()
        except Exception:
            raise IOError('Could not delete ' + str(datatype) +
                          ' from folders')

    @property
    def raw_path(self):
        path = os.path.join(self.path,
                            self.raw_fname)
        return path

    def get_raw(self, preload=True):
        if self._raw is not None:
            if preload:
                self._raw.load_data()
            return self._raw
        else:
            try:
                raw = filemanager.open_raw(self.raw_path, preload=preload)
            except OSError:
                raise IOError("Couldn't find raw file.")
            self._raw = raw

            return raw

    def save(self):
        filemanager.save_raw(self._raw, self.raw_path)

    def release_memory(self):
        """
        """
        if self._raw is not None:
            self._raw = None

    def check_sss_applied(self):
        """
        Checks the subject folder for sss/tsss applied file.
        Returns True if sss/tsss found.
        """

        raw = self.get_raw()
        for item in raw.info['proc_history']:
            if 'maxfilter' in item.get('creator', []):
                return True

        return False

    def ensure_folders(self):

        paths = []
        datatype_path = pkg_resources.resource_filename('meggie', 'datatypes')
        for package in os.listdir(datatype_path):
            config_path = os.path.join(datatype_path, package,
                                       'configuration.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    datatype = config['id']
                    path = getattr(self, datatype + '_directory')
                    paths.append(path)

        try:
            filemanager.ensure_folders(
                [self.path] + paths)
        except OSError:
            raise OSError("Couldn't create all the necessary folders. "
                          "Do you have the necessary permissions?")
