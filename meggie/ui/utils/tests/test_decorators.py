import unittest
import sys

from time import sleep

from meggie.ui.utils.decorators import threaded
from meggie.ui.utils.decorators import messaged

from PyQt4 import QtGui

class TestDecorators(unittest.TestCase):

    @threaded
    def _cat(self, says=None):
        sleep(0.1)
        if not says:
            raise Exception("Error: I speak, therefore I am")
        sleep(0.1)
        return says

    @messaged
    def _bird(self, says=None):
        sleep(0.1)
        if not says:
            raise Exception("Error: I sing, therefore I am")
        sleep(0.1)
        return says

    def test_threads_success(self):
        self.assertEqual(self._cat(says='meow'), 'meow',
                         'thread_success failed')

    def test_threads_fail(self):
        with self.assertRaises(Exception):
            self._cat()

    def test_messages_success(self):
        app = QtGui.QApplication(sys.argv)
        self.assertEqual(self._bird(says='tweet'), 'tweet',
                         'messages_success failed')
