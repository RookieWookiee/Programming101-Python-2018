# generate_numbers.py
import sys
from random import randint


def generate_numbers(filename, numbers):
    f = open(filename, 'w')
    nums = [randint(1, 1000) for _ in range(numbers)]
    f.write(' '.join(str(x) for x in nums))
    f.close()


def main():
    try:
        generate_numbers(sys.argv[1], 100)
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    main()
