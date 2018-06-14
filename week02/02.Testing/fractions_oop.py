from functools import reduce
import operator


class Fraction:
    def __init__(self, t):
        self.numer, self.denom = t[0], t[1]

        if self.denom == 0:
            raise ValueError('Denominator must be different from 0')

        gcd = self._gcd()
        self.numer, self.denom = self.numer // gcd, self.denom // gcd

    def __add__(self, other):
        res_numer = self.numer * other.denom + other.numer * self.denom
        res_denom = self.denom * other.denom

        return Fraction((res_numer, res_denom))

    def __repr__(self):
        return f'({self.numer}, {self.denom})'

    def _gcd(self):
        a, b = abs(self.numer), abs(self.denom)

        while(b != 0):
            a, b = b, a % b
        return a


def simplify_fraction(f):
    return Fraction(f)


def collect_fractions(fractions):
    fractions = map(Fraction, fractions)
    return reduce(operator.add, fractions)
