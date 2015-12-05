'''
Created on Dec 5, 2015

@author: Jaakko Leppakangas
'''
import sys
from PyQt4 import QtGui

from mne.utils import _TempDir
from mne.datasets import sample
from mne.io import Raw

from meggie.ui.general import mainWindowMain
from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import experiment, subject

app = QtGui.QApplication(sys.argv)
data_path = sample.data_path()
fname = data_path + '/MEG/sample/sample_audvis_raw.fif'

caller = Caller.Instance()
tempdir = _TempDir()


def _get_experiment():
    """Helper for constructing experiment."""
    exp = experiment.Experiment()
    exp.workspace = tempdir._path
    exp.name = 'test'
    sub = subject.Subject(exp, 'test_sub')
    sub.raw_data = Raw(fname)
    exp.add_subject(sub)
    return exp


def _setup_caller():
    """Sets up caller."""
    parent = mainWindowMain.MainWindow(app)
    exp = _get_experiment()
    caller.experiment = exp
    caller.parent = parent


def test_call_ecg_ssp():
    """Test calling ecg_ssp."""
    _setup_caller()
    params = {'i': fname, 'tmin': -0.2, 'tmax': 0.5, 'event-id': 1,
              'ecg-l-freq': 0, 'ecg-h-freq': 50, 'n-grad': 2, 'n-mag': 2,
              'n-eeg': 2, 'l-freq': 0, 'h-freq': 50, 'rej-grad': 2000,
              'rej-mag': 2000, 'rej-eeg': 60, 'rej-eog': 100, 'qrs': 0.5,
              'bads': '', 'tstart': 0, 'filtersize': 5, 'n-jobs': 1,
              'avg-ref': False, 'no-proj': False, 'average': False,
              'ch_name': None}
    caller.call_ecg_ssp(params, caller.experiment.get_subjects()[0])
