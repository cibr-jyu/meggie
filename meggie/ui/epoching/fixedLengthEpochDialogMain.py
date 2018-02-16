'''
Created on 10.9.2015

@author: Jaakko Leppakangas
'''
from PyQt4 import QtGui
from PyQt4.QtGui import QDialogButtonBox

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.code_meggie.general.caller import Caller
from meggie.ui.epoching.fixedLengthEpochDialogUi import Ui_FixedLengthEpochDialog

class FixedLengthEpochDialog(QtGui.QDialog):
    """
    Class containing the logic for FixedLengthEpochDialog. It is used for
    creating fixed length events.
    """
    caller = Caller.Instance()

    def __init__(self, parent):
        """Initialize the event selection dialog.

        Keyword arguments:

        parent -- Set the parent of this dialog
        """
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_FixedLengthEpochDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setText('Add events')
        self.raw = self.caller.experiment.active_subject.get_working_file(temporary=True)
        tmax = int(self.raw.times[-1])
        self.ui.spinBoxStart.setMaximum(tmax)
        self.ui.spinBoxEnd.setMaximum(tmax)
        self.ui.spinBoxEnd.setValue(tmax)

    def accept(self, *args, **kwargs):
        event_params = {
            'tmin': self.ui.spinBoxStart.value(),
            'tmax': self.ui.spinBoxEnd.value(),
            'interval': self.ui.doubleSpinBoxInterval.value(),
        }
        subject = self.parent.get_selected_subject()
        working_file = subject.get_working_file(preload=False)
        
        events = mne.make_fixed_length_events(
            working_file, 0, event_params['tmin'],
            event_params['tmax'], event_params['interval']
        )
        if len(events) > 0:
            if event_params not in self.parent.event_data['fixed_length_events']:
                self.parent.event_data['fixed_length_events'].append(event_params)
                self.parent.update_events()
        return QtGui.QDialog.accept(self, *args, **kwargs)
