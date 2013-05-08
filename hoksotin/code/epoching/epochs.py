# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
"""
import mne
from mne.layouts import read_layout
from mne.viz import plot_topo

import pylab as pl

import events

class Epochs(object):
    """
    A class for epochs created from the MEG data.
    """


    def __init__(self, raw, events, mag, grad, eeg, stim,
                 eog, reject, category, tmin=-0.2, tmax=0.5):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object.
        events        -- Array of events.
        mag           -- Boolean that tells whether magnetometers will be used.
        grad          -- Boolean that tells whether gradiometers will be used.
        eeg           -- Boolean that tells whether eeg-channels will be used.
        stim          -- Boolean that tells whether stim-channels will be used.
        eog           -- Boolean that tells whether eog-channels will be used.
        reject        -- Rejection parameter for epochs.
        category      -- Dictionary of categories.
        tmin          -- Start time before event (default -0.2)
        tmax          -- End time after the event (default 0.5)
        Raises TypeError if the raw object isn't of type mne.fiff.Raw.
        Raises Exception if picks are empty.
        """
        if mag and grad:
            meg = True
        elif mag:
            meg = 'mag'
        elif grad:
            meg = 'grad'
        else:
            meg = False
        if isinstance(raw, mne.fiff.raw.Raw):
            picks = mne.fiff.pick_types(raw.info, meg=meg, eeg=eeg,
                                        stim=stim, eog=eog)
            if picks is None:
                raise Exception('Picks cannot be empty.')
            self.epochs = mne.Epochs(raw, events, category,
                                     tmin, tmax, picks=picks, reject=reject)
        else:
            raise TypeError('Not a Raw object.')
        
    def average(self):
        """
        Average epochs.
        Draws a topography representation of the evoked potentials.
        Raises an exception if cannot find any epochs.
        """
        if self.epochs is None:
            raise Exception('No epochs found.')
        category = self.epochs.event_id
        print category
        evokeds = [self.epochs[name].average() for name in category.keys()]
        layout = read_layout('Vectorview-all.lout')
        fig = plot_topo(evokeds, layout, title=str(category.keys()))
        fig.show()
        
        def onclick(event):
            pl.show(block=False)
        
        fig.canvas.mpl_connect('button_press_event', onclick)
        