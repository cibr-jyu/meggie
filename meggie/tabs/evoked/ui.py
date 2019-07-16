"""
"""
import logging


def compute(subject, data):
    logging.getLogger('ui_logger').info('compute called for ' + str(subject.subject_name))
