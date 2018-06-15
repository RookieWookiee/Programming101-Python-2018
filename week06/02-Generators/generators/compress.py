def compress(iterable, mask):
    return (x[0] for x in zip(iterable, mask) if x[1])

if __name__ == '__main__':
    print(list(compress(['a', 'b', 'c'], [False, True, False])))
