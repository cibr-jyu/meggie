# Meggie

## Documentation

* User documentation is found here: *http://meggie.teekuningas.net*
* Developer documentation is found here: *https://cibr-jyu.github.io/meggie*

[//]: # (Hello)

## Installation (from terminal)

Note that Python>=3.8 might be required to get the newest version.

### From conda-forge (mamba instead of conda might install faster):

1. Install meggie to a conda environment: conda create -n meggie-env -c conda-forge meggie=1.6.1
1. Activate the environment: conda activate meggie-env
1. Run: meggie

### Using this repository:

1. Clone this repository to /path/to/meggie/repo
1. Create virtual environment: python -m venv /path/to/meggie-env
1. Activate the environment: source /path/to/meggie-env/bin/activate
1. Enter the repository: cd /path/to/meggie/repo
1. Install dependencies: python -m pip install -r requirements.txt
1. Install meggie: python -m pip install .
1. Run: meggie

[//]: # (Hello)

## Debugging

* If command *meggie* is not found, you should ensure that you are in the correct python environment.
* If the command is found, but the software crashes during startup to an *ImportError*, you should ensure that you are using *Python 3* and that the dependencies are installed. Individual missing dependencies can often be installed with either *conda install* or *pip install*.
* If the software crashes during analysis or startup, and the terminal window does not show you the stacktrace, you can start meggie using command *meggie debug* and then the next crash will come with a stacktrace.

[//]: # (Hello)

## License

This project is licensed under the BSD license.

[//]: # (Hello)

## Acknowledgements

Great thanks to the *excellent* MNE-python and all the people who have helped.
