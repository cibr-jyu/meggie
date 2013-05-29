# coding: latin1
"""
Created on Mar 28, 2013

@author: Jaakko Leppakangas
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
        