""" Contains implementation for epochs info
"""
from meggie.mainwindow.dynamic import InfoAction

from meggie.utilities.formats import format_float


class Info(InfoAction):
    """ Fills up epochs info box """

    def run(self):

        try:
            selected_name = self.data['outputs']['epochs'][0]

            epochs = self.experiment.active_subject.epochs[selected_name]
            params = epochs.params

            message = ""

            message += "Name: {0}\n\n".format(epochs.name)

            message += "Count: {0}\n".format(epochs.count)

            message += 'Baseline: {0}s - {1}s\n'.format(format_float(params['bstart']),
                                                        format_float(params['bend']))
            message += 'Times: {0}s - {1}s\n'.format(format_float(params['tmin']),
                                                     format_float(params['tmax']))

            message += '\nReject params: \n'
            if 'grad' in params:
                message += 'Gradiometers: {}\n'.format(params.get('reject').get('grad'))
            if 'mag' in params:
                message += 'Magnetometers: {}\n'.format(params.get('reject').get('mag'))
            if 'eeg' in params:
                message += 'EEG: {}\n'.format(params.get('reject').get('eeg'))

            if 'events' in params:
                message += '\nCreated from events: \n'
                for event in params.get('events'):
                    message += 'ID: {0}, mask: {1}\n'.format(event['event_id'],
                                                             event['mask'])

        except Exception as exc:
            message = ""

        return message


