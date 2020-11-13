# How to contribute

We would love any contributions, in code and otherwise. Whether its a how-to-use problem, a bug report, or idea for enhancement, please check if an *issue* for the topic already exists, and if not, open one yourself and clearly describe what is in your mind. If you are willing to write code, that is also a good place for us to agree on how to proceed. You don't have to be genius with years of experience; we are all learning. :]

## Getting your code in

We use a simplified variant of GitFlow-model, and have two main branches: master and develop. All features / bugfixes should be implemented in their own branches, and be branched from the develop branch. Develop branch is then merged to master when releasing. To get your code in, you should first fork the repository, create a branch for your contribution out of develop branch, and when finished, create a pull request.

### Getting development environment (in Linux/OSX)

1. Have *Anaconda 3* installed on your system.
1. Fork this repository under your own account.
1. Clone the forked repository to your computer and cd in.
1. Run following command to create isolated environment for development: conda create -n meggie-dev python=3
1. Activate the environment using: source activate meggie-dev
1. Install dependencies from conda-forge: conda install -c conda-forge mne
1. Install meggie in develop mode: python setup.py develop
1. Try if meggie runs by running: meggie debug

### Using Git 

Inside the cloned project directory, you can do following to ensure you are up to date and then create the branch for contribution:
1. Add remote for upstream updates (only once): git remote add upstream git@github.com:Teekuningas/meggie.git
1. Switch to local develop branch: git checkout develop
1. Download and merge updates from upstream: git pull upstream develop
1. Give a good name for feature / bugfix branch and switch to it: git checkout -b fix-bad-documentation

[//]: # (Hello)

Now you are all set to write your code.

### Writing code

Some notes and guidelines:
* Try to keep your code clean. Use for example pycodestyle or flake8 to check your pep8-compliance. Generated code from Qtdesigner is kept as it is.
* UI files (\*.ui) are in the designer\_ui\_files directory. You can use Qtdesigner (open with command *designer* while in the environment) to update UI files, and then *pyuic5* command to generate \*Ui.py files in the meggie/ui/..-directories.
* You can use command *meggie debug* to start meggie in mode, where all output is written into terminal, and you can use python debugger normally.
* If you are fond of *import pdb; pdb.set_trace()*, you should use *meggie.utilities.debug import debug\_trace; debug\_trace()*. Otherwise Qt will spam the window full.

### Finishing with pull request

When finished, you should save your changes (if not done already):
1. Save changes: git commit
1. Push changes to your fork: git push origin fix-bad-documentation
1. Go to your forked repository on github and it should happily notify you about the push you have just made and allow you to click *Compare & pull request*. Fill the details and let the code fly.

## License

When contributing, your code is licensed under BSD license.
