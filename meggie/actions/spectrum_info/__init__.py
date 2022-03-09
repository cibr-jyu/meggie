""" Contains implementation for spectrum info
"""
from meggie.mainwindow.dynamic import InfoAction

from meggie.utilities.formats import format_float


class Info(InfoAction):
    """ Fills up spectrum info box """

    def run(self):
        try:
            selected_name = self.data['outputs']['spectrum'][0]

            spectrum = self.experiment.active_subject.spectrum[selected_name]
            params = spectrum.params

            message = ""

            message += "Name: "+ spectrum.name + "\n\n"

            if 'fmin' in params and 'fmax' in params:
                message += 'Frequencies: {0}Hz - {1}Hz\n'.format(format_float(params['fmin']),
                                                                 format_float(params['fmax']))

            if 'nfft' in params:
                message += 'Window length (samples): {0}\n'.format(params['nfft'])


            if 'overlap' in params:
                message += 'Overlap (samples): {0}\n'.format(params['overlap'])

            if 'intervals' in params:
                message += '\nIntervals: \n'
                for key, ivals in params['intervals'].items():
                    message += 'Condition ' + str(key) + ': '
                    message += ', '.join(['({0}s - {1}s)'.format(format_float(ival[0]), format_float(ival[1]))
                                          for ival in ivals])
                    message += '\n'

            if 'groups' in params:
                for key, names in params['groups'].items():
                    message += '\nGroup ' + str(key) + ': \n'
                    for name in names:
                        message += name + '\n'

        except Exception as exc:
            message = ""

        return message
