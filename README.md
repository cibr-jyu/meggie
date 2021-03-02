# Meggie

## Installation

The simplest way to install and run meggie is with anaconda / miniconda:
1. Have anaconda / miniconda installed
1. Install meggie inside an environment: *conda create -n meggie-env -c cibr -c conda-forge meggie*
1. Activate environment: *conda activate meggie-env*
1. Run: *meggie*

[//]: # (Hello)

The general way to install Meggie is:
1. Install mne and all its dependencies (https://mne.tools/stable/install)
1. Then install meggie either with conda (conda install -c cibr meggie) or setuptools (python setup.py install)

[//]: # (Hello)

## Documentation

Documentation is found here: *https://teekuningas.github.io/meggie*

[//]: # (Hello)

## Debugging

* If command *meggie* is not found, you should ensure that you are in the correct python environment.
* If the command is found, but the software crashes during startup to an *ImportError*, you should ensure that you are using *Python 3* and that the dependencies are installed. Individual missing dependencies can often be installed with either *conda install* or *pip install*.
* If the software crashes during analysis or startup, and the terminal window does not show you the stacktrace, you can start meggie using command *meggie debug* and reproduce the crash with stacktrace.

## License

This project is licensed under the BSD license.

## Acknowledgements

Great thanks to the *excellent* MNE-python and all the people who have helped.
