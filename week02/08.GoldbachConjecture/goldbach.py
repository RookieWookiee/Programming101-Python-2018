import math


def sieve(n):
    primes = [True] * (n+1)
    primes[0] = primes[1] = False

    for i in range(2, int(math.ceil(math.sqrt(n)))):
        if primes[i]:
            j = 2
            while(i * j <= n):
                primes[i * j] = False
                j += 1

    return [x[0] for x in enumerate(primes) if x[1] is True]


# Problem04
def goldbach(n):
    primes = sieve(n)
    primes_lookup = set(primes)
    result = []
    result_lookup = set()

    for p in primes:
        if n - p in primes_lookup and (n - p, p) not in result_lookup:
            result.append((p, n - p))
            result_lookup.add((p, n - p))

    return result
