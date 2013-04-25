
"""
Boilerplate script to run the application.
Please note that this only works on Unix due to pathname conventions
(slash vs. backslash).
TODO: tested to work on Windows, too
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/code/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/code/externalmodules/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/code/tests/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ui/")


import mainWindow_main  

if __name__ == '__main__':
    mainWindow_main.main()
