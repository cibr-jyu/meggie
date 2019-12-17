# Guide to the most basic things in Meggie

## Installation

Suggested way to install meggie is to first install MNE-python with all its dependencies to python environment, and then install meggie to that same environment. Here's one way to do this in Unix with the help of anaconda distribution:
1. Create new python environment: *conda create -n meggie-env python=3*
1. Activate the environment using: *source activate meggie-env*
1. Install mne to environment: *conda install -c defaults -c conda-forge mne*
1. Clone or download this repository and go inside.
1. Install meggie to the environment using: *python setup.py install*
1. Run Meggie with command: *meggie* 

[//]: # (Hello)

Note that installing MNE-python with "pip install mne" does not install dependencies. If you don't want to use conda-forge channel for MNE-python installation, please consult https://www.martinos.org/mne/stable/install_mne_python.html for official instructions.

[//]: # (Hello)

Meggie can be installed directly using conda too:
1. Create environment: *conda create -n meggie-env python=3*
1. Activate environment: *source activate meggie-env*
1. Install meggie: *conda install -c defaults -c conda-forge -c cibr meggie*
1. Run meggie with: *meggie*

[//]: # (Hello)

Given that we routinely release conda packages, meggie can even be installed with no Terminal what so ever if in Windows:
1. Download Anaconda 3 and install it.
1. Open Anaconda Navigator from Start menu.
1. Add channels cibr and conda-forge to channels list.
1. Go to Environments tab, and create environment called *meggie-env* and initialize it with Python version 3.7
1. Go to Home tab again and select *meggie-env* from the environments list at the top.
1. Meggie icon should appear in the main view. Click install.
1. And then launch.

## Debugging

* If command *meggie* is not found, you should ensure that you are in the correct python environment.
* If the command is found, but the software crashes during startup to an *ImportError*, you should ensure that you are using *Python 3* and that the dependencies are installed. Individual missing dependencies can often be installed with either *conda install* or *pip install*.
* If the software crashes during analysis, and the terminal window does not show you the stack trace, you may start meggie using command *meggie debug* and reproduce the crash with stacktrace.

## License

This project is licensed under the BSD license.

## Acknowledgements

Great thanks to the *excellent* MNE-python.
