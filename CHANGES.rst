Changelog
=========

0.3.4 (unreleased)
------------------

- Nothing changed yet.

0.3.3 (2016-10-25)
------------------

- Do bit selection dialog
- Finetune spectrum interval finding
- Use min_duration==2 and shortest_event=1 when finding events

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
