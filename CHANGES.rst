Changelog
=========

1.9.5 (unreleased)
------------------

- nothing changed yet.

1.9.4 (2025-08-21)
------------------

- Remove use of deprecated pkg_resources, use importlib instead

1.9.3 (2025-04-12)
------------------

- Update epochs_plot and raw_plot to correctly apply the changes of bads, annotations or selections at the subject_action. Helps re-running the action only based on action log.

1.9.2 (2025-03-22)
------------------

- Fix serialization of action logs so that the types of values can be reliably inferred on the importing side

1.9.1 (2025-03-16)
------------------

- Migrate to pyproject.toml
- Update installation instructions

1.9.0 (2025-03-15)
------------------

- Simplify test functionality for plugins
- Make internal filename handling more robust for spectrums and tfrs
- Update to mne==1.9.0
- Add action log exports
- For csv's, ask for location instead of using the output folder.
- Update docs
- Support non-scalar spectrums, e.g for differences.

1.8.0 (2024-04-16)
------------------

- Update documentation to include what mne functions are used by the actions
- Make it possible to create experiment based on a open datasets
- Update evoked and tfr default names
- Use standard locations for config and data files
- Make it possible to have dataobjects without raw
- Fix identifying common channels in tfr group average

1.7.0 (2024-03-25)
------------------

- Fix actions.log propagation problem
- Add a lot of tests for maintainability
- Add new partially generated readthedocs documentation
- Add "Add MNE sample data" option to subject dialog.
- Add tooltips to actions using configuration.json metadata
- Add a little messagebox if no subject is active when clicking an action
- Fix empty lines problem in channel groups dialog
- Update to support mne==1.6.1

1.6.3 (2023-12-11)
------------------

- Fix problem with a regexp in save_raw.

1.6.2 (2023-11-27)
------------------

- Fix group averages for multiple groups
- Fix tse plot units with no-mean baseline correction

1.6.1 (2023-11-23)
------------------

- Fix save_raw for long recordings with split files

1.6.0 (2023-11-06)
------------------

- Make meggie consistent across induced response channel averages: baseline is corrected to before averaging over channels
- Pin matplotlib==3.7.3 as newer matplotlibs are not compatible with pinned mne==1.3.1
- Fix bug where saving TFR's resulted in csv file for each subject even though there should be only one file with all subjects' data in.

1.5.3 (2023-10-23)
------------------

- Fix error that happened when saving TFR without baselining

1.5.2 (2023-08-03)
------------------

- Allow selecting multiple channels for rereferencing

1.5.1 (2023-04-05)
------------------

- Remove a forgotten debug command
- Fix tests

1.5.0 (2023-04-05)
------------------

- Update to mne==1.3.1
- Replace heuristic find_stim_channel with mne's own

1.4.4 (2023-04-03)
------------------

- Better color defaults for TFR's
- Fix regression in group average assertions

1.4.3 (2022-12-14)
------------------

- Fix spectrum dialog crashing for non-int overlap

1.4.2 (2022-12-12)
------------------

- Fix evoked image plot

1.4.1 (2022-11-25)
------------------

- Allow persistent custom preferences in .meggieprefs

1.4.0 (2022-11-21)
------------------

- Fix meggie to use matplotlib backend for plot browser even when mne-qt-browser is installed

1.3.9 (2022-10-18)
------------------

- And fix one more missing set_figure_title

1.3.8 (2022-10-18)
------------------

- nothing changed yet.

1.3.7 (2022-10-18)
------------------

- Fix breaking typo

1.3.6 (2022-10-18)
------------------

- matplotlib introduced a breaking change

1.3.6 (2022-10-28)
------------------

- Fix packaging

1.3.5 (2022-10-18)
------------------

- Fix regressions due to mne changes.

1.3.4 (2022-05-19)
------------------

- Bump version to fix pypi build

1.3.3 (2022-0-23)
------------------

- Require python>=3.7

1.3.2 (2022-0-23)
------------------

- Pin mne to 1.0.0
- ..and fix related

1.3.1 (2021-09-08)
------------------

- Add missing h5py dependency

1.3.0 (2021-08-20)
------------------

