from polynomial import Polynomial
from term import Term as T
import unittest


class PolynomialBasicClassFunctionalityTests(unittest.TestCase):
    def tests_len(self):
        with self.subTest('3x^3+5 len should be 3'):
            p1 = Polynomial(T(coeff=3, var='x', power=3), T(coeff=5, var='x', power=0))
            self.assertEqual(len(p1), 3)

        with self.subTest('3x^4 + 3x^3 len should be 4'):
            p2 = Polynomial(T(coeff=3, var='x', power=4), T(coeff=3, var='x', power=3))
            self.assertEqual(len(p2), 4)

        with self.subTest('3 len should be 0'):
            p3 = Polynomial(T(coeff=3, var='x', power=0))
            self.assertEqual(len(p3), 0)

        with self.subTest('0x^3 + 5 len should ignore term with coeff == 0'):
            p = Polynomial(T(coeff=0, var='x', power=3), T.constant(5))
            self.assertEqual(len(p), 0)

    def tests_init(self):
        with self.subTest('Empty ctor raises ValueError'):
            with self.assertRaises(ValueError):
                Polynomial()

    def tests_parse(self):
        with self.subTest('3x^3 + 5 multiple terms'):
            expected = Polynomial(T(coeff=3, var='x', power=3), T.constant(5))
            self.assertEqual(Polynomial.parse('3x^3+5'), expected)

        with self.subTest('3x^3+2x^2+1x+1 multiple terms'):
            expected = Polynomial(T(coeff=3, var='x', power=3), T(coeff=2, var='x', power=2),
                                  T(coeff=1, var='x', power=1), T.constant(1))

            self.assertEqual(Polynomial.parse('3x^3+2x^2+1x+1'), expected)

        with self.subTest('single constant term'):
            expected = Polynomial(T.constant(5))
            self.assertEqual(Polynomial.parse('5'), expected)

    def tests_equals(self):
        with self.subTest("3x^1 + 3x^2 == 3x^2 + 3x^1 -> True: should be associative when coeffs are equal"):
            p1 = Polynomial(T(coeff=3, var='x', power=1), T(coeff=3, var='x', power=2))
            p2 = Polynomial(T(coeff=3, var='x', power=2), T(coeff=3, var='x', power=1))

            self.assertEqual(p1, p2)

        with self.subTest('3x^2 + 2x^2 == 2x^2 + 3x^2 -> True: should be associative when powers are equal'):
            p1 = Polynomial(T(coeff=3, var='x', power=2), T(coeff=2, var='x', power=2))
            p2 = Polynomial(T(coeff=2, var='x', power=2), T(coeff=3, var='x', power=2))

            self.assertEqual(p1, p2)

        with self.subTest('3x^1 == 4x^1 -> False: same powers diff coeffs'):
            p1 = Polynomial(T(coeff=3, var='x', power=1))
            p2 = Polynomial(T(coeff=4, var='x', power=1))

            self.assertFalse(p1 == p2)

        with self.subTest('3x^1 == 3x^2 -> False: same coeffs diff powers'):
            p1 = Polynomial(T(coeff=3, var='x', power=1))
            p2 = Polynomial(T(coeff=3, var='x', power=2))

            self.assertFalse(p1 == p2)

        with self.subTest('2x^1 == 3x^2 -> False'):
            p1 = Polynomial(T(coeff=2, var='x', power=1))
            p2 = Polynomial(T(coeff=3, var='x', power=2))

            self.assertFalse(p1 == p2)

    def tests_cardinalilty(self):
        with self.subTest('(3x^1 + 5).cardinality -> 2'):
            p = Polynomial(T(coeff=3, var='x', power=1), T.constant(5))
            self.assertEqual(p.cardinality, 2)

        with self.subTest('(5).cardinality -> 1'):
            p = Polynomial(T.constant(5))
            self.assertEqual(p.cardinality, 1)

        with self.subTest('3x^1 + 3x^1 + 3x^1 + 3x^1 -> 4'):
            p = Polynomial(*[T(coeff=3, var='x', power=1) for _ in range(4)])
            self.assertEqual(p.cardinality, 4)


