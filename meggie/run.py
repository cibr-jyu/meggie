"""Helper to start meggie, used by the setup.py script."""

import matplotlib
import mne
from meggie import mainWindowMain

# use Qt5Agg as TkAgg really hates threads
matplotlib.use("Qt5Agg")

# Use matplotlib as the backend for browser views for now,
# as it is difficult to bind to qt close events and
# because the functionality is still the same
mne.viz.set_browser_backend("matplotlib")


def main():
    """Run Meggie main window."""
    mainWindowMain.main()


# To start meggie directly from the command-line
if __name__ == "__main__":
    mainWindowMain.main()
