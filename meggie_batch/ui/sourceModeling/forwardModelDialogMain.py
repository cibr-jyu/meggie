'''
Created on 30.6.2014

@author: Kari Aliranta
'''


from PyQt4 import QtCore, QtGui

from forwardModels import ForwardModels
from forwardModelDialogUi import Ui_forwardModelDialog
import messageBoxes
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
        
    
    def populateSurfaceNamesCombobox(self):
        """
        TODO use file manager to find all files under the surf-directory
        and populate the self.ui.comboBoxSurfaceName with them.
        """
        
    def collectParametersIntoDictionary(self):
        """
        Collects the parameters from the ui fields of the dialog and returns
        them in a dictionary.
        """
        fmdict = {}
        
        fmdict['fname'] = self.ui.lineEditFModelName.text()
        
        # A bit of checking for stupidities in naming to avoid conflicts
        # with directories created by MNE scripts.
        # TODO probably should be limited to alphanumeric ascii without spaces,
        # too.
        if string.lower(fmdict['fname']) is 'mri' or 'bem':
            message = "'mri' or 'bem' are not acceptable fmodel names"
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        fmdict['spacing'] = self.ui.spinBoxSpacing.value()
        fmdict['surfaceDecimMethod'] = self.ui.comboBoxSurfaceDecimMethod.currentText()
        fmdict['surfaceDecimValue'] = self.ui.spinBoxSurfaceDecimValue.value()
        
        # TODO should be self.ui.comboBoxSurfaceName.currentText(), currently
        # using default 'white' for testing
        fmdict['surfaceName'] = 'white'
        
        if self.ui.buttonGroupCorticalPatchStats.checkedButton().objectName() is \
        'radioButtonPatchStatYes':
            fmdict['computeCorticalStats'] = True
        else: fmdict['computeCorticalStats'] = False
            
        if self.ui.buttonGroupAtlas.checkedButton().objectName() is \
        'radioButtonAtlasYes':
            fmdict['useAtlas'] = True
        else: fmdict['useAtlas'] = False                    
        
        fmdict['triangFilesType'] = self.ui.comboBoxTriangFiles.currentText()
        fmdict['triangFilesIco'] = self.ui.spinBoxTriangFilesIco.value()
        fmdict['compartModel'] = self.ui.comboBoxCompartmentModel.currentText()
        
        if self.ui.buttonGroupNosol.checkedButton.objectName() is \
        'radioButtonNoSolYes':
            fmdict['nosol'] = True
        else: fmdict['nosol'] = False
        
        fmdict['innerShift'] = self.ui.spinBoxInnerShift.value()
        fmdict['outerShift'] = self.ui.spinBoxOuterShift.value()
        fmdict['skullShift'] = self.ui.spinBoxSkullShift.value()
        fmdict['brainc'] = self.ui.doubleSpinBoxBrainConductivity.value()
        fmdict['skullc'] = self.ui.doubleSpinBoxSkullConductivity.value()
        fmdict['scalpc'] = self.ui.doubleSpinBoxScalpConductivity.value()
        
        return fmdict
        
        
    def convertParameterDictionaryToCommandlineParameterDict(self, fmdict):
        """
        Converts the parameters input in the dialog into valid command line
        argument strings for various MNE-C-scripts (mne_setup_source_space, 
        mne_watershed_bem, mne_setup_forward_model) used in forward model
        creation.
        
        Keyword arguments:
        
        pdict        -- dictionary
        
        Returns a tuple of lists with suitable arguments for commandline tools.
        Looks like this:
        (mne_setup_source_space_argumentList, mne_watershed_bem_argumentList, 
        mne_setup_forward_model_argumentList) 
        """
        
        # Arguments for source space setup
        if fmdict['surfaceDecimMethod'] is 'traditional (default)':
            sDecimIcoArg = []
        else: sDecimIcoArg = ['--ico', fmdict['surfaceDecimValue']]
        
        if fmdict['computeCorticalStats'] is True:
            cpsArg = ['--cps']
        else: cpsArg = []
        
        spacingArg = ['--spacing', fmdict['spacing']]
        surfaceArg = ['--surface', fmdict['surfaceName']]
        
        setupSourceSpaceArgs = spacingArg + surfaceArg + sDecimIcoArg + cpsArg
        
        # Arguments for BEM model meshes
        if fmdict['useAtlas'] is True:
            waterShedArgs = ['--atlas']
        else: waterShedArgs = []
        
        # Arguments for BEM model setup
        if fmdict['triangFilesType'] is 'standard ASCII (default)':
            surfArg = []
            bemIcoArg = []
        else: 
            surfArg = '--surf'
            bemIcoArg = ['--ico', fmdict['triangFilesIco']]
        
        if fmdict['compartModel'] is 'standard ASCII (default)':
            braincArg = [ fmdict['brainc']]
            skullcArg = fmdict['skullc']
            scalpcArg = fmdict['scalpc']
        else:
            braincArg = []
            skullcArg = []
            scalpcArg = []

        if fmdict['nosol'] is True:
            nosolArg = '--nosol'
        else: nosolArg = []
        
        innerShiftArg = ['--innerShift', fmdict['innerShift']] 
        outerShiftArg = ['--outerShift', fmdict['outerShift']] 
        skullShiftArg = ['--outerShift', fmdict['skullShift']] 
        
        setupFModelArgs = surfArg + bemIcoArg + braincArg + skullcArg + \
                          scalpcArg + nosolArg + innerShiftArg + outerShiftArg + \
                          + skullShiftArg
        
        return (setupSourceSpaceArgs, waterShedArgs, setupFModelArgs)
        
        
    def accept(self):
        """
        Gets the arguments from the gui and passes them to caller for forward
        model creation. 
        """
        
        fmdict = self.collectParametersIntoDictionary(self)
        
        pdict = self.convertParameterDictionaryToCommandlineParameterTuple(fmdict)

        try:
            self.parent.caller.create_forward_model(pdict)
        except Exception, err:
            message = 'Problem creating forward model' + str(err)
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return