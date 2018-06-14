import sys
from parser import Parser


if __name__ == '__main__':
    parser = Parser(sys.argv[1])
    aggregate = AggregateMoneyTracker(parser)
