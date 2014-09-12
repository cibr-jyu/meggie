'''
Created on 30.6.2014

@author: Kari Aliranta
'''


from PyQt4 import QtCore, QtGui

from forwardModels import ForwardModels
from forwardModelDialogUi import Ui_forwardModelDialog
import messageBox
import string

class ForwardModelDialog(QtGui.QDialog):
    """
    Class containing the logic for forwardModelDialog. It collects parameter
    values for creating forward models and passes them to ***
    
    TODO passes to something that coordinates the MVC structure related
    to views related to forward modeling and saving new forward models to disk.
    
    TODO Removing forward models from disk and view coordination is handled by
    ***
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_forwardModelDialog()
        self.ui.setupUi(self)
        
    
    def accept(self):
        """
        Does the following:

        1. Collects the parameters from the dialog
        2. Passes the parameters to forwardModeling for actual creation of
        forward model.
        """
        
        fmdict = {}
        
        fmdict['fname'] = self.ui.lineEditFModelName.text()
        fmdict['spacing'] = self.ui.spinBoxSpacing.value()
        fmdict['surfaceDecimMethod'] = self.ui.comboBoxSurfaceDecimMethod.currentText()
        fmdict['surfaceDecimValue'] = self.ui.spinBoxSurfaceDecimValue.value()
        fmdict['surfaceName'] = self.ui.comboBoxSurfaceName.currentText()
        fmdict['computeCorticalStats'] = str(self.ui.buttonGroupCorticalPatchStats \
                                           .checkedButton().objectName())
        fmdict['useAtlas'] = str(self.ui.buttonGroupAtlas \
                                           .checkedButton().objectName())
        fmdict['triangFilesType'] = self.ui.comboBoxTriangFiles.currentText()
        fmdict['triangFilesIco'] = self.ui.spinBoxTriangFilesIco.value()
        fmdict['CompartModel'] = self.ui.comboBoxCompartmentModel.currentText()
        fmdict['nosol'] = str(self.ui.buttonGroupNosol \
                        .checkedButton.objectName())
        fmdict['innerShift'] = self.ui.spinBoxInnerShift.value()
        fmdict['outerShift'] = self.ui.spinBoxOuterShift.value()
        fmdict['skullShift'] = self.ui.spinBoxSkullShift.value()
        fmdict['brainc'] = self.ui.doubleSpinBoxBrainConductivity.value()
        fmdict['skullc'] = self.ui.doubleSpinBoxSkullConductivity.value()
        fmdict['scalpc'] = self.ui.doubleSpinBoxScalpConductivity.value()
        
        # A bit of checking for stupidities in naming to avoid conflicts
        # with directories created by MNE scripts.
        if string.lower(fmdict['fname']) is 'mri' or 'bem':
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(
                "'mri' or 'bem' are not acceptable fmodel names")
            self.messageBox.show()
            return

        try:
            self.parent.caller.create_forward_model(fmdict)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(
                'Problem creating forward model' + str(err))
            self.messageBox.show()
            return