- Fix spectrums and actions for old experiments
- Add descriptions to logged actions

1.2.1 (2021-08-19)
------------------

- Update setup.py for pypi

1.2.0 (2021-08-19)
------------------

- Switch to pipelines and actions architecture
- Replace message logging with more structured actions logging
- Add three basic pipelines for evokeds, spectrums and TFR's
- Make it possible to easily extend pipelines from plugins
- Add dialog for explicitly enabling or disabling installed plugins
- Improve exception handling to avoid crashing
- Add more throbbers to UI

1.1.1 (2021-06-21)
------------------

- Add simple reusable dialog

1.1.0 (2021-05-12)
------------------

- Make mne==0.23.0 compatible
- Add permutation tests 
- Clean codebase for better reuse
- Add docstrings and autogenerate documentation using sphinx
- Include mne.Info to spectrum objects.
- Fix non-fif reading.
- Add utility for generating multi-subject experiments from sample_audvis_raw
- Update messaging
- Move source analysis out to external plugin.

1.0.2 (2021-03-02)
------------------

- Fix channel average plots with non-orthodox channel groups

1.0.1 (2021-03-02)
------------------

- Fix issue with channel selection saving

1.0.0 (2020-01-11)
------------------

- Add 19 tests.
- Improve exception handling and logging
- Make plugin loading more robust
- Fix tab ordering of main window
- Channel average plots for each channel type are put into single figure
- Fix tse baselining for channel averages
- Sorted conditions in topo plot and channel averages
- Try to use default channel groups if channel groups not set
- Fix regexp for next_available_name
- Allow delay in epoch creation

0.17.1 (2020-12-31)
------------------

- Update mne dependency to >=0.22.0

0.17.0 (2020-12-31)
------------------

- Remove workspace attribute from experiment and use path instead
- Do not require comment attribute to be set when creating Evoked
- Try to get default channel groups from active subject if channel groups not set
- Add tests for utilities, experiment.py, subject.py and datatypes
- Remove old stc code to separate branch
- Add new import possibilities by using read_raw instead of read_raw_fif
- If both EEG and MEG data present, show both when plotting topography
- Add event delay for epoch creation
- Fix mne_wrapper pkgutil bug
- Improve exception messaging in many places

0.16.1 (2020-11-13)
------------------

- Fix broken import

0.16.0 (2020-11-13)
------------------

- Add single channel plotting functionality for evokeds
- Add radius setting for evoked topomaps (to allow different "skirts")
- Add more information to info boxes
- Overwrite when saving epochs
- Fix import bug in montage dialog
- Fix reject param ticks bug

0.15.0 (2020-04-20)
------------------

- Use Qt5 backend instead off Tkinter for matplotlib (fixes threading issues, hopefully not much slower)
- Implement plugin discovery
- Try printing more info on terminal on crash even on non-debug session
- Update to mne==0.20.0
- Replace layouts with default montages (mne is deprecating layouts)
- Add dialog for setting and computing channel average groups
- Store spectrums under the hood only in power units
- Fix couple of crashes
- Clean up iterate_topography code and name cleaning code
- In saved csvs, use different columns for ch_name, ch_type, subject name etc.

0.14.6 (2020-03-11)
------------------

- Improve memory handling

0.14.5 (2020-03-09)
------------------

- Add events from annotations dialog
- Allow missing end points in dynamic spectrum creation

0.14.4 (2020-02-19)
------------------

- Fix subject removal error when any subject activated
- Add times settings to evoked topomaps

0.14.3 (2020-02-14)
------------------

- Fix saving exceptions

0.14.2 (2019-12-18)
------------------

- Fix layout problem

0.14.1 (2019-12-18)
------------------

- Experiment file backup when saving
- Splitter to main window
- Improve dynamic spectrum creation
- Fix bugs

0.14.0 (2019-12-17)
------------------

- New dynamic tab and datatype handling unifies both code and look
- Tab presets for pipelines
- Look and implementation of dialogs unified
- MaiWindow left bar updated
- Be more defensive on getting maxfilter info
- Improve spectrum batching with more options to dynamic interval selection
- CSV saving for TFR's
- Add more baselining options to TFR's
- Make mne==0.19.2 compatible
- Add default object namings for dialogs
- Lots of codebase cleaning
- Update mne logging from whitelisting to blacklisting

