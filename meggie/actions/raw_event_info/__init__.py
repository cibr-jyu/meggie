""" Contains implementation for raw event info
"""
import numpy as np 

from meggie.mainwindow.dynamic import InfoAction
from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events


class Info(InfoAction):
    """ Shows event information on a info box.
    """

    def run(self):
        try:
            subject = self.experiment.active_subject
            if not subject:
                return ""

            raw = subject.get_raw()

            stim_ch = find_stim_channel(raw)
            if not stim_ch:
                return ""

            events = find_events(raw, stim_ch=stim_ch)
            if events is None:
                return ""

            bins = np.bincount(events[:,2])
            event_counts = dict()
            for event_id in set(events[:, 2]):
                event_counts[event_id] = bins[event_id]

            events_string = ""
            for key, value in event_counts.items():
                events_string += 'Trigger %s, %s events\n' % (str(key), str(value))

            return events_string
        except Exception as exc:
            return ""

