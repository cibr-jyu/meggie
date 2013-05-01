'''
Created on Apr 25, 2013

@author: jaeilepp
'''
import glob

import mne

from PyQt4 import QtCore,QtGui
from addProjections_Ui import Ui_Dialog

class AddEOGProjections(QtGui.QDialog):
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        directory = self.parent.experiment._subject_directory
        self.proj_file = glob.glob(directory + '*_eog_proj.fif')[0]
        self.projs = mne.read_proj(self.proj_file)
        
        self.listWidget = QtGui.QListWidget()
        self.ui.verticalLayout_2.addWidget(self.listWidget)
        #add checkboxes
        for proj in self.projs:
            item = QtGui.QListWidgetItem(self.listWidget)
            checkBox = QtGui.QCheckBox()
            self.listWidget.setItemWidget(item, checkBox)
            checkBox.setText(str(proj))
        
        
    def accept(self):
        applied = []
        for index in xrange(self.listWidget.count()):
            check_box = self.listWidget.itemWidget(self.listWidget.item(index))
            if check_box.checkState() == QtCore.Qt.Checked:
                applied.append(self.projs[index])
        mne.write_proj(self.proj_file, applied)
        self.parent.caller.apply_eog(self.parent.experiment.raw_data,
                                     self.parent.experiment._subject_directory)
        self.parent._initialize_ui()
        self.close()
        