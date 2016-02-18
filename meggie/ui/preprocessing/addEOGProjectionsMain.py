# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Apr 25, 2013

@author: Jaakko Leppakangas
Contains the AddEOGProjections-class used for adding EOG projections.
"""

import glob
import mne

from PyQt4 import QtCore,QtGui

from meggie.ui.preprocessing.addProjectionsUi import Ui_Dialog
from meggie.code_meggie.general.caller import Caller

from meggie.ui.utils.messaging import exc_messagebox

class AddEOGProjections(QtGui.QDialog):
    """
    Class for adding EOG projections.
    Projections should be created and saved in a file before adding them.
    """
    caller = Caller.Instance()
    
    def __init__(self, parent, added_projs):
        """
        Constructor. Initializes the dialog.
        Keyword arguments:
        parent        -- The parent of this object.
        projs         -- Projectors already added to the raw object.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        directory = self.caller.experiment._active_subject._subject_path
        self.proj_file = glob.glob(directory + '/*_eog_*proj*')[0]
        self.projs = mne.read_proj(self.proj_file)

        self.listWidget = QtGui.QListWidget()
        self.ui.verticalLayout_2.addWidget(self.listWidget)
        #add checkboxes
        for proj in self.projs:
            item = QtGui.QListWidgetItem(self.listWidget)
            checkBox = QtGui.QCheckBox()
            self.listWidget.setItemWidget(item, checkBox)
            checkBox.setText(str(proj))
            if str(proj) in [str(x) for x in added_projs]:
                checkBox.setChecked(True)

    def accept(self):
        """
        Adds the projections.
        """
        applied = list()
        for index in xrange(self.listWidget.count()):
            check_box = self.listWidget.itemWidget(self.listWidget.item(index))
            applied.append(check_box.isChecked())

        raw = self.caller.experiment.active_subject.working_file
        directory = self.caller.experiment._active_subject._subject_path

        try:
            self.caller.apply_exg('eog', raw, directory, self.projs, applied)
            self.parent.ui.checkBoxEOGApplied.setChecked(True)
        except Exception as e:
            exc_messagebox(self.parent, e)

        self.parent._initialize_ui()
        self.close()
        
