"""Contains implementation for epochs plot"""

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.plotting import set_figure_title
from meggie.utilities.plotting import get_figure_title

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotEpochsImage(Action):
    """Opens MNE's image plot."""

    def run(self):

        try:
            selected_name = self.data["outputs"]["epochs"][0]
        except IndexError:
            return

        subject = self.experiment.active_subject
        try:
            self.handler(subject, {"name": selected_name})
        except Exception as exc:
            exc_messagebox(self.window, exc)

    @subject_action
    def handler(self, subject, params):
        epochs = subject.epochs.get(params["name"])
        mne_epochs = epochs.content
        figs = mne_epochs.plot_image()
        for fig in figs:
            ch_type = get_figure_title(fig)
            title = "{0}_{1}".format(params["name"], ch_type)
            set_figure_title(fig, title)
