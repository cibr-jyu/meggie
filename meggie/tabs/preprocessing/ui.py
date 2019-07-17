"""
"""
from meggie.tabs.preprocessing.dialogs.icaDialogMain import ICADialog
from meggie.tabs.preprocessing.dialogs.filterDialogMain import FilterDialog
from meggie.tabs.preprocessing.dialogs.resamplingDialogMain import ResamplingDialog
from meggie.tabs.preprocessing.dialogs.rereferencingDialogMain import RereferencingDialog


def plot(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    raw = subject.get_raw()
    if raw:
        raw.plot()


def projections(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    raw = subject.get_raw()
    if not raw.info['projs']:
        messagebox(self, "No added projections.")
        return

    fig = raw.plot_projs_topomap()

    name = subject.name 
    fig.canvas.set_window_title('Projections for ' + name)


def ica(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    ica_dialog = ICADialog(parent, experiment)
    ica_dialog.show()


def filter(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    filter_dialog = FilterDialog(parent, experiment)
    filter_dialog.show()


def resample(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    resampling_dialog = ResamplingDialog(parent, experiment)
    resampling_dialog.show()


def rereference(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    rereferencing_dialog = RereferencingDialog(parent, experiment)
    rereferencing_dialog.show()
