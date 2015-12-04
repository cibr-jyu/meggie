import unittest

from time import sleep

from meggie.ui.utils.decorators import threaded

class TestThreading(unittest.TestCase):

    @threaded
    def _cat(self, says=None):
        sleep(0.3)
        if not says:
            raise Exception("Error: One must meow")
        sleep(0.3)
        return says

    def test_threads_success(self):
        self.assertEqual(self._cat(says='meow'), 'meow',
                         'thread_success failed')

    def test_threads_fail(self):
        with self.assertRaises(Exception):
            self._cat()
