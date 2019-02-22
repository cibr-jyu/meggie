# Guide to the most basic things in Meggie

## Installation
### Install from anaconda cloud (works in 64bit linux environments)
1. Install meggie from anaconda cloud in an isolated conda environment using command: *conda create -c conda-forge -c CIBR -n meggie-env meggie*
1. Activate the environment using: *source activate meggie-env*
1. Run with command: *meggie* 

[//]: # (Hello)

Installation with this method would be possible for other operating systems too, but conda packages are yet to be built.

### Install from source
My suggestion is to first install MNE-python with all its dependencies to your python environment, and then install meggie to that same environment. Here's one way to do this:
1. Create new python environment: *conda create -n meggie-env python=3*
1. Activate the environment using: *source activate meggie-env*
1. Install mne to environment: *conda install -c conda-forge mne==0.17.0*
1. Clone this repository and go inside.
1. Install meggie to environment using: *python setup.py install*
1. Run Meggie with command: *meggie* 

[//]: # (Hello)

The idea of installing meggie over mne with dependencies should work on any major platform (Windows, Linux, Mac).

### Debugging

* If command *meggie* is not found, you should ensure that you are in the correct python environment.
* If the command is found, but the software crashes during startup to an *ImportError*, you should ensure that you are using *Python 3* and that the dependencies are installed. Individual missing dependencies can often be installed with either *conda install* or *pip install*.
* If the software crashes during analysis, and the terminal window does not show you the stack trace, you may start meggie using command *meggie debug* and reproduce the crash.

## Set up meggie experiment and add first dataset

1. Let's ensure first that preferences are set up correctly, so go and select **Tools** from the menu, and then **Preferences**. Most important setting for now is the working directory. It is the place where all things created by meggie will go. It could be for example *your\_home\_directory/meggie-experiments*. After setting that, click **ok**.
1. You can then create a new meggie experiment. Click **File** and then **Create new experiment**. Fill the fields as you like (you must give a name.) Good practice is to avoid spaces and special characters in the name. Then click **ok**. A folder for the experiment is created inside the working directory. An experiment will be a container for datasets, or as they are called in Meggie, subjects, that you can run analysis on.
1. Then, add a subject to this experiment. Click **Add new...** on the left panel, and then click **Browse...** Locate a raw dataset in .fif format from your file system, select it, and then click **Open** and **ok**. Rest of the text will assume that you selected *sample\_audvis\_raw.fif* from the mne software package. When a subject is added, Meggie will copy (but not cut) the original raw data file to experiment folder. 
1. To start analysing the added subject, select the name *sample\_audvis\_raw.fif* from the list on the left panel, and click **Activate selected**. Shortly, some info appears on the bottom left of the window, and perhaps in other parts of the window too, and the analysis tools become available.

## Taking the first look

* We can take a look at the data by clicking **Raw plot**. You can use arrow keys to move through time or through channels. More functionality can be found by clicking the **Help** button. 
* Bad channels can be set via **Customize channels..** on the right so that they are not taken into account in the further analysis.

## Artifact removal via ICA

1. Select **ICA...** in the *Available actions* section. 
1. Click **Compute** to start a temporal FastICA-algorithm. When the computation is done, the upper list box below is populated with the found ICA components.
1. One can use **Plot time courses** and **Plot topographies** actions to identify components containing the artifacts. Usually the cardiac artifact and the blink artifact are easily identified both by their topography and time course.
1. After identifying the components, select them in the upper box, and use **Transfer** button, to move them to the lower, “to be removed”, list.
1. **Plot changes** button creates a plot where one can compare the data before component removal and after component removal, without actually changing the data yet.
1. If it looks like that the artifacts are getting removed properly, close the plot and press **Apply** to remove the components from the data. Data is modified in-place, and cannot be reversed (note that original data is still unchanged as Meggie makes a copy of it when adding a subject.) In the main window, *ICA applied* -checkbox should be now toggled.

## Computing evoked responses

1. Select *Epoching* tab from the upper part of the main window.
1. Select **Create new collection..** from the *Available actions* section. 
1. Let's first create a collection for left-ear auditory responses. For those, the event code that was used to label left auditory sounds during the experiment was *1*. Set *Collection name* to be *LeftAuditory*, and set *Event ID* to *1*, while leaving *Mask* as *0*. Click **Add to list**, and then **Create epochs** from the bottom.
1. Let's do the same for right-ear auditory responses. Click **Create new collection..**, use *RightAuditory* as name, set *2* as *Event ID*, and *0* as *Mask*, and click **Create epochs**. 
1. Select *Evoked responses* tab from the upper part of the main window. Our purpose is to create a plot where evoked potentials of left auditory and right auditory responses are plotted on top of each other to see if they differ.
1. Select both *RightAuditory* and *LeftAuditory* entries from the *Epoch collections* list and click **Create evoked dataset**.
1. Entry called *RightAuditory-LeftAuditory_evoked.fif* should appear on the right. Select it and click **Visualize selected dataset** below. Topographically arranged plot of evoked responses appears.
1. Click plots to see subplots.
1. Close all the opened plots. If you want to do statistical analysis (outside of Meggie), you can use **Save evoked data** to export data as a csv file. The csv file will be created in *output*-folder inside the experiment folder.

## License

This project is licensed under the BSD license.

## Acknowledgements

Great thanks to the *excellent* MNE-python.
