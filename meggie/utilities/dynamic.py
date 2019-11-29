# coding: utf-8

import os
import json
import pkg_resources
import importlib
import logging

from PyQt5 import QtWidgets

from meggie.utilities.messaging import exc_messagebox


def find_all_tab_specs():
    """ Finds all valid tab packages under tabs-folder.
    """
    tab_specs = {}
    tab_path = pkg_resources.resource_filename('meggie', 'tabs')
    for package in os.listdir(tab_path):
        config_path = os.path.join(tab_path, package, 'configuration.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                if config:
                    tab_specs[config['id']] = package, config
    return tab_specs

def construct_tab(package, tab_spec, parent):
    """ Constructs analysis tab dynamically.

    Constructs analysis tab dynamically from python package
    containing an configuration file and code
    """

    class DynamicTab(QtWidgets.QDialog):
        def __init__(self, parent):
            QtWidgets.QDialog.__init__(self)
            self.parent = parent
            self.tab_spec = tab_spec

            # first create basic layout

            self.gridLayoutContainer = QtWidgets.QGridLayout(self)

            self.gridLayoutRoot = QtWidgets.QGridLayout()
            self.gridLayoutContainer.addLayout(self.gridLayoutRoot, 0, 0, 1, 1)

            if tab_spec.get('outputs'):
                self.groupBoxOutputs = QtWidgets.QGroupBox(self)
                self.groupBoxOutputs.setTitle('Outputs')
                self.gridLayoutOutputs = QtWidgets.QGridLayout(self.groupBoxOutputs)

            if tab_spec.get('actions'):
                self.groupBoxActions = QtWidgets.QGroupBox(self)
                self.groupBoxActions.setTitle('Actions')
                self.gridLayoutActions = QtWidgets.QGridLayout(self.groupBoxActions)

            if tab_spec.get('transforms'):
                self.groupBoxTransforms = QtWidgets.QGroupBox(self)
                self.groupBoxTransforms.setTitle('Transforms')
                self.gridLayoutTransforms = QtWidgets.QGridLayout(self.groupBoxTransforms)
                
            if tab_spec.get('inputs'):
                self.groupBoxInputs = QtWidgets.QGroupBox(self)
                self.groupBoxInputs.setTitle('Inputs')
                self.gridLayoutInputs = QtWidgets.QGridLayout(self.groupBoxInputs)

            if tab_spec.get('info'):
                self.groupBoxInfo = QtWidgets.QGroupBox(self)
                self.groupBoxInfo.setTitle('Info')
                self.gridLayoutInfo = QtWidgets.QGridLayout(self.groupBoxInfo)

            # add the (empty) input lists
            for idx, input_name in enumerate(tab_spec.get('inputs', [])):

                if input_name in list(tab_spec.get('translations', {}).keys()):
                    title = tab_spec['translations'][input_name]
                else:
                    title = input_name.capitalize()

                groupBoxInputElement = QtWidgets.QGroupBox(self.groupBoxInputs)
                groupBoxInputElement.setTitle(title)
                gridLayoutInputElement = QtWidgets.QGridLayout(groupBoxInputElement)
                listWidgetInputElement = QtWidgets.QListWidget(groupBoxInputElement)

                listWidgetInputElement.setSelectionMode(
                    QtWidgets.QAbstractItemView.ExtendedSelection)

                gridLayoutInputElement.addWidget(listWidgetInputElement, idx, 0, 1, 1)
                self.gridLayoutInputs.addWidget(groupBoxInputElement)

                setattr(self, 'groupBoxInputElement_' + str(idx+1), 
                        groupBoxInputElement)
                setattr(self, 'gridLayoutInputElement_' + str(idx+1), 
                        gridLayoutInputElement)
                setattr(self, 'listWidgetInputElement_' + str(idx+1), 
                        listWidgetInputElement)

            # add the (empty) output lists
            for idx, output_name in enumerate(tab_spec.get('outputs', [])):
                if output_name in list(tab_spec.get('translations', {}).keys()):
                    title = tab_spec['translations'][output_name]
                else:
                    title = output_name.capitalize()

                groupBoxOutputElement = QtWidgets.QGroupBox(self.groupBoxOutputs)
                groupBoxOutputElement.setTitle(title)
                gridLayoutOutputElement = QtWidgets.QGridLayout(groupBoxOutputElement)
                listWidgetOutputElement = QtWidgets.QListWidget(groupBoxOutputElement)

                listWidgetOutputElement.setSelectionMode(
                    QtWidgets.QAbstractItemView.ExtendedSelection)

                gridLayoutOutputElement.addWidget(listWidgetOutputElement, idx, 0, 1, 1)
                self.gridLayoutOutputs.addWidget(groupBoxOutputElement)

                setattr(self, 'groupBoxOutputElement_' + str(idx+1), 
                        groupBoxOutputElement)
                setattr(self, 'gridLayoutOutputElement_' + str(idx+1), 
                        gridLayoutOutputElement)
                setattr(self, 'listWidgetOutputElement_' + str(idx+1), 
                        listWidgetOutputElement)

            # add transform buttons
            for idx, transform_name in enumerate(tab_spec.get('transforms', [])):
                if transform_name in list(tab_spec.get('translations', {}).keys()):
                    title = tab_spec['translations'][transform_name]
                else:
                    title = transform_name.capitalize()

                pushButtonTransformElement = QtWidgets.QPushButton(self.groupBoxTransforms)
                pushButtonTransformElement.setText(title)
                self.gridLayoutTransforms.addWidget(pushButtonTransformElement, idx, 0, 1, 1)
                setattr(self, 'pushButtonTransformElement_' + str(idx+1), 
                        pushButtonTransformElement)

            # add action buttons
            for idx, action_name in enumerate(tab_spec.get('actions', [])):
                if action_name in list(tab_spec.get('translations', {}).keys()):
                    title = tab_spec['translations'][action_name]
                else:
                    title = action_name.capitalize()

                pushButtonActionElement = QtWidgets.QPushButton(self.groupBoxActions)
                pushButtonActionElement.setText(title)
                self.gridLayoutActions.addWidget(pushButtonActionElement, idx, 0, 1, 1)
                setattr(self, 'pushButtonActionElement_' + str(idx+1), 
                        pushButtonActionElement)

            # add info text boxes
            for idx, info_name in enumerate(tab_spec.get('info', [])):

                if info_name in list(tab_spec.get('translations', {}).keys()):
                    title = tab_spec['translations'][info_name]
                else:
                    title = info_name.capitalize()

                groupBoxInfoElement = QtWidgets.QGroupBox(self.groupBoxInfo)
                groupBoxInfoElement.setTitle(title)
                gridLayoutInfoElement = QtWidgets.QGridLayout(groupBoxInfoElement)
                plainTextEditInfoElement = QtWidgets.QTextBrowser(groupBoxInfoElement)

                gridLayoutInfoElement.addWidget(plainTextEditInfoElement, idx, 0, 1, 1)
                self.gridLayoutInfo.addWidget(groupBoxInfoElement)

                setattr(self, 'groupBoxInfoElement_' + str(idx+1), 
                        groupBoxInfoElement)
                setattr(self, 'gridLayoutInfoElement_' + str(idx+1), 
                        gridLayoutInfoElement)
                setattr(self, 'plainTextEditInfoElement_' + str(idx+1), 
                        plainTextEditInfoElement)

            # lay out inputs, transforms, outputs, actions and info elements
            # in a nice way to a grid
            if tab_spec.get('inputs') and not tab_spec.get('transforms'):
                self.gridLayoutRoot.addWidget(self.groupBoxInputs, 0, 0, 2, 1)
            elif tab_spec.get('inputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxInputs, 0, 0, 1, 1)

            if tab_spec.get('outputs') and not tab_spec.get('actions'):
                self.gridLayoutRoot.addWidget(self.groupBoxOutputs, 0, 1, 2, 1)
            elif tab_spec.get('outputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxOutputs, 0, 1, 1, 1)

            if tab_spec.get('transforms') and not tab_spec.get('inputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxTransforms, 0, 0, 2, 1)
            elif tab_spec.get('transforms'):
                self.gridLayoutRoot.addWidget(self.groupBoxTransforms, 1, 0, 1, 1)

            if tab_spec.get('actions') and not tab_spec.get('outputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxActions, 0, 1, 2, 1)
            elif tab_spec.get('actions'):
                self.gridLayoutRoot.addWidget(self.groupBoxActions, 1, 1, 1, 1)

            if tab_spec.get('info'):
                self.gridLayoutRoot.addWidget(self.groupBoxInfo, 0, 2, 2, 1)

            # add spacers to bottom and right to keep the window concise
            spacerItemVertical = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayoutContainer.addItem(spacerItemVertical, 1, 0, 1, 1)
            spacerItemHorizontal = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.gridLayoutContainer.addItem(spacerItemHorizontal, 0, 1, 1, 1)

            # add handlers for list selection changed -> info updates
            def connect_to_handler(list_element, info_element, info_name):
                module = importlib.import_module(
                    '.'.join(['meggie', 'tabs', package, 'ui']))
                handler = getattr(module, info_name)

                def handler_wrapper():
                    experiment = self.parent.experiment
                    if not experiment:
                        return
                    subject = experiment.active_subject
                    if not subject:
                        return

                    data = self._get_data()

                    try:
                        info_content = handler(experiment, data, parent)
                    except Exception as e:
                        exc_messagebox(self, e)

                    info_element.setPlainText(info_content)
                    
                list_element.itemSelectionChanged.connect(handler_wrapper)

            for idx, info_name in enumerate(self.tab_spec.get('info', [])):
                info_element = getattr(self, 'plainTextEditInfoElement_' + 
                                       str(idx+1))

                for idx, input_name in enumerate(tab_spec.get('inputs', [])):

                    input_element = getattr(self, 'listWidgetInputElement_' + str(idx+1))
                    connect_to_handler(input_element, info_element, info_name)

                for idx, output_name in enumerate(tab_spec.get('outputs', [])):

                    output_element = getattr(self, 'listWidgetOutputElement_' + str(idx+1))
                    connect_to_handler(output_element, info_element, info_name)


            # add button handlers
            def connect_to_handler(button, name):
                module = importlib.import_module(
                    '.'.join(['meggie', 'tabs', package, 'ui']))
                handler = getattr(module, name)

                def handler_wrapper(checked):
                    experiment = self.parent.experiment
                    if not experiment:
                        return

                    subject = experiment.active_subject
                    if not subject:
                        return

                    data = self._get_data()

                    try:
                        handler(experiment, data, parent)
                    except Exception as e:
                        exc_messagebox(self, e)
                    
                button.clicked.connect(handler_wrapper)

            for idx, action_name in enumerate(tab_spec.get('actions', [])):
                action_element = getattr(self, 'pushButtonActionElement_' + str(idx+1))
                connect_to_handler(action_element, action_name)
            for idx, transform_name in enumerate(tab_spec.get('transforms', [])):
                transform_element = getattr(self, 'pushButtonTransformElement_' + str(idx+1))
                connect_to_handler(transform_element, transform_name)

        def _get_data(self):
            """ Returns data from input and output lists
            """
            data = {'inputs': {},
                    'outputs': {}}

            inputs = [] 
            for idx, name in enumerate(self.tab_spec.get('inputs', [])):
                ui_element = getattr(self, 'listWidgetInputElement_' + str(idx+1))
                try:
                    selected_items = [item.text() for item in ui_element.selectedItems()]
                except:
                    continue

                data['inputs'][name] = selected_items
        
            for idx, name in enumerate(self.tab_spec.get('outputs', [])):
                ui_element = getattr(self, 'listWidgetOutputElement_' + str(idx+1))
                try:
                    selected_items = [item.text() for item in 
                                      ui_element.selectedItems()]
                except:
                    continue
                data['outputs'][name] = selected_items

            return data

        def initialize_ui(self):
            """ Updates (empties and refills) ui contents when called
            """

            experiment = self.parent.experiment
            if not experiment:
                return

            subject = experiment.active_subject

            # fill input lists with contents
            for idx, input_name in enumerate(self.tab_spec.get('inputs', [])):
                ui_element = getattr(self, 'listWidgetInputElement_' + str(idx+1))

                ui_element.clear()

                if not subject:
                    continue

                data = getattr(subject, input_name, None)
                if not data:
                    logging.getLogger('ui_logger').info(
                        "Data not found for " + str(input_name) + 
                        " in " + self.name + " tab.")
                    continue

                for key in sorted(list(data.keys())):
                    ui_element.addItem(key)

            # fill output lists with contents
            for idx, output_name in enumerate(self.tab_spec.get('outputs', [])):
                ui_element = getattr(self, 'listWidgetOutputElement_' + str(idx+1))

                ui_element.clear()

                if not subject:
                    continue

                data = getattr(subject, output_name, None)
                if not data:
                    logging.getLogger('ui_logger').info(
                        "Data not found for " + str(output_name) + 
                        " in " + self.name + " tab.")
                    continue

                for key in sorted(list(data.keys())):
                    ui_element.addItem(key)

            # allow to fill info element already here.
            # there are also handlers to update info element 
            # on list selection changes
            for idx, info_name in enumerate(self.tab_spec.get('info', [])):
                ui_element = getattr(self, 'plainTextEditInfoElement_' + str(idx+1))

                module = importlib.import_module(
                    '.'.join(['meggie', 'tabs', package, 'ui']))
                handler = getattr(module, info_name)
                info_content = handler(experiment, None, self.parent)
                ui_element.setPlainText(info_content)

        @property
        def name(self):
            return self.tab_spec['name']

    DynamicTab.__name__ = 'MainWindowTab' + tab_spec['id'].capitalize()

    tab = DynamicTab(parent)

    return tab