0.13.1 (2019-04-28)
------------------

- Fix log dialog filtering
- Clean up code base
- Fix crashes when no subject is activated

0.13.0 (2019-04-13)
------------------

- Fix source analysis pipeline
- Fix epochs plot scale
- Allow multiple conditions in TFR's
- Implement multi-group-average for TFR's
- Add TSE plot

0.12.0 (2019-04-03)
------------------

- Add filter options to log window
- Remove SSP for now
- Implement multi-group-average for evokeds and spectrums
- Make batching widget more sensible
- Add batch for resampling, spectrums and TFR's
- Implement channel averages for TFR's
- Improve TFR dialogs
- Catch name validation failures

0.11.1 (2019-03-24)
------------------

- Allow adding same dataset again, add number suffix
- Fix batch widget in event selection dialog
- Fix group averages if only active subject contains the data


0.11.0 (2019-03-18)
------------------

- Update MNE dependency to 0.17.1
- Add and unify channel averaging in spectrums and evokeds
- Open experiment also by specifying exp file
- Disallow creating new experiment over existing experiment
- Fix power spectrum dialog name field size
- Improve EEG support

0.10.1 (2019-02-21)
------------------

- Fix typo that made epoch creation crash

0.10.0 (2019-02-21)
------------------

- Refactor code
- Make meggie windows compatible
- Fix bugs
- Clean up UI

0.9.1 (2019-01-15)
------------------

- Implement resampling and rereferencing
- Add baseline adjusting to epochs
- Add bad channel dropping to evoked topo
- Fix ICA for EEG
- Fix EEG topomaps
- Update to mne==0.17.0

0.9.0 (2018-11-06)
------------------

- Update code to be python3 and pyqt5 compatible
- Fix splitted raw file problem with spectrum computation
- Separate grad and mag ch types properly in spectrum computation
- Add small beauty enhancements

0.8.1 (2018-05-03)
------------------

- Fix bugs

0.8.0 (2018-05-02)
------------------

- Fix evoked topomap title bug
- Implement group average for psd's and tfr's
- Fix defaults for tfr and psd creation
- Don't exclude bads when creating epochs
- Fix epoch overwrite bug
- Separate creation, plotting and saving of TFR's and spectrums
- Spectrums to their own tab
- Refactor codebase

0.7.0 (2018-04-12)
------------------

- Add plot evoked topomaps
- Add output options for spectrums
- Remove evoked stats dialog
- Add throbbers
- Add subject list sorting
- Update power spectrum dialog default values
- Fix evoked batch ui initialization bug

0.6.3 (2018-04-03)
------------------

- Fix ICA 

0.6.2 (2018-03-23)
------------------

- Add throbbers

0.6.1 (2018-03-22)
------------------

- Refactor code
- Update throbbers
- Clean up messages

0.6.0 (2018-03-09)
------------------

- Pin MNE-python dependency to 0.15.2
- Update logging mechanism
- Refactor a lot of codebase
- (Re)implement the source analysis pipeline
- Fix ICA custom layout issue

0.5.2 (2017-10-14)
------------------

- Add throbber to ICA computation

0.5.1 (2017-10-14)
------------------

- Fix bug that broke opening of some EEG files

0.5.0 (2017-08-14)
------------------

- Implement simple ICA for preprocessing
- Fix bug of pattern matching in file saving validity check
- Fix open raw problem
- Use weighted average for averaging in spectrums
- Hide some misleading warnings
- Add meggie version number to experiment files
- Fix power spectrum units label
- Improve folder structure and code quality of meggie
- Improve evoked topology colors
- Do not save raw if saving terminated
- Add save data tick for tfr topology 

0.4.3 (2017-04-04)
------------------

- Remove unnecessary import that crashed after scipy updated

0.4.2 (2017-04-04)
------------------

- Don't crash on MNE-python's show_fiff-bug

0.4.1 (2016-12-09)
------------------

