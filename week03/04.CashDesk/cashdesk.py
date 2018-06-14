from functools import reduce
import operator
import os


class Bill:
    def __init__(self, amount):
        if amount < 0:
            raise ValueError('amount should be positive')
        if type(amount) is not int:
            raise TypeError('amount should be int')

        self.amount = amount
        self.bills = [self]

    def __str__(self):
        return f'A {self.amount}$ Bill'

    def __repr__(self):
        return f'A {self.amount}$ Bill'

    def __int__(self):
        return self.amount

    def __eq__(self, other):
        return self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __hash__(self):
        return self.amount


class BillBatch:
    def __init__(self, bills):
        self.bills = bills

    def total(self):
        return reduce(operator.add, (int(b) for b in self.bills))

    def __len__(self):
        return len(self.bills)
    
    def __getitem__(self, index):
        return self.bills[index]


class CashDesk:
    def __init__(self):
        self.drawer = {}

    def take_money(self, thing):
        if type(thing) is not Bill and type(thing) is not BillBatch:
            raise TypeError('Type of thing should be Bill or BillBatch')

        for b in thing.bills:
            if b not in self.drawer:
                self.drawer[b] = 0
            self.drawer[b] += 1

    def total(self):
        return reduce(lambda a, x: a + int(x[0]) * x[1], self.drawer.items(), 0)

    def inspect(self):
        print(f'We have a total of {self.total()}$ in the desk')
        print(f'We have the following count of bills, sorted in ascending order')

        _sorted = sorted(self.drawer, key=lambda x: x.amount)
        print(os.linesep.join(f'{b.amount}$ bills - {self.drawer[b]}' for b in _sorted))
