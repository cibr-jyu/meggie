# coding: utf-8

import numpy as np

from meggie.utilities.events import update_stim_channel


def events_from_annotations(subject, conversion_info):
    """ convert annotations to events and add merge them with the stim channel
    """

    raw = subject.get_raw()

    events = []
    for annotation_name, event_id, use_start in conversion_info:
        for idx, annot_desc in enumerate(raw.annotations.description):
            if annot_desc != annotation_name:
                continue

            if use_start:
                onset_time = raw.annotations.onset[idx]
            else:
                onset_time = (raw.annotations.onset[idx] + 
                              raw.annotations.duration[idx])

            tidx = int(onset_time*raw.info['sfreq'])

            events.append([tidx, 0, event_id])

    events = np.array(sorted(events, key=lambda x: x[0]))

    update_stim_channel(raw, events)

