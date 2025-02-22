"""Helper to start meggie, used by the setup.py script."""

import matplotlib
import joblib
import mne

import colorama

from meggie import mainWindowMain

# use Qt5Agg as TkAgg really hates threads
matplotlib.use("Qt5Agg")

# Use matplotlib as the backend for browser views for now,
# as it is difficult to bind to qt close events and
# because the functionality is still the same
mne.viz.set_browser_backend("matplotlib")

# Silence the failing of reset_all in colorama:
# RuntimeError: wrapped C/C++ object of type EmittingStream has been deleted
colorama.initialise.reset_all = lambda: None


# Joblib is so very verbose,
# and we have our own logging system,
# so silence it for now.
def patched_progress(self):
    return


joblib.parallel.Parallel.print_progress = patched_progress


def main():
    """Run Meggie main window."""
    mainWindowMain.main()


# To start meggie directly from the command-line
if __name__ == "__main__":
    mainWindowMain.main()
