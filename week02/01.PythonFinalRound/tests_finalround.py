import unittest
from finalround import (
        is_number_balanced,
         increasing_or_decreasing,
         get_largest_palindrome,
         sum_of_numbers,
         birthday_ranges,
         numbers_to_message,
         message_to_numbers,
         elevator_trips
)

class FinalRoundTests(unittest.TestCase):
    def tests_is_number_balanced(self):
        with self.subTest('9 -> True'):
            self.assertTrue(is_number_balanced(9))

        with self.subTest('4518 -> True'):
            self.assertTrue(is_number_balanced(4518))

        with self.subTest('28471 -> False'):
            self.assertFalse(is_number_balanced(28471))

        with self.subTest('1238033 -> True'):
            self.assertTrue(is_number_balanced(1238033))

    def tests_increasing_or_decreasing(self):
        with self.subTest('[1 2 3 4 5] -> "Up!"'):
            self.assertEqual(increasing_or_decreasing([1, 2, 3, 4, 5]), 'Up!')

        with self.subTest('[5, 6, -10] -> False'):
            self.assertFalse(increasing_or_decreasing([5, 6, -10]))

        with self.subTest('[1, 1, 1, 1] -> False'):
            self.assertFalse(increasing_or_decreasing([1, 1, 1, 1]))

        with self.subTest('[9, 8, 7, 6] -> "Down!"'):
            self.assertEqual(increasing_or_decreasing([9, 8, 7, 6]), 'Down!')

    def tests_largest_palindrome(self):
        with self.subTest('[99, 252, 994687, 754649] -> [88, 242, 252, 994687, 754649]'):
            inputs = [99, 252, 994687, 754649]
            outputs = [88, 242, 994499, 754457] 

            for _in, out in zip(inputs, outputs):
                self.assertEqual(get_largest_palindrome(_in), out)

    def tests_sum_of_numbers(self):
        with self.subTest('''["ab125cd3", "ab12", "ab", "1101", "1111O", "1abc33xyz22", "0hfabnek"] -> 
                             [128, 12, 0, 1101, 1111, 56, 0]'''):
            inputs = ["ab125cd3", "ab12", "ab", "1101", "1111O", "1abc33xyz22", "0hfabnek"] 
            outputs = [128, 12, 0, 1101, 1111, 56, 0]

            for _in, out in zip(inputs, outputs):
                self.assertEqual(sum_of_numbers(_in), out)

    def tests_birthday_ranges(self):
        with self.subTest('happy path 1'):
            actual = birthday_ranges([1, 2, 3, 4, 5], [(1, 2), (1, 3), (1, 4), (1, 5), (4, 6)])
            expected = [2, 3, 4, 5, 2]
            self.assertEqual(actual, expected)

        with self.subTest('happy path 2'):
            actual = birthday_ranges([5, 10, 6, 7, 3, 4, 5, 11, 21, 300, 15], [(4, 9), (6, 7), (200, 225), (300, 365)])
            expected = [5, 2, 0, 1]
            self.assertEqual(actual, expected)

    def tests_numbers_to_message(self):
        with self.subTest('happy path 1'):
            actual = numbers_to_message([2, -1, 2, 2, -1, 2, 2, 2])
            expected = 'abc'
            self.assertEqual(actual, expected)

        with self.subTest('happy path 2'):
            actual = numbers_to_message([2, 2, 2, 2])
            expected = 'a'
            self.assertEqual(actual, expected)

        with self.subTest('happy path 3'):
            actual = numbers_to_message([1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 7, 7, 7, 7, 2, 6, 6, 3, 2])
            expected = 'Ivo e Panda'
            self.assertEqual(actual, expected)

    def tests_message_to_numbers(self):
        with self.subTest('"abc"'):
            actual = message_to_numbers('abc')
            expected = [2, -1, 2, 2, -1, 2, 2, 2]
            self.assertEqual(actual, expected)

        with self.subTest('"a" -> [2]'):
            actual = message_to_numbers('a')
            self.assertEqual(actual, [2])

        with self.subTest('"Ivo e Panda"'):
            actual = message_to_numbers('Ivo e Panda')
            expected = [1, 4, 4, 4, 8, 8, 8, 6, 6, 6, 0, 3, 3, 0, 1, 7, 2, 6, 6, 3, 2]
            self.assertEqual(actual, expected)

        with self.subTest('aabbcc'):
            actual = message_to_numbers('aabbcc')
            expected = [2, -1, 2, -1, 2, 2, -1, 2, 2, -1, 2, 2, 2, -1, 2, 2, 2]
            self.assertEqual(actual, expected)

    def test_elevator_trips(self):
        with self.subTest('invalid input 1'):
            actual = elevator_trips([], [], 5, 2, 200)
            expected = 0
            self.assertEqual(actual, expected)

        with self.subTest('invalid input 2'):
            actual = elevator_trips([40, 50], [], 5, 2, 200)
            expected = 0
            self.assertEqual(actual, expected)

        with self.subTest('valid input 1'):
            actual = elevator_trips([40, 40, 100, 80, 60], [2, 3, 3, 2, 3], 3, 5, 200)
            expected = 6
            self.assertEqual(actual, expected)

        with self.subTest('valid input 2'):
            actual = elevator_trips([80, 60, 40], [2, 3, 5], 5, 2, 200)
            expected = 5
            self.assertEqual(actual, expected)
