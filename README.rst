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

1. Build by:
   conda build .
2. Copy created meggie package to for example anaconda.org cloud:
   anaconda upload ...
   
