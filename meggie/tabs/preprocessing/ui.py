"""
"""
from meggie.tabs.preprocessing.dialogs.icaDialogMain import ICADialog
from meggie.tabs.preprocessing.dialogs.filterDialogMain import FilterDialog
from meggie.tabs.preprocessing.dialogs.resamplingDialogMain import ResamplingDialog
from meggie.tabs.preprocessing.dialogs.rereferencingDialogMain import RereferencingDialog


def plot(experiment, data, window):
    """
    """
    subject = experiment.active_subject
    raw = subject.get_raw()
    if raw:
        raw.plot()


def projections(experiment, data, window):
    """
    """
    subject = experiment.active_subject
    raw = subject.get_raw()
    if not raw.info['projs']:
        messagebox(self, "No added projections.")
        return

    fig = raw.plot_projs_topomap()

    name = subject.name 
    fig.canvas.set_window_title('Projections for ' + name)


def ica(experiment, data, window):
    """
    """
    ica_dialog = ICADialog(window, experiment)
    ica_dialog.show()


def filter(experiment, data, window):
    """
    """
    filter_dialog = FilterDialog(window, experiment)
    filter_dialog.show()


def resample(experiment, data, window):
    """
    """
    resampling_dialog = ResamplingDialog(window, experiment)
    resampling_dialog.show()


def rereference(experiment, data, window):
    """
    """
    rereferencing_dialog = RereferencingDialog(window, experiment)
    rereferencing_dialog.show()