class PolynomialMathOperationsTests(unittest.TestCase):
    def tests_addition(self):
        with self.subTest('3x^1 + 2x^1 -> 5x^1: equal powers should add coeffs'):
            p1 = Polynomial(T(coeff=3, var='x', power=1))
            p2 = Polynomial(T(coeff=2, var='x', power=1))

            self.assertEqual(p1 + p2, Polynomial(T(coeff=5, var='x', power=1)))

        with self.subTest('(3x^1) + (2x^2 + 0x^3) -> 2x^2 + 3x^1: diff powers should not add coeffs'):
            p1 = Polynomial(T(coeff=3, var='x', power=1))
            p2 = Polynomial(T(coeff=2, var='x', power=2), T(coeff=0, var='x', power=3))
            expected = Polynomial(T(coeff=2, var='x', power=2), T(coeff=3, var='x', power=1))

            self.assertEqual(p1 + p2, expected)

        with self.subTest('should be associative'):
            p1 = Polynomial(T(coeff=3, var='x', power=1))
            p2 = Polynomial(T(coeff=2, var='x', power=2))

            self.assertEqual(p1 + p2, p2 + p1)

    def tests_subtraction(self):
        with self.subTest('3x^1 - 2x^1 -> x^1'):
            p1 = Polynomial(T(coeff=3, var='x', power=1))
            p2 = Polynomial(T(coeff=2, var='x', power=1))

            self.assertEqual(p1 - p2, Polynomial(T(coeff=1, var='x', power=1)))

        with self.subTest('x - 2x -> -1x'):
            p1 = Polynomial(T(coeff=1, var='x', power=1))
            p2 = Polynomial(T(coeff=2, var='x', power=1))

            self.assertEqual(p1 - p2, Polynomial(T(coeff=-1, var='x', power=1)))

        with self.subTest('should not be associative'):
            p1 = Polynomial(T(coeff=1, var='x', power=1))
            p2 = Polynomial(T(coeff=2, var='x', power=1))

            self.assertFalse(p1 - p2 == p2 - p1)

    def tests_multiplication(self):
        with self.subTest('2x * 2 -> 4x'):
            p1 = Polynomial(T(coeff=2, var='x', power=1))
            p2 = Polynomial(T.constant(2))

            expected = Polynomial(T(coeff=4, var='x', power=1))
            self.assertEqual(p1 * p2, expected)

        with self.subTest('2x * 2x -> 4x^2'):
            p1 = Polynomial.parse('2x')

            expected = Polynomial.parse('4x^2')
            self.assertEqual(p1 * p1, expected)

        with self.subTest('(x^2 + 5)*(x^2 + 9x + 9) -> x^4 + 9x^3 + 14x^2 + 45x + 45 '):
            p1 = Polynomial(
                T(coeff=1, var='x', power=2),
                T.constant(5)
            )
            p2 = Polynomial(
                T(coeff=1, var='x', power=2),
                T(coeff=9, var='x', power=1),
                T.constant(9)
            )

            expected = Polynomial(
                T(coeff=1, var='x', power=4),
                T(coeff=9, var='x', power=3),
                T(coeff=14, var='x', power=2),
                T(coeff=45, var='x', power=1),
                T.constant(45)
            )

            self.assertEqual(p1 * p2, expected)

        with self.subTest('should be associative'):
            p1 = Polynomial(T(coeff=2, var='x', power=1))
            p2 = Polynomial(T.constant(2))

            self.assertEqual(p1 * p2, p2 * p1)

    def tests_derivative(self):
        with self.subTest('zero or negative derivative should raise value error'):
            with self.assertRaises(ValueError):
                p = Polynomial(T.constant(3))
                p.derivative(0)

        with self.subTest('first derivative (3x^3 + 4x^2 + 2x^1 + 5) -> 9x^2 + 8x + 2'):
            p = Polynomial(
                    T(coeff=3, var='x', power=3),
                    T(coeff=4, var='x', power=2),
                    T(coeff=2, var='x', power=1),
                    T(coeff=5, var='x', power=0)
                )
            expected = Polynomial(
                    T(coeff=9, var='x', power=2),
                    T(coeff=8, var='x', power=1),
                    T(coeff=2, var='x', power=0),
                    T(coeff=0, var='x', power=0)
                )

            self.assertEqual(p.derivative(), expected)

        with self.subTest('second derivative (2x^3 + 3x^2) -> 12x + 6'):
            p = Polynomial(T(coeff=2, var='x', power=3), T(coeff=3, var='x', power=2))
            expected = Polynomial(T(coeff=12, var='x', power=1), T(coeff=6, var='x', power=0))

            self.assertEqual(p.derivative(2), expected)

        with self.subTest('third derivative (2x^3 + 3x^1 + 2) -> 12'):
            p = Polynomial(T(coeff=2, var='x', power=3), T(coeff=3, var='x', power=1), T(coeff=2, var='x', power=0))
            expected = Polynomial(T(coeff=12, var='x', power=0), T(coeff=0, var='x', power=0), T(coeff=0, var='x', power=0))

            self.assertEqual(p.derivative(3), expected)

        with self.subTest('third derivative 3x -> 0'):
            p = Polynomial(T(coeff=3, var='x', power=1))
            expected = Polynomial(T(coeff=0, var='x', power=0))

            self.assertTrue(p.derivative(3) == expected)


if __name__ == '__main__':
    unittest.main()
