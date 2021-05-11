"""Provides for a class that wraps measurement information from the mne.Info.
"""

class MeasurementInfo(object):
    """A class for collecting information from raw files.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw object the measurement info is based on.
    """

    def __init__(self, raw):
        self._info = raw.info

    @property
    def high_pass(self):
        """Returns the high-pass filter value.
        """
        try:
            return round(self._info.get('highpass'), 2)
        except Exception as exc:
            pass

    @property
    def low_pass(self):
        """Returns the low-pass filter value.
        """
        try:
            return round(self._info.get('lowpass'), 2)
        except Exception as exc:
            return ""

    @property
    def sampling_freq(self):
        """Returns the sampling frequency.
        """
        try:
            return round(self._info.get('sfreq'), 2)
        except Exception as exc:
            return ""

    @property
    def date(self):
        """Returns the measurement date."""
        try:
            return str(self._info['meas_date'].date())
        except Exception as exc:
            return ""

    @property
    def subject_name(self):
        """Constructs a one-string-name."""
        subj_info = self._info.get('subject_info')

        if not subj_info:
            return ''

        last_name = subj_info.get('last_name', '')
        first_name = subj_info.get('first_name', '')

        return last_name + ' ' + first_name

