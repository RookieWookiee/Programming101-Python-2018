def to_digits(n):
    return list(map(int, list(str(n))))


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
def is_credit_card_valid(number):
    digits = to_digits(number)
    if len(digits) % 2 == 0:
        return False
    res = [x[1]*2 if x[0] % 2 != 0 else x[1] for x in enumerate(digits)]

    return sum_of_digits(res) % 10 == 0
