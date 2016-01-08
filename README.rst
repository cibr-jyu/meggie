Meggie
------

User-friendly graphical interface to do analysis on EEG and MEG data.

To develop:

1. install anaconda
2. "install" meggie as symlinks using anaconda's interpreter:
   for example: ~/anaconda/bin/python setup.py develop
3. run meggie:
   for example: ~/anaconda/bin/meggie
4. run tests:
   for example: ~/anaconda/bin/python setup.py nosetests

When installed with "develop", changes made to the code will be reflected when meggie is run

To release conda-package:

1. Add our custom channel to conda config by: 
   conda config --add channels *repo-address*
2. Build by:
   conda build .
3. Copy created meggie package to our channel via for example scp:
   scp ...
