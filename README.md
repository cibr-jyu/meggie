Meggie
------

User-friendly graphical interface to do analysis on EEG and MEG data.

To develop:

1. install anaconda
2. create a new isolated environment:
   conda create -n meggie-dev-env python=3
3. activate the environment:
   conda activate meggie-dev-env
4. install dependencies:
   conda install -c conda-forge mne
5. "install" meggie as symlinks:
   for example: python setup.py develop
6. run meggie in debug mode (error messages in console):
   for example: meggie debug
