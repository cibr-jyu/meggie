""" Contains implementation for tfr info
"""
from meggie.mainwindow.dynamic import InfoAction

from meggie.utilities.formats import format_float
from meggie.utilities.formats import format_floats


class Info(InfoAction):
    """ Fills up tfr info box """

    def run(self):
        try:
            selected_name = self.data['outputs']['tfr'][0]

            tfr = self.experiment.active_subject.tfr[selected_name]
            params = tfr.params

            message = ""
            if 'decim' in params:
                message += 'Decimated by factor: {0}\n'.format(params['decim'])
            if 'evoked_subtracted' in params:
                message += 'Evoked subtracted: {0}\n'.format(params['evoked_subtracted'])
            if 'conditions' in params:
                message += 'Conditions: ' + ', '.join(params['conditions']) + '\n'
            if 'n_cycles' in params:
                message += 'Cycles: ' + ', '.join(format_floats(params['n_cycles'])) + '\n'

            if hasattr(tfr, 'times'):
                message += 'Times: {0}s - {1}s\n'.format(
                    format_float(tfr.times[0]), format_float(tfr.times[-1]))

            if hasattr(tfr, 'freqs'):
                message += 'Freqs: {0} - {1}\n'.format(
                    format_float(tfr.freqs[0]), format_float(tfr.freqs[-1]))

            if 'groups' in params:
                for key, names in params['groups'].items():
                    message += '\nGroup ' + str(key) + ': \n'
                    for name in names:
                        message += name + '\n'

        except Exception as exc:
            message = ""

        return message

