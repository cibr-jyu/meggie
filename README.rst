Meggie
------

User-friendly graphical interface to do analysis on EEG and MEG data.

To develop:

1. install anaconda
2. create a new isolated environment:
   conda create -n meggie-env python
3. activate the environment:
   source activate meggie-env
4. install dependencies:
   conda install -c cibr mne
   conda install pyqt==4.11.4
   conda install pyface
   conda install xlrd
5. "install" meggie as symlinks using anaconda's interpreter:
   for example: ~/anaconda/bin/python /path/to/setup.py develop
6. run meggie in debug mode:
   for example: ~/anaconda/bin/meggie debug
7. run tests:
   for example: ~/anaconda/bin/python setup.py nosetests

When installed with "develop", changes made to the code will be reflected when meggie is run

To release conda-package:

1. Build by:
   conda build .
2. Copy created meggie package to for example anaconda.org cloud:
   anaconda upload ...
3. newest version of meggie should now be installable with just:
   conda install -c cibr meggie
   
