Meggie
------

User-friendly graphical interface to do analysis on EEG and MEG data.

To develop:

1. install anaconda
2. create a new isolated environment:
   conda create -n meggie-env python==2.7.14
3. activate the environment:
   conda activate meggie-env
4. install dependencies:
   pip install mne==0.15.2
   pip install pysurfer
   conda install pyqt==4.11.4
   conda install pyface
   conda install xlrd
   conda install scikit-learn
   conda install matplotlib
   conda install mayavi
5. "install" meggie as symlinks:
   for example: python /path/to/setup.py develop
6. run meggie in debug mode (error messages in console):
   for example: meggie debug
7. run tests:
   for example: python setup.py nosetests

When installed with "develop", changes made to the code will be reflected when meggie is run

To release conda-package (in root directory):

1. Build by:
   conda build .
2. Copy created meggie package to for example anaconda.org cloud:
   anaconda upload ...
3. newest version of meggie should now be installable with just:
   conda install -c cibr meggie
   
