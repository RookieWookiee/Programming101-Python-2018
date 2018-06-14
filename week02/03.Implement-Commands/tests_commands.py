import unittest
import os
import sys
from io import StringIO
from contextlib import contextmanager

from cat import cat
from duhs import du

@contextmanager
def captured_output():
    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr

    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err

class CatTests(unittest.TestCase):
    def test_should_work_correctly(self):
        INPUT = ['I am a test', 'I am not really a cat']
        with open('test_cat', 'w') as f:
            f.writelines(INPUT)

        with captured_output() as (out, err):
            cat('test_cat')

        output = out.getvalue().strip()
        self.assertEqual(output, INPUT[0] + INPUT[1])

        try:
            os.remove('test_cat')
        except:
            pass

    def test_should_throw_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            cat('non-existing')

class DiskUsageTests(unittest.TestCase):
    def test_should_throw_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            du('non-existing-path')
