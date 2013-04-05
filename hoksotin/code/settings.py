'''
Created on Mar 28, 2013

@author: jaeilepp
'''
import re


class Settings(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def validate_int(self, value, min, max):
        """
        Validator for integers.
        
        Keyword arguments:
        value         -- Value to validate
        min           -- Lower limit for the value
        max           -- Upper limit for the value
        """
        if re.match("^-*[0-9,\.]+$", value):
            if int(value) > max or int(value) < min:
                raise Exception('Value out of bounds.')
        else: raise Exception('Use only numbers.')
        return True
        
    def validate_string(self, value):
        """
        Validator for strings.
        
        Keyword arguments:
        value         -- String to validate.
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
        