from fractions import *
import unittest


class GcdTests(unittest.TestCase):
    def test_should_return_int(self):
        self.assertIsInstance(gcd(1, 2), int)

    def test_positive_input_should_work_correctly(self):
        self.assertEqual(gcd(2, 4), 2)
        self.assertEqual(gcd(4, 2), 2)
        self.assertEqual(gcd(3, 9), 3)
        self.assertEqual(gcd(3, 12), 3)
        self.assertEqual(gcd(5, 25), 5)
        self.assertEqual(gcd(5, 1), 1)

    def test_negative_input_should_work_correctly(self):
        self.assertEqual(gcd(-2,  4), 2)
        self.assertEqual(gcd(-2, -4), 2)
        self.assertEqual(gcd(+2, -4), 2)

    def test_zero_denominator_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            gcd(1, 0)


class SimplifyFractionTests(unittest.TestCase):
    def test_should_return_tuple(self):
        self.assertIsInstance(simplify_fraction((1, 1)), tuple)
        self.assertEqual(len(simplify_fraction((1, 1))), 2)

    def test_should_raise_type_error(self):
        invalid = [1, '123', [3, 4], ('a', 'a'), ('1', '1'), {1, 2}]
        for _input in invalid:
            with self.assertRaises(TypeError, msg='invalid input: {0}'.format(_input)):
                simplify_fraction(_input)

    def test_zero_denominator_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            simplify_fraction((1, 0))

    def test_positive_input_should_work_correctly(self):
        _input = ((1, 1), (2, 4), (3, 9), (1, 7), (4, 10), (63, 462))
        expect = ((1, 1), (1, 2), (1, 3), (1, 7), (2, 5), (3, 22))

        for x, fx in zip(_input, expect):
            actual = simplify_fraction(x)
            self.assertEqual(actual, fx, msg="x: {0}, expected: {1}, actual: {2}".format(x, fx, actual))


class AddFractionTests(unittest.TestCase):
    def test_should_throw_type_error(self):
        invalid = [(1, 2, 3), '123',
                   [3, 4], ('a', 'a'),
                   ('1', '1'), {1, 2},
                   [(1, 2), (1, 2, 3)]]

        for _input in invalid:
            with self.assertRaises(TypeError, msg='invalid input: {0}'.format(_input)):
                add_fraction(_input, _input)

    def test_should_return_tuple(self):
        self.assertIsInstance(add_fraction((1, 1), (1, 1)), tuple)
        self.assertEqual(len(add_fraction((1, 1), (1, 1))), 2)

    def test_zero_denominator_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            add_fraction((1, 1), (1, 0))

    def test_should_work_correctly(self):
        self.assertEqual(add_fraction((1, 2), (1, 2)), (1, 1))
        self.assertEqual(add_fraction((1, 2), (-1, 2))[0], 0)
        self.assertEqual(add_fraction((-1, 2), (-1, 2)), (-1, 1))
        self.assertEqual(add_fraction((-1, -2), (-1, 2))[0], 0)


class CollectFractionsTests(unittest.TestCase):
    def test_should_return_tuple_of_ints(self):
        fx = collect_fractions([(1, 1)])

        self.assertIsInstance(fx, tuple)
        self.assertEqual(len(fx), 2)
        self.assertIsInstance(fx[0], int)
        self.assertIsInstance(fx[1], int)

    def test_should_raise_type_error(self):
        invalid = [(1, 2, 3), '123',
                   [3, 4], ('a', 'a'),
                   ('1', '1'), {1, 2},
                   [(1, 2), (1, 2, 3)]]

        for _input in invalid:
            with self.assertRaises(TypeError, msg='invalid input: {0}'.format(_input)):
                collect_fractions(_input)

    def test_should_raise_value_error(self):
        _input = [(1, 1), (1, 1), (1, 1), (1, 0)]
        with self.assertRaises(ValueError):
            collect_fractions(_input)

    def test_should_return_correct_result(self):
        self.assertEqual(collect_fractions([(1, 1), (1, 1), (1, 1)]), (3, 1))
        self.assertEqual(collect_fractions([(1, 2), (1, 2)]), (1, 1))
        self.assertEqual(collect_fractions([(-1, -2), (-1, -2)]), (1, 1))
        self.assertEqual(collect_fractions([(0, 1), (1, 8)]), (1, 8))
        self.assertEqual(collect_fractions([(1, 2), (1, 4)]), (3, 4))
        self.assertEqual(collect_fractions([(1, 2), (2, 8)]), (3, 4))
        self.assertEqual(collect_fractions([(1, 7), (2, 6)]), (10, 21))

    def test_sum_0_should_work_correctly(self):
        self.assertEqual(collect_fractions([(1, 2), (-1, 2)])[0], 0)
        self.assertEqual(collect_fractions([(-1, 2), (1, 2)])[0], 0)
        self.assertEqual(collect_fractions([(1, 2), (1, -2)])[0], 0)
        self.assertEqual(collect_fractions([(1, -2), (1, 2)])[0], 0)
        self.assertEqual(collect_fractions([(-1, -2), (-1, 2)])[0], 0)


class SortFractionsTests(unittest.TestCase):
    def test_should_work_correctly(self):
        self.assertEqual(sort_fractions([(2, 3), (1, 2)]), [(1, 2), (2, 3)])
        self.assertEqual(sort_fractions([(2, 3), (1, 2), (1, 3)]), [(1, 3), (1, 2), (2, 3)])
        self.assertEqual(sort_fractions([(5, 6), (22, 78), (22, 7), (7, 8), (9, 6), (15, 32)]), [(22, 78), (15, 32), (5, 6), (7, 8), (9, 6), (22, 7)])


if __name__ == '__main__':
    unittest.main()
