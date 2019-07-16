"""
"""
from meggie.tabs.preprocessing.dialogs.icaDialogMain import ICADialog


def plot(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    raw = subject.get_working_file()
    if raw:
        raw.plot()


def projections(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    raw = subject.get_working_file()
    if not raw.info['projs']:
        messagebox(self, "No added projections.")
        return

    fig = raw.plot_projs_topomap()

    name = subject.subject_name 
    fig.canvas.set_window_title('Projections for ' + name)

def ica(experiment, data, parent):
    """
    """
    subject = experiment.active_subject
    if not subject:
        return

    ica_dialog = ICADialog(parent, experiment)
    ica_dialog.show()
