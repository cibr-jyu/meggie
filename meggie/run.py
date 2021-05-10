"""Helper to start meggie, used by the setup.py script."""

# use Qt5Agg as TkAgg really hates threads
import matplotlib
matplotlib.use('Qt5Agg')

from meggie import mainWindowMain


def main():
    """ Run Meggie main window.
    """
    mainWindowMain.main()

# To start meggie directly from the command-line
if __name__ == '__main__':
    mainWindowMain.main()
