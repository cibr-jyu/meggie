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
Subjects are added to experiments and store subject-specific data. Most importantly they are responsible for saving and loading the raw data, but they also store instances of datatypes.

Actions, pipelines and datatypes
--------------------------------
The analysis functionality is based on three key structures: actions, pipelines and datatypes.

Datatypes 
*********
Often the raw data can be summarized in structures that capture the essential features for the purpose of analysis. For example, based on event information, the raw data can split into small segments of data that are averaged together to create event-related responses. These kind of structures, e.g. epochs, evokeds, spectrums, TFRs, that are instantiated from prespecified datatypes, can be stored within subjects. In meggie, these "blueprints" are all stored, declared and implemented in the datatypes folder.

Actions
*******
Actions are basic analysis steps such as "filter" or "create epochs". In Meggie, each one of these is declared independently in its own folder within "actions" folder. Each action consists of metadata in "configuration.json" and python code. The entry point within the python code is assumed to inherit from the Action-class defined in mainwindow/dynamic.py. If done so, the actions can be embedded in pipelines, and are automatically logged in a backlog of actions.

Pipelines
*********
Pipelines are sets of actions arranged as buttons within tabs in the GUI and correspond to certain types of analyses from the beginning to the end such as "Sensor-level continuous data analysis" or "Source-level evoked response analysis". These are declared in the main configuration.json and as they utilize the actions for implementations, they do not include any python code.

Plugins
-------
Creation of plugins is simple. Pipelines, datatypes and actions are dynamically located at the runtime and are loadable from other python packages from meggie_* namespace. Thus implementing a plugin corresponds to creating a python package (with name in the meggie_* namespace) which introduced pipelines, actions and/or datatypes.

API
***
We thrive to keep the core of Meggie, which covers everything but the actions, as stable and reusable as possible. Thus as a plugin developer, you are allowed to use the API of MainWindow, Subject and Experiment classes, the four datatypes provided in the datatypes folder, as well as the functions, dialogs and widgets stored in the utilities folder.

Where to start
**************
See the code for simplest possible plugin `here <https://github.com/cibr-jyu/meggie_simpleplugin>`_. 
To see it in use, see `the user documentation <http://meggie.teekuningas.net>`_.

