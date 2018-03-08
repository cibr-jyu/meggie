from PyQt4 import QtGui

from meggie.ui.source_analysis.linearSourceEstimateDialogUi import Ui_linearSourceEstimateDialog  # noqa

from meggie.code_meggie.general.source_analysis import create_linear_source_estimate  # noqa

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.decorators import threaded

import meggie.code_meggie.general.mne_wrapper as mne

class LinearSourceEstimateDialog(QtGui.QDialog):
    """
    """

    def __init__(self, parent, fwd_name, inst_type, inst_name, experiment=None, on_close=None):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_linearSourceEstimateDialog()
        self.ui.setupUi(self)
        self.on_close = on_close
        self.experiment = experiment
        self.fwd_name = fwd_name
        self.inst_type = inst_type
        self.inst_name = inst_name

        if inst_type == 'raw':
            self.ui.groupBoxTimeParameters.setEnabled(True)
            self.ui.doubleSpinBoxStart.setEnabled(True)
            self.ui.doubleSpinBoxEnd.setEnabled(True)
            raw = self.experiment.active_subject.get_working_file(preload=False)
            self.ui.doubleSpinBoxStart.setValue(raw.times[0])
            self.ui.doubleSpinBoxEnd.setValue(raw.times[-1])

        self.ui.lineEditBasedOn.setText(fwd_name)
        self.ui.lineEditData.setText(inst_name)

        self.populate_labels()
        self.populate_covariances()


    def read_labels(self):
        active_subject = self.experiment.active_subject
        subject = active_subject.mri_subject_name
        subjects_dir = active_subject.source_analysis_directory

        labels = mne.read_labels_from_annot(subject=subject, parc='aparc',
            subjects_dir=subjects_dir)

        return labels

    def populate_labels(self):
        labels = self.read_labels()

        self.ui.comboBoxLabel.clear()
        self.ui.comboBoxLabel.addItem('None')
        for label in labels:
            self.ui.comboBoxLabel.addItem(label.name)

        self.ui.comboBoxLabel.setCurrentIndex(0)

    def populate_covariances(self):
        active_subject = self.experiment.active_subject

        covariances = active_subject.get_covfiles()
        self.ui.comboBoxCovariance.clear()
        for covariance in covariances:
            self.ui.comboBoxCovariance.addItem(covariance)
        self.ui.comboBoxCovariance.setCurrentIndex(0)

    def accept(self):
        """
        """

        # collect parameters
        stc_name = str(self.ui.lineEditSourceEstimateName.text())
        if not stc_name:
            messagebox(self, "Please give a name for the source estimate", 
                       exec_=True)
            return

        if stc_name in self.experiment.active_subject.stcs:
            messagebox(self, "Source estimate with this name already exists", 
                       exec_=True)
            return

        fwd_name = self.fwd_name
        inst_name = self.inst_name
        inst_type = self.inst_type

        loose = float(self.ui.doubleSpinBoxLoose.value())
        depth = float(self.ui.doubleSpinBoxDepth.value())
        lambda2 = float(self.ui.doubleSpinBoxLambda.value())
        method = str(self.ui.comboBoxMethod.currentText())
        covfile = str(self.ui.comboBoxCovariance.currentText())

        if not covfile:
            messagebox(self, "No covariance matrix selected", exec_=True)
            return

        start = float(self.ui.doubleSpinBoxStart.value())
        end = float(self.ui.doubleSpinBoxEnd.value())

        if inst_type == 'raw':
            start, end = None, None

        label = str(self.ui.comboBoxLabel.currentText())
        if label == 'None':
            label = None
        else:
            labels = self.read_labels()
            label = [lbl for lbl in labels if lbl.name == label][0]

        subject = self.experiment.active_subject

        @threaded
        def linear_stc(*args, **kwargs):
            create_linear_source_estimate(*args, **kwargs)

        try:
            linear_stc(self.experiment, stc_name, inst_name, inst_type, 
                       covfile, fwd_name, loose, depth, label, lambda2, 
                       method, start, end)
        except Exception as exc:
            exc_messagebox(self.parent, exc, exec_=True)

        # call close handler
        if self.on_close:
            self.on_close()

        self.close()

