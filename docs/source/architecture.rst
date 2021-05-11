Architecture
============

Main classes
------------
There are three basic structures in Meggie.

MainWindow
**********
MainWindow contains the user interface.

Experiment
**********
Experiment contains the highest-level container for all the data.

Subject
*******
Subjects are added to experiments and store subject-specific data.

Tabs and datatypes
------------------
Analysis functionality is based on two key structures, datatypes and tabs. 

Datatypes 
*********
Datatypes can store objects created from subject-specific data.
created from the subject-specific data.

Tabs
****
Tabs provide implementations for the analysis actions.

Plugins
-------
Creation of plugins is simple and fun. Datatypes and tabs are dynamically located at the runtime and are loadable from other python packages from meggie_* namespace.

Simplest possible plugin
************************
To create a plugin, start by bootstrapping a package with this structure:

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

The tab introduces an action that needs implementation in ui.py:

.. container:: codelisting
   
   * from meggie.utilities.messaging import messagebox
   * def hello(experiment, data, window):

      * """ Helloes the active subject.
      * """
      * message = 'Hello {}!'.format(experiment.active_subject.name)
      * messagebox(window, message)

That's it! The code is available in `here. <https://github.com/Teekuningas/meggie_simpleplugin>`_. 
To see it in use, see `this. <https://meggie.teekuningas.net>`_.
