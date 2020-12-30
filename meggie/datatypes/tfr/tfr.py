# coding: utf-8

"""
"""

import os
import re
import logging

import mne


class TFR(object):
    """
    """

    def __init__(self, name, tfr_directory, params, content=None):
        """
        """
        self._name = name
        self._content = content
        self._params = params
        self._tfr_directory = tfr_directory

    def _get_fname(self, tfr_name):
        # for backward compatibility
        if tfr_name == '':
            name = self._name + '-tfr.h5'
        else:
            name = self._name + '-' + tfr_name + '-tfr.h5'

        fname = os.path.join(self._tfr_directory,
                             name)
        return fname

    def save_content(self):
        try:
            for tfr_name, tfr in self._content.items():
                fname = self._get_fname(tfr_name)
                tfr.save(fname, overwrite=True)
        except Exception as exc:
            logging.getLogger('ui_logger').exception(str(exc))
            raise IOError('Writing TFRs failed')

    def delete_content(self):

        # if not self._content:
        #     return
        # for tfr_name, tfr in self._content.items():
        #     fname = self._get_fname(tfr_name)
        #     os.remove(fname)

        template = self._name + '-' + r'([a-zA-Z1-9_]+)\-tfr\.h5'
        for fname in os.listdir(self._tfr_directory):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    continue

                # if proper condition parameters set,
                # check if the key is in there
                if 'conditions' in self._params:
                    if key not in [str(elem) for elem in
                                   self._params['conditions']]:
                        continue

                logging.getLogger('ui_logger').debug(
                    'Removing existing tfr file: ' + str(fname))
                os.remove(os.path.join(self._tfr_directory, fname))

    def _load_content(self):
        self._content = {}
        template = self._name + '-' + r'([a-zA-Z1-9_]+)\-tfr\.h5'
        for fname in os.listdir(self._tfr_directory):
            path = None
            if fname == self._name + '-tfr.h5':
                path = os.path.join(self._tfr_directory, fname)
                key = ''
            else:
                match = re.match(template, fname)
                if match:
                    try:
                        key = str(match.group(1))
                    except Exception as exc:
                        raise Exception("Unknown file name format.")

                    # if proper condition parameters set,
                    # check if the key is in there
                    if 'conditions' in self._params:
                        if key not in [str(elem) for elem in
                                       self._params['conditions']]:
                            continue

                    path = os.path.join(self._tfr_directory,
                                        fname)
            if path:
                logging.getLogger('ui_logger').debug(
                    'Reading tfr file: ' + str(path))

                self._content[key] = mne.time_frequency.read_tfrs(path)[0]

    @property
    def content(self):
        if self._content is None:
            self._load_content()
        return self._content

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    @property
    def name(self):
        return self._name

    @property
    def decim(self):
        return self._params.get('decim')

    @property
    def n_cycles(self):
        return self._params.get('n_cycles')

    @property
    def ch_names(self):
        return list(self.content.values())[0].info['ch_names']

    @property
    def times(self):
        return list(self.content.values())[0].times

    @property
    def freqs(self):
        return list(self.content.values())[0].freqs

    @property
    def info(self):
        return list(self.content.values())[0].info

    @property
    def evoked_subtracted(self):
        return self._params.get('evoked_subtracted')