- Add polarity inversion feature to ocular projections dialog
- Do plot for exg events
- Fix epoch channel visualization error

0.4.0 (2016-12-07)
------------------

- Remove window scaling from dialog parameters in epoch channel visualization
- Fix batching widget error when collect_parameter_values returned empty list
- Update TFR dialogs and allow saving
- Change file naming
- Fix TFR in preprocessing tab
- Do experiment specific layout selection
- Do not make copy of raw when open customize bads dialog
- Rename fourier analysis -tab to spectral analysis -tab
- Make changes in averaging tab including stats dialog
- Fix ecg/eog dialogs
- Fix epoch plot to not save bads

0.3.9 (2016-11-21)
------------------

- Fix subject activation bug
- Clean up logging code a bit
- Do bad channel selection dialog
- change logic that checks if projs are applied
- Fix bitselectiondialog
- fix meggie events
- fix filter batch
- fix projs previews
- remove mne_browse_raw
- Remove tabs from code
- Remove stim in eventselectiondialog
- Remake epoch masking
- Do not change bad channels when normally plotting raw

0.3.8 (2016-11-07)
------------------

- Update MNE to 0.13.0
- Fix error of meggie not starting because of random import

0.3.7 (2016-11-01)
------------------

- Add uint_cast=True when finding events
- Check if file has movement corrections
- fix spurious event detection
- remove stimulus channel selection in eventselectiondialog
- Use stim channel when finding events in power spectrum dialog
- Fix default stim channel in event selection dialog

0.3.6 (2016-10-27)
------------------

- Fix preferences dialog

0.3.5 (2016-10-27)
------------------

- Fix mask length on spectrum events dialog

0.3.4 (2016-10-27)
------------------

- Update bit selection dialog

0.3.3 (2016-10-25)
------------------

- Do bit selection dialog
- Finetune spectrum interval finding

0.3.2 (2016-10-18)
------------------

- Do event based power spectrum calculation
- Fix evoked stats channel visualization.
- Set correct default tab on source analysis.
- Fix bug of end time equaling length of data crashing the spectrum calculation
- Fix bug where ECG batching didnt work for a set of subjects in experiment

0.3.1 (2016-08-03)
------------------

- Fix power spectrum bug

0.3.0 (2016-08-01)
------------------

- New Fourier analysis tab
- Source analysis tabs gathered to same place
- Simplify tfr and spectrum calculations on raw data
- Allow spectrums to be calculated for epoched data
- Better save data functionality
- Cleaner dialogs
- Update MNE to 0.12.0
- Global n_jobs setting

0.2.9 (2016-04-27)
------------------

- Improve performance in ECG calculation dialog
- Make exp file more readable

0.2.8 (2016-04-25)
------------------

- Remove epoch and evoked batch, clear event list

0.2.7 (2016-04-21)
------------------

- Fix EEG reference reapplying
- UI stuff

0.2.6 (2016-04-19)
------------------

- Allow saving all evoked data
- Interesting channels selection on epoch creation
- Fix layout files
- Group averaging creates evoked object

0.2.5 (2016-04-07)
------------------

- Revert to meggie console logging

0.2.4 (2016-04-07)
------------------

- Fix epoch rejections

0.2.3 (2016-04-07)
------------------

- Fix bugs

0.2.2 (2016-04-01)
------------------

- Debug logging

0.2.1 (2016-03-31)
------------------

- Fix after broken merge

0.2.0 (2016-03-31)
------------------

- Whole new batching functionality
- New beautiful core without pickling
- Experiments can be opened from everywhere
- Old-style experiments cannot be opened anymore
- Cleaned up a lot of code
- Log mne commands

0.1.5 (2016-02-08)
------------------

- Add missing dependencies 

0.1.4 (2016-02-01)
------------------

- Use home folder for preferences instead of installation folder
- Clean up prints

0.1.3 (2016-01-25)
------------------

- Fix mask spinBox

0.1.2 (2016-01-22)
------------------

- Logging 

0.1.1 (2016-01-13)
------------------

- Fix backwards compatibility issue and exclude some unnecessary files from the package


0.1.0 (2016-01-08)
------------------

- Initial release with conda packaging system
