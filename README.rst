Meggie
------

User-friendly graphical interface to do analysis on EEG and MEG data.

To develop in linux:

1. install anaconda
2. create a new isolated environment:
   conda create -n meggie-env-develop python==3.6.6
3. activate the environment:
   conda activate meggie-env-develop
4. install dependencies:
   conda install -c conda-forge mne
   pip install nose
5. "install" meggie as symlinks:
   python setup.py develop
6. run meggie in debug mode (error messages in console):
   meggie debug
7. run tests:
   for example: python -m "nose"

When installed with "develop", changes made to the code will be reflected when meggie is run

To release conda-package (in root directory):
1. Have following entry in .condarc:
   channels:
     - https://conda.anaconda.org/conda-forge
     - defaults
     - https://conda.anaconda.org/CIBR
2. Build by:
   conda build .
3. Copy created meggie package to for example anaconda.org cloud:
   anaconda upload ...
4. newest version of meggie should now be installable with just:
   conda install -n meggie-env -c CIBR -c conda-forge meggie
