import unittest
from cycle import cycle

class Cycle(unittest.TestCase):
    def test_cycle1(self):
        numbers = [1, 2, 3]
        gen = cycle(numbers)

        for i in range(1000):
            self.assertEqual(next(gen), numbers[i % len(numbers)])

    def test_cycle2(self):
        numbers = [3, 2, 5, 6]
        gen = cycle(numbers)

        for i in range(100):
            self.assertEqual(next(gen), numbers[i % len(numbers)])
