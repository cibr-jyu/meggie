
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
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/code/epoching/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/code/preprocessing/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/code/general/")

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ui/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ui/widgets/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ui/epoching/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ui/general/")
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/ui/preprocessing/")


import mainWindow_main  

if __name__ == '__main__':
    mainWindow_main.main()
