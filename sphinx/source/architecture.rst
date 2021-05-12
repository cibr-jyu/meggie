Architecture
============
This document provides a broad overview with some insights to how meggie is built and how that can be used for advantage.

Main classes
------------
There are three basic structures in Meggie.

MainWindow
**********
MainWindow contains the user interface, and is implemented with PyQt5. The most important elements of the MainWindow are the left panel, holding experiment-specific information, the bottom console, which logs user actions, and the right panel, which contains the tabs that are used for data transformations.

Experiment
**********
Experiment contains the highest-level container for all the data. It implements logic for saving and loading experiments and stores subjects within it.

Subject
*******
Subjects are added to experiments and store subject-specific data. Most importantly they are responsible for saving and loading the raw data, but they also store dataobjects based on datatypes.

Tabs and datatypes
------------------
The analysis functionality is based on two key structures, datatypes and tabs. 

Datatypes 
*********
Often the raw data can be summarized in structures, that capture the essential features for the purpose of analysis. For example, based on event information, the raw data can split into small segments of data that are averaged together to create event-related responses. These kind of structures, e.g. epochs, evokeds, spectrums, TFRs, that are instantiated from prespecified datatypes, can be stored within subjects. In meggie, these "blueprints" are all stored in the datatypes folder.

Tabs
****
Tabs provide implementations for the analysis actions. They consist of a declaration of what buttons (actions and transformations), and what boxes (inputs, outputs, info) should be in the tab, and the implementations of these in Python. From the declaration meggie dynamically creates the tab, figures out its layout, fills in the contents, and puts it into the MainWindow. Clicking the buttons, for example, will then call a function with matching name in the python implementation. In meggie, these are stored in the tabs folder.

Plugins
-------
Creation of plugins is simple and fun. Datatypes and tabs are dynamically located at the runtime and are loadable from other python packages from meggie_* namespace. Thus implementing a plugin corresponds to creating a python package (with name in the meggie_* namespace) which introduced tabs and datatypes.

API
***
We thrive to keep the core of Meggie, which is covers everything but the tabs, as stable and reusable as possible. Thus as a plugin developer, you are allowed to use the API of MainWindow, Subject and Experiment classes, the four datatypes provided in the datatypes folder, as well as the utilities stored in the utilities folder.

Simplest possible plugin
************************
To create a plugin, start by bootstrapping a package with this structure:

.. container:: codelisting

   * meggie_simpleplugin

      * MANIFEST.in
      * setup.py
      * meggie_simplelugin

         * configuration.json
         * tabs

            * simpleplugin

               * configuration.json
               * ui.py

MANIFEST.in and setup.py are standard files in python packaging. MANIFEST.in lists
what files inside the subdirectories should be included and what should be excluded when
installing the package. setup.py contains the installation script with some metadata and
flags. Let us use trivial ones. 
MANIFEST.in:

.. container:: codelisting

   * recursive-include meggie_simpleplugin *
   * global-exclude \*.py[co]
   * global exclude __pycache__

setup.py:

.. container:: codelisting

   * from setuptools import setup
   * setup(

      * name='meggie_simpleplugin',
      * version='0.1.0',
      * license='BSD',
      * packages=['meggie_simpleplugin'],
      * include_package_data=True,
      * zip_safe=False,
      * install_requires=['setuptools'])

Next, configuration.json declares the name and description of the plugin.

.. container:: codelisting

   * {"name": "meggie_simpleplugin",
   * "description": "The most simple possible meggie plugin"}

The plugin introduces a tab, and a tab needs a declaration in the 
meggie_simpleplugin/tabs/simpleplugin/configuration.json file:

.. container:: codelisting

   * {"id": "simpleplugin",
   * "name": "Simple plugin",
   * "actions": ["hello"]}

The tab introduces an action that needs a implementation in ui.py:

.. container:: codelisting
   
   * from meggie.utilities.messaging import messagebox
   * def hello(experiment, data, window):

      * """ Helloes the active subject.
      * """
      * message = 'Hello {}!'.format(experiment.active_subject.name)
      * messagebox(window, message)

That's it! The code is available in `here <https://github.com/Teekuningas/meggie_simpleplugin>`_. 
To see it in use, see `the user documentation <http://meggie.teekuningas.net>`_.

