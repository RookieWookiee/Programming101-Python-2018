import sys


def sum_numbers(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()

    return sum(int(x) for x in content.split())


def main():
    _sum = sum_numbers(sys.argv[1])
    print(_sum)


if __name__ == '__main__':
    main()
