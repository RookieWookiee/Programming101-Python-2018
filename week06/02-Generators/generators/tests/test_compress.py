import unittest

from compress import compress

class TestCompress(unittest.TestCase):
    def test_compress1(self):
        actual = list(compress([1, 2, 3], [False, True, False]))
        self.assertEqual(actual, [2])

    def test_compress2(self):
        actual = list(compress([1, 2, 3, 4], [False, False, False, False]))
        self.assertEqual(actual, [])
