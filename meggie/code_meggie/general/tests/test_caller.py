'''
Created on Dec 5, 2015

@author: Jaakko Leppakangas
'''
import sys
import os
from PyQt4 import QtGui
from numpy.testing import assert_equal

from mne.utils import _TempDir
from mne.datasets import sample
from mne.io import Raw

from meggie.ui.general import mainWindowMain
from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import experiment, subject

app = QtGui.QApplication(sys.argv)
try:
    import pkg_resources
    path = pkg_resources.resource_filename('meggie', 'data')
    fname = path + "/sample_audvis_raw.fif"
    if not os.path.isfile(fname):
        raise Exception(fname + ' not found.')
except Exception as e:
    print e
    print "Couldn't locate test file using pkg_resources. Trying mne sample data path instead."
    data_path = sample.data_path()
    fname = data_path + '/MEG/sample/sample_audvis_raw.fif'
    fname = "/home/zairex/Code/cibr/sample_data/MEG/sample"

caller = Caller.Instance()
tempdir = _TempDir()


def _get_experiment():
    """Helper for constructing experiment."""
    exp = experiment.Experiment()
    exp.workspace = tempdir._path
    os.chmod(tempdir._path, 0777)
    exp.name = 'test'
    sub = subject.Subject(exp, 'test_sub')
    sub._working_file = Raw(fname, preload=True)
    exp.add_subject(sub)
    path = os.path.join(tempdir._path, 'experiment')
    os.mkdir(path)
    sub.save_raw(fname, sub.subject_path)
    exp.active_subject_name = sub.subject_name
    exp.update_working_file(exp.active_subject_name, sub.subject_name)
    experiment.ExperimentHandler(caller.parent).initialize_logger(exp)
    return exp


def _setup_caller():
    """Sets up caller."""
    parent = mainWindowMain.MainWindow(app)
    exp = _get_experiment()
    caller.experiment = exp
    caller.parent = parent


def _update_ui():
    QtGui.QApplication.processEvents()


def test_call_exg_ssp():
    """Test calling ecg_ssp and eog_ssp."""
    _setup_caller()
    raw = caller.experiment.get_subjects()[0]._working_file
    params = {'i': raw, 'tmin': -0.1, 'tmax': 0.1, 'event-id': 999,
              'ecg-l-freq': 1., 'ecg-h-freq': 50., 'n-grad': 1, 'n-mag': 1,
              'n-eeg': 1, 'l-freq': 0, 'h-freq': 50, 'rej-grad': 2000,
              'rej-mag': 2000, 'rej-eeg': 60, 'rej-eog': 100, 'qrs': 'auto',
              'bads': '', 'tstart': 0, 'filtersize': 5, 'n-jobs': 1,
              'avg-ref': False, 'no-proj': False, 'average': False,
              'ch_name': None}

    caller._call_ecg_ssp(
        params, 
        caller.experiment.get_subjects()[0],
        do_meanwhile=_update_ui,
    )

    params.update({'eog-l-freq': 1., 'eog-h-freq': 40.})
    result = caller._call_eog_ssp(
        params, 
        caller.experiment.get_subjects()[0],
        do_meanwhile=_update_ui,
    )