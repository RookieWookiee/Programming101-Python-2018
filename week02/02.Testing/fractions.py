from functools import reduce


def gcd(a, b):
    if b is 0:
        raise ValueError('b cannot be zero')
    while(b != 0):
        t = b
        b = a % b
        a = t
    return abs(a)


def simplify_fraction(f):
    if type(f) is not tuple:
        raise TypeError('f must be a tuple')
    if len(f) != 2 or any(type(x) is not int for x in f):
        raise TypeError('f must be a tuple with 2 integers')

    nom, denom = f
    _gcd = gcd(nom, denom)

    return (nom // _gcd, denom // _gcd)


def add_fraction(f1, f2):
    if type(f1) is not tuple or type(f2) is not tuple:
        raise TypeError('f1 and f2 must be tuples')
    if any(type(x) is not int for x in f1) or any(type(x) is not int for x in f2):
        raise TypeError('f1 and f2 must contain only integers')
    if f1[1] == 0 or f2[1] == 0:
        raise ValueError('f1 and f2 must have denominators different from 0')
    if len(f1) != 2 or len(f2) != 2:
        raise TypeError('f1 and f2 must contain 2 integers each')

    nom_f1, nom_f2 = f1[0], f2[0]
    denom_f1, denom_f2 = f1[1], f2[1]
    return simplify_fraction((nom_f1 * denom_f2 + nom_f2 * denom_f1, denom_f1 * denom_f2))


def collect_fractions(l):
    if type(l) is not list:
        raise TypeError('l must be a list')
    if any(type(x) is not tuple or len(x) != 2 for x in l):
        raise TypeError('l must contain only tuples with 2 integers')
    if any(denom == 0 for _, denom in l):
        raise ValueError('Invalid fraction')

    return reduce(add_fraction, l)

def sort_fractions(l):
    def validate_input(l):
        if type(l) is not list:
            raise TypeError('l must be a list')
        if any(type(x) is not tuple for x in l):
            raise TypeError('All elements of l must be tuples')
        if any(type(x) is not int for t in l for x in t):
            raise TypeError('All elements of the tuples must be integers')
        if any(t[1] == 0 for t in l):
            raise ValueError('Invalid fraction')

    validate_input(l)
    return sorted(l, key=lambda x: x[0] / x[1])
