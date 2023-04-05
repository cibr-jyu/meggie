""" Contains useful functions for handling events.
"""

import logging

import numpy as np
import mne

from collections import OrderedDict


def _should_take(id_, mask, event):
    """Check if event has same non-masked bits as id_.
    """
    id_bin = '{0:016b}'.format(id_)
    mask_bin = '{0:016b}'.format(mask)
    event_bin = '{0:016b}'.format(event[2])

    take_event = True
    for i in range(len(mask_bin)):
        if int(mask_bin[i]) == 1:
            continue
        if int(id_bin[i]) != int(event_bin[i]):
            take_event = False
            break

    return take_event


def find_events(raw, stim_ch=None, mask=0, id_=None):
    """Finds events using mne.find_events, but implements
    own masking procedure.

    The masking procedure is simple. Event is ok if it has the same
    bits as the id everywhere where the mask is zero. Thus mask 
    specifies bits that are not cared about.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw object.
    stim_ch : str
        Name of the stimulus channel.
    mask : int
        The mask as integer, is converted to binary representation.
    id_ : int
        The id as integer, is converted to binary representation.

    Returns
    -------
    np.array
        MNE-style events array, i.e. np.array of shape (n_events, 3).

    """

    events = mne.find_events(raw, stim_channel=stim_ch, shortest_event=1,
                             uint_cast=True)

    if mask or id_:
        events = list(filter(
            lambda event: _should_take(id_, mask, event), events))
        events = np.array(events)

    # remove spurious events (only one sample difference to next event)
    counter = 0
    for idx in reversed(range(1, len(events))):
        if events[idx][0] - events[idx - 1][0] < 2:
            events = np.delete(events, idx - 1, axis=0)
            counter += 1

    if counter > 0:
        message = (str(counter) +
                   " events dropped because they seem spurious "
                   "(only one sample difference to next event). "
                   "This is normal and should not be worried about.")
        logging.getLogger('ui_logger').warning(message)

    return events


def find_stim_channel(raw):
    """ Finds the appropriate stim channel from raw.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw object

    Returns
    -------
    str
        Channel name of the stimulus channel.
    """

    # Use mne's own function to find out the stim channel
    try:
        return mne.utils.config._get_stim_channel(None, raw.info)[0]
    except Exception as exc:
        pass


def update_stim_channel(raw, events):
    """Writes events to the stimulus channel.

    If no stimulus channel, create one, and then write.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw object.
    events : np.array
        MNE-style events array.
    """
    # time on in samples
    length = 5

    stim_channel = find_stim_channel(raw)

    if not stim_channel:
        # create stim_channel
        info = mne.create_info(['STI101'], raw.info['sfreq'], ['stim'])
        stim_raw = mne.io.RawArray(np.zeros((1, len(raw.times))), info)
        raw.add_channels([stim_raw], force_update_info=True)
        stim_channel = 'STI101'

    ch_idx = raw.info['ch_names'].index(stim_channel)
    for event in events:
        start = event[0] - raw.first_samp
        raw._data[ch_idx][start:start+length] = event[2]


def events_from_annotations(subject, conversion_info):
    """Convert annotations to events and merge them with the stim channel.

    Parameters
    ----------
    subject : meggie.subject.Subject
        The subject to do the conversion.
    conversion_info : list
        List of tuples like (annotation_name, event_id, use_start),
        where use_start is a boolean and False means end of the annotation.
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


def _find_event_times(raw, event_id, mask):
    """Given the event_id and mask, find the event times.
    """
    stim_ch = find_stim_channel(raw)
    sfreq = raw.info['sfreq']

    events = find_events(raw, stim_ch, mask, event_id)
    times = [(event[0] - raw.first_samp) / sfreq for event in events]
    return times


def get_raw_blocks_from_intervals(subject, intervals):
    """ Creates RawAarrays from time interval specifications.

    Parameters
    ----------
    subject : meggie.subject.Subject
        The subject whose raw data is used.
    intervals : list
        List of time interval specifications like (type, (group, tmin, tmax)),
        where type can be 'dynamic' or 'fixed' and group is a str.

    Returns
    -------
    OrderedDict
        Times of the intervals organized by average groups.
    OrderedDict
        RawArrays organized by average groups.

    """
    raw = subject.get_raw()

    raw_times = raw.times.copy()

    raw_blocks = OrderedDict()
    times = OrderedDict()
    for ival_type, (avg_group, start, end) in intervals:
        if avg_group not in raw_blocks:
            raw_blocks[avg_group] = []
            times[avg_group] = []

        if ival_type == 'fixed':
            block = raw.copy().crop(tmin=start, tmax=end)
            raw_blocks[avg_group].append(block)
            times[avg_group].append((start, end))
        else:
            # the following code finds all start points of intervals by events or
            # start of recording. then matching end point is found by
            # (can be same) other events or end of recording.
            if start[0] == 'events':
                start_times = _find_event_times(raw, start[1], start[2])
            elif start[0] == 'start':
                start_times = [raw_times[0]]
            elif start[0] == 'end':
                start_times = [raw_times[-1]]

            for start_time in start_times:
                if end[0] == 'events':
                    end_times = _find_event_times(raw, end[1], end[2])
                    found = False
                    for end_time in end_times:
                        # use equality so that one can also specify same trigger for
                        # start and end (with different offsets)

                        # sanity check
                        if np.isclose((end_time + end[3]) - (start_time + start[3]), 0):
                            continue

                        if end_time >= start_time:
                            found = True
                            break
                    if not found:
                        logging.getLogger('ui_logger').info(
                            'Found start event with no matching end event')
                        continue
                elif end[0] == 'start':
                    end_time = raw_times[0]
                elif end[0] == 'end':
                    end_time = raw_times[-1]

                # crop with offsets
                times[avg_group].append((start_time + start[3],
                                         end_time + end[3]))
                block = raw.copy().crop(tmin=(start_time + start[3]),
                                        tmax=(end_time + end[3]))
                raw_blocks[avg_group].append(block)

    for key in raw_blocks:
        if len(raw_blocks[key]) == 0:
            raise Exception('Was not able to find raw segments for all groups')
     
    return times, raw_blocks

