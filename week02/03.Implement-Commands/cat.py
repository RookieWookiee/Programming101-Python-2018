import sys


def cat(f):
    f = open(f, 'r')
    print(f.read())
    f.close()


def main():
    for f in sys.argv[1:]:
        try:
            cat(f)
        except FileNotFoundError as e:
            print(e)


if __name__ == '__main__':
    main()
