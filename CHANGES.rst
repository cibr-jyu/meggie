Changelog
=========

0.7.1 (unreleased)
------------------

- Nothing changed yet.

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
