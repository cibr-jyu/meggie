""" Helpers related to identifiers
"""
import uuid


def generate_uid():
    """ Generates uid that is 8 characters long. """
    return uuid.uuid4().hex[0:8]

