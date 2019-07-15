# coding: utf-8

"""
"""

import datetime
import logging
import re

import meggie.code_meggie.general.mne_wrapper as mne


class MeasurementInfo(object):
    """
    A class for collecting information from MEG-measurement raw files.
    """

    def __init__(self, raw):
        """
        """
        if isinstance(raw, mne.RAW_TYPE):
            self._info = raw.info
        else:
            raise TypeError('Not a Raw object.')

    @property
    def high_pass(self):
        """
        Returns the online high pass cutoff frequency in Hz.
        Raises an exception if the field highpass does not exist.
        """
        if self._info.get('highpass') is None:
            raise Exception('Field highpass does not exist.')
        else:
            return round(self._info.get('highpass'), 2)

    @property
    def low_pass(self):
        """
        Returns the online low pass filter cutoff frequency.
        Raises an exception if the field lowpass does not exist.
        """
        if self._info.get('lowpass') is None:
            raise Exception('Field lowpass does not exist.')
        else:
            return round(self._info.get('lowpass'), 2)

    @property
    def sampling_freq(self):
        """
        returns the sampling frequency.
        """
        if self._info.get('sfreq') is None:
            raise Exception('Field sfreq does not exist.')
        else:
            return round(self._info.get('sfreq'), 2)

    @property
    def date(self):
        """
        Returns the date of measurement in form yyyy-mm-dd.
        """
        if self._info.get('meas_date') is None:
            raise Exception('Field meas_date does not exist.')
        elif not isinstance(datetime.datetime.fromtimestamp
                            (self._info.get('meas_date')[0]), datetime.datetime):
            raise TypeError('Field meas_date is not a valid timestamp.')
        else:
            d = datetime.datetime.fromtimestamp(self._info.get('meas_date')[0])
            return d.strftime('%Y-%m-%d')

    @property
    def subject_name(self):
        """
        Returns the subjects name. If some of the name fields are nonexistent
        or empty, substitutes information with emptry strings.
        """
        subj_info = self._info.get('subject_info')

        if not subj_info:
            logging.getLogger('ui_logger').debug("Personal info not found.")
            return ''

        last_name = subj_info.get('last_name', '')
        first_name = subj_info.get('first_name', '')

        return last_name + ' ' + first_name
