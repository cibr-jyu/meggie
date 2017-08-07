""" Provides tests for utils package """

import unittest
import sys

from time import sleep

from meggie.ui.utils.decorators import threaded

from PyQt4 import QtGui

class TestDecorators(unittest.TestCase):
    """ Test cases for decorators """

    def setUp(self):
        self.app = QtGui.QApplication(sys.argv)

    def tearDown(self):
        self.app = None

    @staticmethod
    @threaded
    def _cat(says=None):
        """ Cat say something """
        sleep(0.1)
        if not says:
            raise Exception("Error: I speak, therefore I am")
        sleep(0.1)
        return says

    def test_threads_success(self):
        """ Test the threaded cat-function """
        self.assertEqual(TestDecorators._cat(says='meow'), 'meow',
                         'thread_success failed')

    def test_threads_fail(self):
        """ Test for exceptions occuring inside threaded function """
        with self.assertRaises(Exception):
            TestDecorators._cat()
