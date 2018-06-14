from functools import reduce


def char_histogram(s):
    def add_or_update(d, ch):
        d[ch] = 1 if ch not in d else d[ch] + 1
        return d

    return reduce(add_or_update, s, {})


# Problem01
def anagrams(s1, s2):
    s1 = ''.join(x for x in s1 if x != ' ')
    s2 = ''.join(x for x in s2 if x != ' ')

    are_anagrams = char_histogram(s1.lower()) == char_histogram(s2.lower())
    return 'ANAGRAMS' if are_anagrams else 'NOT ANAGRAMS'
