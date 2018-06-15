def chain(*iterables):
    return (x for iterable in iterables for x in iterable)

if __name__ == '__main__':
    print(list(chain([1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 10, 10])))
