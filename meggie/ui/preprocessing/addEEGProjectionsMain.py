'''
Created on 11.10.2016

@author: jaolpeso
'''

import glob
import mne

from PyQt4 import QtGui

from meggie.code_meggie.general.caller import Caller

from meggie.ui.preprocessing.addProjectionsUi import Ui_Dialog
from meggie.ui.utils.messaging import exc_messagebox


class AddEEGProjections(QtGui.QDialog):
    '''
    classdocs
    '''
    caller = Caller.Instance()

    def __init__(self, parent, added_projs):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        directory = self.caller.experiment.active_subject.subject_path
        self.proj_file = glob.glob(directory + '/*_eeg_*proj*')[0]
        self.projs = mne.read_proj(self.proj_file)
        
        self.listWidget = QtGui.QListWidget()
        self.ui.verticalLayout_2.addWidget(self.listWidget)
        # Add checkboxes
        for proj in self.projs:
            item = QtGui.QListWidgetItem(self.listWidget)
            checkBox = QtGui.QCheckBox()
            self.listWidget.setItemWidget(item, checkBox)
            checkBox.setText(str(proj))
            if str(proj) in [str(x) for x in added_projs]:
                checkBox.setChecked(True)
                
    def accept(self):
        """
        Tells the caller to add the selected projections to the working file.
        """       

        applied = list()
        for index in xrange(self.listWidget.count()):
            check_box=self.listWidget.itemWidget(self.listWidget.item(index))
            applied.append(check_box.isChecked())

        raw = self.caller.experiment.active_subject.get_working_file()
        directory = self.caller.experiment.active_subject.subject_path

        try:
            self.caller.apply_exg('eeg', raw, directory, self.projs, applied)
            self.parent.ui.checkBoxEEGApplied.setChecked(True)
        except Exception as e:
            exc_messagebox(self.parent, e)

        self.parent.initialize_ui()
        self.close()

        