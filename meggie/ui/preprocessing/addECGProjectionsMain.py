# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppakangas, Janne Pesonen and Atte Rautio>
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
Contains the AddECGProjections-class used for adding ECG projections.
"""

import glob
import numpy as np

from PyQt4 import QtGui

from meggie.code_meggie.preprocessing.projections import read_projections
from meggie.code_meggie.preprocessing.projections import preview_projections
from meggie.code_meggie.preprocessing.projections import apply_exg

from meggie.ui.preprocessing.addProjectionsUi import Ui_Dialog
from meggie.ui.utils.messaging import exc_messagebox

class AddECGProjections(QtGui.QDialog):
    """
    Class containing the logic for adding ECG projections.
    Projections should be created and saved in a file before adding them.
    """
    def __init__(self, parent, added_projs):
        """
        Constructor. Initializes the dialog.
        Keyword arguments:
        parent        -- The parent of this object.
        added_projs   -- Projectors already added to the raw object.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        directory = self.parent.experiment.active_subject.subject_path

        self.projs = read_projections(
            glob.glob(directory + '/*_ecg_*proj*')[0])

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

    def on_pushButtonPreview_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        raw = self.parent.experiment.active_subject.get_working_file()
        applied = self.create_applied_list()
        projs = np.array(self.projs)[np.array(applied)]

        preview_projections(raw, projs)

    def create_applied_list(self):
        """
        """
        applied = list()

        for index in xrange(self.listWidget.count()):
            checkbox = self.listWidget.itemWidget(self.listWidget.item(index))
            applied.append(checkbox.isChecked())

        return applied

    def accept(self):
        """
        add the selected projections to the working file.
        """

        experiment = self.parent.experiment
        raw = experiment.active_subject.get_working_file()
        directory = experiment.active_subject.subject_path
        applied = self.create_applied_list()

        projs = np.array(self.projs)[np.array(applied)]

        try:
            apply_exg('ecg', experiment, raw, directory, projs,
                      do_meanwhile=self.parent.update_ui)
            self.parent.ui.checkBoxECGApplied.setChecked(True)
        except Exception as exc:
            exc_messagebox(self.parent, exc)

        self.parent.initialize_ui()
        self.close()
