from term import Term
import unittest


class TermBasicClassFunctionalityTests(unittest.TestCase):
    def tests_parse(self):
        with self.subTest("2*x^3: explicit '*' explicit '^'"):
            self.assertEqual(Term.parse('2*x^3'), Term(coeff=2, var='x', power=3))

        with self.subTest('x^3: implicit coeff = 1'):
            self.assertEqual(Term.parse('x^3'), Term(coeff=1, var='x', power=3))

        with self.subTest("10: implicit 'x^0'"):
            self.assertEqual(Term.parse('10'), Term(coeff=10, var='x', power=0))

        with self.subTest("10*x: implicit '^1'"):
            self.assertEqual(Term.parse('10*x'), Term(coeff=10, var='x', power=1))

        with self.subTest("10x: implicit '*', implicit '^1'"):
            self.assertEqual(Term.parse('10x'), Term(coeff=10, var='x', power=1))

        with self.subTest("100x^0: three digit coeff"):
            self.assertEqual(Term.parse('100x^0'), Term(coeff=100, var='x', power=0))

    def tests_constant(self):
        with self.subTest('Term 3 power should be 0'):
            t = Term.constant(3)
            self.assertEqual(t.power, 0)

        with self.subTest('Term 3 coeff should be 3'):
            t = Term.constant(3)
            self.assertEqual(t.coeff, 3)

        with self.subTest('Term 3 is_constant should be True'):
            t = Term.constant(3)
            self.assertTrue(t.is_constant)


class TermMathOperationsTests(unittest.TestCase):
    def tests_add(self):
        with self.subTest('1x^2 + 3x^2 -> 4 coeff'):
            t1 = Term(coeff=1, var='x', power=2)
            t2 = Term(coeff=3, var='x', power=2)

            actual = t1 + t2
            self.assertEqual(actual.coeff, 4)

        with self.subTest('1x^2 + 3x^2 -> 2 power'):
            t1 = Term(coeff=1, var='x', power=2)
            t2 = Term(coeff=3, var='x', power=2)

            actual = t1 + t2
            self.assertEqual(actual.power, 2)

        with self.subTest('1x^2 + 1x^3 -> raise ValueError'):
            t1 = Term(coeff=1, var='x', power=2)
            t2 = Term(coeff=1, var='x', power=3)

            with self.assertRaises(ValueError):
                t1 + t2

    def tests_sub(self):
        with self.subTest('3x^2 - 2x^2 -> 1 coeff'):
            t1 = Term(coeff=3, var='x', power=2)
            t2 = Term(coeff=2, var='x', power=2)

            actual = t1 - t2
            self.assertEqual(actual.coeff, 1)

        with self.subTest('3x^2 - 2x^2 -> 2 power'):
            t1 = Term(coeff=3, var='x', power=2)
            t2 = Term(coeff=2, var='x', power=2)

            actual = t1 - t2
            self.assertEqual(actual.power, 2)

        with self.subTest('3x^2 - 3x^3 -> raise ValueError'):
            with self.assertRaises(ValueError):
                Term(coeff=3, var='x', power=2) - Term(coeff=3, var='x', power=3)

    def tests_derivative(self):
        with self.subTest('x -> 1'):
            t = Term(coeff=1, var='x', power=1)

            self.assertEqual(t.derivative(), Term.constant(1))

        with self.subTest('2x^2 -> 4x'):
            t = Term(coeff=2, var='x', power=2)
            expected = Term(coeff=4, var='x', power=1)

            self.assertEqual(t.derivative(), expected)

        with self.subTest('2 -> 0'):
            t = Term.constant(2)

            self.assertEqual(t.derivative(), Term.constant(0))

        with self.subTest('0x^3 -> 0'):
            t = Term(coeff=0, var='x', power=3)

            self.assertEqual(t.derivative(), Term.constant(0))

        with self.subTest('-3x^2 -> -6x'):
            t = Term(coeff=-3, var='x', power=2)
            expected = Term(coeff=-6, var='x', power=1)

            self.assertEqual(t.derivative(), expected)

        with self.subTest('-6x -> -6'):
            t = Term(coeff=-6, var='x', power=1)

            self.assertEqual(t.derivative(), Term.constant(-6))


if __name__ == '__main__':
    unittest.main()
