""" Contains implementation for raw measurement info
"""
from meggie.mainwindow.dynamic import InfoAction

from meggie.utilities.measurement_info import MeasurementInfo
from meggie.utilities.channels import is_montage_set


class Info(InfoAction):
    """ Shows measurement information on a info box
    """

    def run(self):

        message = ""
        try:
            subject = self.experiment.active_subject
            raw = subject.get_raw()
            mi = MeasurementInfo(raw)

            maxfilter_applied = subject.sss_applied
            ica_applied = subject.ica_applied
            rereferenced = subject.rereferenced

            try:
                eeg_montage_set = is_montage_set(raw, 'eeg')
            except Exception as exc:
                eeg_montage_set = False

            message += "Subject name: {0}\n".format(mi.subject_name)
            message += "Date: {0}\n".format(mi.date)
            message += "Length: {0:.2f} s\n".format(raw.times[-1])
            message += "Highpass: {0} Hz\n".format(mi.high_pass)
            message += "Lowpass: {0} Hz\n".format(mi.low_pass)
            message += "Sampling rate: {0} Hz\n".format(mi.sampling_freq)
            message += "Bads: " + ', '.join(raw.info['bads']) + '\n'

            message += "Maxfilter applied: {0}\n".format(str(maxfilter_applied))
            message += "ICA applied: {0}\n".format(str(ica_applied))
            message += "Rereferenced: {0}\n".format(rereferenced)
            message += "EEG montage set: {0}\n".format(eeg_montage_set)
        except Exception as exc:
            return ""

        return message
