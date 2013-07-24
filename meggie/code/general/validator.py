# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
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
Created on Mar 28, 2013

@author: Jaakko Leppakangas
Contains the Validator-class for validating different types.
"""
import re


class Validator(object):
    """
    Contains validators for different types.
    """
    

    def __init__(self):
        pass
        
    def validate_int(self, value, min, max):
        """
        Validator for integers.
        
        Keyword arguments:
        value         -- Value to validate
        min           -- Lower limit for the value
        max           -- Upper limit for the value
        Raises an exception if the value is over the given boundaries.
        Raises an exception if value is not an integer.
        """
        if re.match("^-*[0-9,\.]+$", value):
            if int(value) > max or int(value) < min:
                raise Exception('Value out of bounds.')
        else:
            raise Exception('Use only numbers.')
        return True
        
    def validate_string(self, value):
        """
        Validator for strings.
        
        Keyword arguments:
        value         -- String to validate.
        Raises an exception if the value is not a string.
        """
        if re.match("^[a-zA-Z0]+$", value):
            return True
        else: raise Exception('Use only letters.')
        
    def validate_float(self, value, min, max):
        """
        Validator for floats.
        
        Keyword arguments:
        value         -- Value to validate
        min           -- Lower limit for the value
        max           -- Upper limit for the value
        """
    
    def validate_channelList(self, channelList):
        """
        Checks whether the channels in channelList are valid MEG channels.
        The channels must be already stripped of the 'MEG' string in the
        beginning, i.e. must be of the form 0222, 0223 etc.
        
        Keyword arguments:
        channelList   -- list of channels to check
        
        """
        
        for channel in channelList:
            if channel
            
            
        
        