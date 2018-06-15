from collections import deque, Iterable


def deep_compare(obj1, obj2):
    q1 = deque()
    q2 = deque()
    q1.append(obj1), q2.append(obj2)

    while q1 or q2:
        item1, item2 = q1.pop(), q2.pop()
        if item1 != item2:
            return False
        if type(item1) != type(item2):
            return False

        if isinstance(item1, dict):
            if type(item1) != type(item2):
                return False

            sorted_iter = zip(sorted(item1.items()), sorted(item2.items()))
            for kvp1, kvp2 in sorted_iter:
                q1.append(kvp1[1])
                q2.append(kvp2[1])

        elif (isinstance(item1, Iterable)
                and type(item1) is not str):
            for v1, v2 in zip(sorted(item1), sorted(item2)):
                q1.append(v1)
                q2.append(v2)

    return True


d1 = {
    1: {2, 3, 1},
    2: (1, 2),
    3: [1, 2, 2],
    4: {
        'b': 'B',
        'a': 'A',
    }
}

d2 = {
    2: (1, 2),
    3: [1, 2, 2],
    1: {1, 2, 3},
    4: {
        'a': 'A',
        'b': 'B',
    }
}

print(deep_compare(d1, d2))
