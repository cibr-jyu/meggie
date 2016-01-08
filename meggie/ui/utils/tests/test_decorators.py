import unittest
import sys

from time import sleep

from meggie.ui.utils.decorators import threaded
from meggie.ui.utils.decorators import messaged

class TestDecorators(unittest.TestCase):

    @threaded
    def _cat(self, says=None):
        sleep(0.1)
        if not says:
            raise Exception("Error: I speak, therefore I am")
        sleep(0.1)
        return says

    def test_threads_success(self):
        self.assertEqual(self._cat(says='meow'), 'meow',
                         'thread_success failed')

    def test_threads_fail(self):
        with self.assertRaises(Exception):
            self._cat()
