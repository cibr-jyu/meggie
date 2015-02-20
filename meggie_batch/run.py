# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code_meggie must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.


"""
Boilerplate script to run the application.
"""

import sys
import os
import sip

# For interoperability with Canopy and to remove need to mess with QStrings.
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)
os.environ['QT_API'] = 'pyqt'

# To make Meggie user static MNE instead of a possible system one
sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)) + "/externalModules/")

# Recursively append everything in Meggie to syspath to make running from
# command line viable
runpath = os.path.dirname(os.path.abspath(__file__))
for root, dirs, files in os.walk(runpath):
    if runpath is not root:
        sys.path.append(root)

from ui.general import mainWindowMain  
if __name__ == '__main__':
    mainWindowMain.main()