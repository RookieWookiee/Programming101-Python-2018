import unittest
from chain import chain

class TestChain(unittest.TestCase):
    def test_chain1(self):
        actual = list(chain([1, 2, 3], [4, 5, 6]))
        self.assertEqual(actual, [1, 2, 3, 4, 5, 6])
