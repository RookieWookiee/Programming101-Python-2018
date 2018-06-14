from functools import reduce
from collections import deque


# ---- Helper functions ----
def split_in_two(n):
    n = str(n)
    left_end = (len(n) + 1) // 2
    right_start = len(n) // 2

    return (n[:left_end], n[right_start:])

def palindrome(n):
    left, right = split_in_two(n)
    return left == right[::-1]

def sum_of_digits(n):
    if type(n) is str:
        n = int(n)
    elif type(n) is list:
        n = int(''.join(map(str, n)))

    n = abs(n)
    n = list(str(n))
    return sum(map(int, n))

def group(n):
    def append_or_create(groups, x):
        if len(groups) == 0 or groups[-1][0] != x:
            groups.append([])
        groups[-1].append(x)
        return groups
    
    return reduce(append_or_create, n, [])
# ---- End of Helper functions ----


# Problem01
def is_number_balanced(n):
    halfs = split_in_two(n)
    digit_sums = [sum_of_digits(x) for x in halfs]

    return digit_sums[0] == digit_sums[1]


# Problem02
def increasing_or_decreasing(seq):
    left_shifted = seq[1:]  # Shift to the left by one, no carry

    all_inc = all(x > seq[i] for i, x in enumerate(left_shifted))
    all_dec = all(x < seq[i] for i, x in enumerate(left_shifted))

    return 'Up!' if all_inc else 'Down!' if all_dec else False


# Problem03
def get_largest_palindrome(n):
    return next(filter(palindrome, range(n-1, 0, -1)), None)


# Problem04
def sum_of_numbers(s):
    def group_digits(n): return reduce(append_or_create, n, [])

    def append_or_create(groups, x):
        if len(groups) == 0:
            groups.append([])
        if x.isdigit() == False:
            if(len(groups[-1]) != 0):
                groups.append([])

        if x.isdigit():
            groups[-1].append(x)
        return groups

    numbers = list(map(''.join, group_digits(s)))
    if len(numbers[0]) == 0:
        return 0
    return sum([int(x) for x in numbers if x != ''])


# Problem05
def birthday_ranges(birthdays, ranges):
    birthdays_in_range = [0] * len(ranges)

    for birthday in birthdays:
        for range in enumerate(ranges):
            if birthday >= range[1][0] and birthday <= range[1][1]:
                birthdays_in_range[range[0]] += 1

    return birthdays_in_range


def gen_phone_keyboard():
    # Not exactly triplets
    def append_or_create_triplets(groups, x):
        if x == 's' or x == 'z':
            groups[-1].append(x)
            return groups

        if len(groups) == 0 or len(groups[-1]) >= 3:
            groups.append([])
        groups[-1].append(x)

        return groups

    alphabet = [chr(97+x) for x in range(0, 26)]
    phone_keyboard = reduce(append_or_create_triplets, alphabet, [])
    phone_keyboard.insert(0, [' '])

    return phone_keyboard


# Problem06
def numbers_to_message(numbers):
    SPACE = 0
    CAPITALIZE = 1
    BREAK = -1

    groups = group(numbers)
    phone = gen_phone_keyboard()
    res = []
    capitalize = False

    for g in groups:
        num = g[0]
        if num == BREAK:
            continue
        if num == CAPITALIZE:
            capitalize = True
            continue

        if num == SPACE:
            letter = ' '
        else:
            letter = phone[num-1][(len(g)-1) % len(phone[num-1])]

        if capitalize:
            capitalize = False
            letter = letter.capitalize()

        res.append(letter)

    return ''.join(res)


# Problem06
def message_to_numbers(message):
    phone_keyboard = gen_phone_keyboard()
    numbers_seq = []
    for letter in message:
        if letter.isupper():
            letter = letter.lower()
            numbers_seq.append(1)

        pos = ord(letter) - 97
        key = (pos // 3)+1
        if letter == 's' or letter == 'v' or letter == 'z':
            key -= 1
        elif letter == ' ':
            key = 0

        repeat = phone_keyboard[key].index(letter)+1

        if letter == ' ':
            numbers_seq.append(0)
        else:
            if len(numbers_seq) > 0 and numbers_seq[-1] == key+1:
                numbers_seq.append(-1)
            numbers_seq += [key+1] * repeat

    return numbers_seq[:-1] if numbers_seq[-1] == -1 else numbers_seq


# Problem07
def elevator_trips(p_weight, p_floors, elevator_floors, max_ppl, max_w):
    def takewhile(predicate, iterable):
        count = 0
        total_weight = 0
        result = []

        for x in iterable:
            count += 1
            total_weight += x[0]
            if predicate(count, total_weight):
                result.append(x)
            else:
                break

        return result

    if len(p_weight) == 0 or len(p_floors) == 0:
        return 0
    if any(w > max_w for w in p_weight):
        raise ValueError('Take the stairs')

    p_weight = p_weight[:len(p_floors)]

    people = zip(p_weight, p_floors)
    # Sort by weight, then by floor
    people = deque(x for x in sorted(people, key=lambda p: (p[0], p[1])))
    trips = 0

    while(len(people) > 0):
        batch = takewhile(lambda c, w: c <= max_ppl and w <= max_w, people)
        [people.popleft() for x in batch]
        # +1 because of the return to floor 0
        trips += len(set(x[1] for x in batch)) + 1

    return trips
