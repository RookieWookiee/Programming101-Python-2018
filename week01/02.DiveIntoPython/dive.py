import math
import operator
from functools import reduce


# Problem01
def count_substrings(haystack, needle): return haystack.count(needle)


# Problem02
def sum_matrix(m): return sum(reduce(operator.add, m))


# Problem03
def nan_expand(n):
    expanded = reduce(lambda a, x: a + 'Not a ', range(0, n), '') + 'NaN'
    return '' if n == 0 else expanded


# Holy shit...
def factorize_v1(primes, n, fact=None, prod=1):
    if fact is None:
        fact = []
    if n == prod:
        return fact

    for p in reversed(primes):
        i = 1

        while(prod * p ** i <= n):
            fact.append((p, i))
            len_before = len(fact)
            factorize_v1(primes, n, fact, prod * (p ** i))

            if prod * (fact[-1][0] ** fact[-1][1]) == n:
                return fact
            if len_before != len(fact):
                return fact
            else:
                fact.pop()
            i += 1


def factorize_v2(primes, n):
    factors = []
    while(n > 1):
        for p in primes:
            if n % p == 0:
                n //= p
                factors.append(p)
                break

    print(factors)


# Problem04 Helper
def sieve(n):
    primes = [True] * (n+1)
    primes[0] = primes[1] = False

    for i in range(2, int(math.ceil(math.sqrt(n)))):
        if primes[i] is True:
            j = 2
            while(i * j <= n):
                primes[i * j] = False
                j += 1

    return [x[0] for x in enumerate(primes) if x[1] is True]


# Problem04
def prime_factorization(n):
    def factorize_v3(n, primes=None, fact=None):
        if fact is None:
            fact = []
        if primes is None:
            primes = sieve(n)
        if n == 1:
            return fact

        for p in primes:
            if n % p is 0:
                return factorize_v3(n // p, primes, fact + [p])

    factors = factorize_v3(n)
    return [(x[0], len(x)) for x in group(factors)]


# Problem05
def group(n):
    def append_or_create(groups, x):
        if len(groups) == 0 or groups[-1][0] != x:
            groups.append([])
        groups[-1].append(x)
        return groups
    return reduce(append_or_create, n, [])


# Problem06
def max_consecutive(n):
    return len(reduce(lambda a, x: x if len(x) > len(a) else a, group(n)))


# Problem07 Helper
def match(matrix, from_row, from_col, keyword, memo_thing):
    directions = [{'dx': +1, 'dy': -1}, {'dx': +1, 'dy': +1},  # Diagonals
                  {'dx': -1, 'dy': +1}, {'dx': -1, 'dy': -1},
                  {'dx': +1, 'dy': 0}, {'dx': 0, 'dy': +1},  # Straigts
                  {'dx': -1, 'dy': 0}, {'dx': 0, 'dy': -1}]
    # Diagonals - clockwise; Straights - right, down, left, up
    count = 0

    for _dir in directions:
        i = 0
        start_row, start_col = from_row, from_col
        while True:
            curr_row = from_row + i * _dir['dy']
            curr_col = from_col + i * _dir['dx']

            if curr_row < 0 or curr_row >= len(matrix):
                break
            if curr_col < 0 or curr_col >= len(matrix[curr_row]):
                break
            if(i >= len(keyword)):
                break
            if(matrix[curr_row][curr_col] != keyword[i]):
                break

            if(matrix[curr_row][curr_col] == keyword[-1] and
                    i == len(keyword) - 1):
                # Match found.
                start_pos = (start_row, start_col)
                end_pos = (curr_row, curr_col)
                location_of_match = (start_pos, end_pos)
                # If already encountered -> palindrome -> break;
                if(location_of_match in memo_thing):
                    break
                # Push (end_pos, start_pos). This is the potential palindrome,
                # that we check against before pushing.
                memo_thing.append((end_pos, start_pos))
                count += 1
            i += 1

    return count


# Problem07 Helper
def count_occurences(matrix, keyword):
    count = 0
    memo_thing = []
    for row_idx, row in enumerate(matrix):
        for col_idx, elem in enumerate(matrix[row_idx]):
            if(elem == keyword[0]):
                count += match(matrix, row_idx, col_idx, keyword, memo_thing)

    return count


# Problem07
def word_counter():
    search_word = input()
    matrix = []
    dimensions = [int(x) for x in input().split()]

    try:
        matrix = [input().split() for i in range(dimensions[0])]
    except EOFError:
        print('Invalid number of rows or columns!')
        return

    count_occurences(matrix, search_word)


# Problem08
def gas_stations(distance, tank_size, stations):
    remaining_fuel = tank_size
    strategy = []
    stations.insert(0, 0)
    stations.append(distance)

    for i in range(0, len(stations)-1):
        dist_to_next = stations[i+1] - stations[i]
        if dist_to_next >= remaining_fuel:
            strategy.append(stations[i])
            remaining_fuel = tank_size
        remaining_fuel -= dist_to_next

    return strategy
