import unittest
from functools import reduce
from operator import mul


def sum_of_digits(number):
    if type(number) is not int:
        raise TypeError('number should be an integer but it is ' + str(type(number)))

    number = abs(number)
    return sum(int(d) for d in str(number))


def to_digits(n):
    if type(n) is not int:
        raise TypeError("n should be 'int' but it is " + str(type(n)))
    n = abs(n)
    return [int(d) for d in list(str(n))]


def to_number(digits):
    if type(digits) is not list:
        raise TypeError('digits should be list, but it is {0}'.format(type(digits)))
    if any(x < 0 for x in digits):
        x, _ = next(filter(lambda x: x[1] < 0, enumerate(digits)))
        raise ValueError('all elements in the sequence should be >= 0, element at index {0} is not'.format(x))

    return int(''.join(str(x) for x in digits))


def fact_digits(n):
    def fact(x):
        if x == 0:
            return 1
        return reduce(mul, range(1, x+1))

    if type(n) is not int:
        raise TypeError('n should be int, but it is {0}'.format(type(n)))
    if n < 0:
        n = abs(n)

    return sum(fact(int(x)) for x in list(str(n)))


class SumOfDigitsTests(unittest.TestCase):
    def test_zero_tests_correctness(self):
        self.assertEqual(sum_of_digits(123), 6)
        self.assertEqual(sum_of_digits(1325132435356), 43)
        self.assertEqual(sum_of_digits(6), 6)

    def test_negative_input_should_return_1(self):
        self.assertEqual(sum_of_digits(-10), 1)

    def test_big_number_should_return_1(self):
        self.assertEqual(sum_of_digits(1000000000000000000000000000000000000000000000000000000000000000000000000), 1)

    def test_valid_input_should_return_int(self):
        self.assertEqual(type(sum_of_digits(1123123123123123)), int)

    def test_input_string_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            sum_of_digits('123')

    def test_input_none_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            sum_of_digits(None)


class ToDigitsTests(unittest.TestCase):
    def test_should_return_123_as_list(self):
        self.assertEqual(to_digits(123), [1, 2, 3])

    def test_should_return_321_as_list(self):
        self.assertEqual(to_digits(321), [3, 2, 1])

    def test_input_string_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            to_digits('asdfasdf')

    def test_input_number_as_string_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            to_digits('123')

    def test_negative_number_should_return_five_ones_as_list(self):
        self.assertEqual(to_digits(---1111), [1, 1, 1, 1])

    def test_valid_input_should_return_list(self):
        self.assertEqual(type(to_digits(1)), list)

    def test_valid_input_should_return_non_empty_list(self):
        self.assertGreater(len(to_digits(1)), 0)

    def test_valid_input_all_elements_should_be_ints(self):
        self.assertTrue(to_digits(123456789), lambda actual: all(type(x) is int for x in actual))

    def test_valid_input_all_elements_should_be_positive(self):
        self.assertTrue(to_digits(987654321), lambda actual: all(x > 0 for x in actual))


class ToNumberTests(unittest.TestCase):
    def test_list_input_should_return_int(self):
        self.assertIsInstance(to_number([1, 2, 3]), int)

    def test_input_wrong_type_input_should_raise_type_error(self):
        with self.assertRaises(TypeError):
            to_number(1337)

    def test_list_input_negative_number_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            to_number([1, 2, -3, 4, 5])

    def test_valid_input_should_return_non_negative_int(self):
        self.assertGreaterEqual(to_number([1, 2, 3, 4]), 0)

    def test_valid_inputs_should_return_correct_number(self):
        self.assertEqual(to_number([1, 2, 3]), 123)
        self.assertEqual(to_number([21, 2, 3]), 2123)
        self.assertEqual(to_number([9, 9, 9, 9, 9]), 99999)
        self.assertEqual(to_number([1, 2, 3, 0, 2, 3]), 123023)
        self.assertEqual(to_number([0, 0, 0, 1, 2, 3, 0, 2, 3]), 123023)


class FactDigitsTests(unittest.TestCase):
    def test_valid_input_should_return_int(self):
        self.assertIsInstance(fact_digits(111), int)

    def test_invalid_type_input_should_raise_type_error(self):
        for invalid in ['123123', [1, 2, 3, 4], (123, 123), {123, 123}, '1', None]:
            with self.assertRaises(TypeError, msg="input type: {0}".format(type(invalid))):
                fact_digits(invalid)

    def test_single_digit_input_should_calculate_correctly(self):
        factorials = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880]
        for fx, x in zip(factorials, range(10)):
            actual_fx = fact_digits(x)
            self.assertEqual(actual_fx, fx, msg="x: {0}, f(x): {1}".format(x, actual_fx))

    def test_multi_digit_input_should_work_correctly(self):
        _input = [11, 22, 33, 44, 55, 66, 77, 88, 99]
        expected = [2, 4, 12, 48, 240, 1440, 10080, 80640, 725760]
        for expected, x in zip(expected, _input):
            actual = fact_digits(x)
            self.assertEqual(actual, expected, msg="x: {0} expected: {1} actual:{2}"
                             .format(x, expected, actual))

    def test_multi_digit_negative_input_should_work_correctly(self):
        self.assertEqual(fact_digits(-145), 145)


if __name__ == '__main__':
    unittest.main()
