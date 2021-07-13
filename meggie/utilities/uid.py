""" Helpers related to identifiers
"""
import uuid

def generate_uid():
    return uuid.uuid4().hex[0:8]

