from term import Term
from functools import reduce
import operator


class Polynomial:
    def __init__(self, *terms):
        if len(terms) == 0:
            raise ValueError('There must be at least one term')

        self.terms = sorted(terms, key=lambda x: (x.power, x.coeff, x.var), reverse=True)
        self.terms = tuple(self.terms)

    @classmethod
    def parse(cls, s):
        return cls(*[Term.parse(x) for x in s.split('+')])

    def __len__(self):
        """Length is the biggest power from the terms comprising it."""
        if len(self.terms) == 1 and self.terms[0].coeff == 0:
            return 0

        return next(x.power for x in self.terms if x.coeff != 0)

    def __repr__(self):
        return self.terms.__repr__()

    def __str__(self):
        return ' + '.join(map(str, (x for x in self.terms if x.coeff != 0)))

    def __iter__(self):
        return self.terms.__iter__()

    def __add__(self, other):
        p1, p2 = self.__class__._add_missing_terms(self, other)
        res_terms = tuple(x + y for x, y in zip(p1, p2))

        return self.__class__(*res_terms)

    def __mul__(self, other):
        poly_cls = self.__class__
        polynomials = (poly_cls(*[t1 * t2 for t2 in other]) for t1 in self)
        return reduce(operator.add, polynomials)

    @property
    def cardinality(self):
        return len(self.terms)

    def __sub__(self, other):
        p1, p2 = Polynomial._add_missing_terms(self, other)
        res_terms = tuple(x - y for x, y in zip(p1, p2))

        return self.__class__(*res_terms)

    def eval(self, **kwargs):
        raise NotImplementedError

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if len(self) != len(other):
            return False

        p1, p2 = self.__class__._add_missing_terms(self, other)
        return all(x == y for x, y in zip(p1, p2))

    def derivative(self, order=1):
        if order <= 0:
            raise ValueError('order should be positive integer')

        terms = self.terms
        for i in range(order):
            terms = [x.derivative() for x in terms]

        return self.__class__(*terms)

    @classmethod
    def _add_missing_terms(cls, self, other):
        powers_p1 = set(x.power for x in self)
        powers_p2 = set(x.power for x in other)

        missing_p1 = powers_p2 - powers_p1  # Get those exclusively in p2
        missing_p2 = powers_p1 - powers_p2  # Get those exclusively in p1

        missing_p1_terms = tuple(Term(coeff=0, var='x', power=x) for x in missing_p1)
        missing_p2_terms = tuple(Term(coeff=0, var='x', power=x) for x in missing_p2)

        res_terms_p1 = self.terms + missing_p1_terms
        res_terms_p2 = other.terms + missing_p2_terms

        return (cls(*res_terms_p1), cls(*res_terms_p2))
