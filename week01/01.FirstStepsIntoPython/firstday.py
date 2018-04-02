import operator

from functools import reduce


# Problem01
def sum_of_digits(n):
    if type(n) is str:
        n = int(n)
    elif type(n) is list:
        n = int(''.join(map(str, n)))

    n = abs(n)
    n = list(str(n))
    n = map(int, n)

    return sum(n)


# Problem02
def to_digits(n):
    return [int(x) for x in list(str(n))]


# Problem03
def to_number(digits):
    return int(''.join(str(x) for x in digits))


# Problem04
def fact_digits(n):
    def fact(n):
        if n == '0': return 1
        return reduce((lambda x, y: x * y), range(1, int(n)+1))

    return sum(fact(digit) for digit in str(n))


# Problem05
def fibonacci(n):
    result = []
    a, b = 0, 1

    for i in range(0, n):
        c = a + b
        result.append(b)
        a, b = b, c

    return result


# Problem06
def fib_number(n): return reduce(operator.add, (map(str, fibonacci(n))))


def split_in_two(n):
    n = str(n)
    left_end = (len(n)+1)//2
    right_start = len(n)//2

    return (n[:left_end], n[right_start:])

# Problem07
def palindrome(n):

    l = split_in_two(n)
    return l[0] == l[1][::-1]


# Problem 08, 09 helper
def count_letters(letters_str, str): return sum(x in letters_str for x in str)


# Problem08
def count_vowels(str): return count_letters(_vowels, str.lower())
_vowels = "aoeiuy"


# Problem09
def count_consonants(str): return count_letters(_consonants, str.lower())
_consonants = "bcdfghjklmnpqrstvwxz"


# Problem10
def char_histogram(str):
    def add_or_update(d, ch):
        d[ch] = 1 if ch not in d else d[ch] + 1
        return d

    return reduce(add_or_update, str, {})
