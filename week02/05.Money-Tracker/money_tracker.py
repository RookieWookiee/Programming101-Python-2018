from functools import reduce
from datetime import datetime


def list_user_data(data=None):
    if data is None:
        data = read_data('money_tracker.txt')

    for d in data[0]:
        print(d.strftime('=== %d-%m-%Y ==='))
        for x in data[1][d]:
            print(x)


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def get_values(data): return [x for key in data[0] for x in data[1][key]]


def show_user_incomes(data=None):
    if data is None:
        data = read_data('money_tracker.txt')

    incomes = [x for x in get_values(data) if x.endswith('New Income')]
    formatted = [tuple(x.split(', ')[:2]) for x in incomes]
    return [(num(q), _type) for q, _type, in formatted]


def show_user_deposits(data=None):
    if data is None:
        data = read_data('money_tracker.txt')

    deposits = [x for x in get_values(data) if 'Deposit' in x.split(', ')]
    formatted = [tuple(x.split(', ')[:2]) for x in deposits]
    return [(num(q), _type) for q, _type in formatted]


def show_user_savings(data=None):
    if data is None:
        data = read_data('money_tracker.txt')

    incomes = [x for x in get_values(data) if 'Savings' in x.split(', ')]
    formatted = [tuple(x.split(', ')[:2]) for x in incomes]
    return [(num(q), _type) for q, _type in formatted]


def show_user_expenses(data=None):
    if data is None:
        data = read_data('money_tracker.txt')

    expenses = [x for x in get_values(data) if x.endswith('New Expense')]
    formatted = [tuple(x.split(', ')[:2]) for x in expenses]
    return [(num(x[0]), x[1]) for x in formatted]


def list_user_expenses_ordered_by_categories(data=None):
    if data is None:
        data = read_data('money_tracker.txt')

    expenses = show_user_expenses(data)
    return sorted(expenses, key=lambda x: (x[1], x[0]))


def show_user_data_per_date(date=None, data=None):
    if data is None:
        data = read_data('money_tracker.txt')

    date = get_input(date, lambda: datetime.strptime(input('>>> '), '%d-%m-%Y'),
                     msg='New income date:',
                     failmsg='Invalid date: the date should be in dd-mm-YYYY format')

    query = data[1][date]
    formatted = [tuple(y.strip() for y in x.split(',')) for x in query]

    return [(num(q), c, t) for q, c, t in formatted]


def list_income_categories(data=None):
    if data is None:
        data = read_data('money_tracker.txt')
    t = set(x.split(', ')[1] for x in get_values(data) if x.endswith('Income'))
    return list(t)


def list_expense_categories(data=None):
    if data is None:
        data = read_data('money_tracker.txt')
    t = set(x.split(', ')[1] for x in get_values(data) if x.endswith('Expense'))

    return list(t)


def get_input(data, key, msg=None, failmsg=None):
    if msg is not None:
        print(msg)

    while data is None:
        try:
            data = key()
        except ValueError:
            if msg is not None:
                print(failmsg)
            data = None

    return data


def add_income(income_category=None, money=None, date=None, write_to_disk=True, data=None):
    get_input(money, lambda: num(input('>>> '), msg='New income amount:',
              failmsg='Invalid input, try again'))

    if income_category is None:
        print('New income type:')
        income_category = input('>>> ')

    get_input(date, lambda: datetime.strptime(input('>>> '), '%d-%m-%Y',
              msg='New income date:',
              failmsg='Invalid date: the date should be in dd-mm-YYYY format'))

    if data is None:
        data = read_data()

    if date not in data[1]:
        data[0].append(date)
        data[1][date] = []

    date[1].append('{0}, {1}, New Income', money, income_category)

    if write_to_disk:
        write_data(data)


def add_expense(expense_category=None, money=None, date=None, write_to_disk=True, data=None):
    get_input(money, lambda: num(input('>>> '), msg='New expense amount:',
              failmsg='Invalid input, try again'))

    if expense_category is None:
        print('New expense type:')
        expense_category = input('>>> ')

    get_input(date, lambda: datetime.strptime(input('>>> '), '%d-%m-%Y',
              msg='New expense date:',
              failmsg='Invalid date: the date should be in dd-mm-YYYY format'))

    if data is None:
        data = read_data()

    if date not in data[1]:
        data[0].append(date)
        data[1][date] = []

    date[1].append('{0}, {1}, New Expense', money, expense_category)

    if write_to_disk:
        write_data(data)


def exit(data=None):
    if data is not None:
        write_data(data)


def read_data(f='money_tracker.txt'):
    def group_by_date(a, x):
        if x.startswith('===') and x.endswith('==='):
            date = datetime.strptime(x, '=== %d-%m-%Y ===')
            a.append((date, []))
        else:
            a[-1][1].append(x)
        return a

    with open(f, 'r') as _f:
        lines = _f.readlines()

    by_date_l = reduce(group_by_date, [x.strip() for x in lines], [])
    dates = [x[0] for x in by_date_l]
    return (dates, {x[0]: x[1] for x in by_date_l})


def write_data(data=None, f='money_tracker.txt'):
    if data is None:
        return

    acc = []
    for key in data[0]:
        acc.append(key.strftime('=== %d-%m-%Y ==='))
        for x in data[1][key]:
            acc.append(x)

    with open(f, 'w') as _f:
        _f.writelines(acc)


def get_date(_type=None):
    def _get_date():
        date = None
        while date is None:
            try:
                date = datetime.strptime(input('>>> '), '%d-%m-%Y')
            except ValueError:
                print('Invalid date: the date should be in d-mm-YYYY format')
                date = None
        return tuple([date])

    def get_income_date():
        print('New income date:')
        return _get_date()

    def get_expense_date():
        print('New expense date:')
        return _get_date()

    def get_no_particular_date():
        print('Date:')
        return _get_date()

    if _type == 'income':
        return get_income_date
    elif _type == 'expense':
        return get_expense_date
    else:
        return get_no_particular_date


def get_category(_type):
    def _get_category():
        return tuple([input('>>> ')])

    def get_income_category():
        print('New income type:')
        return _get_category()

    def get_expense_category():
        print('New expense type:')
        return _get_category()

    if _type == 'income':
        return get_income_category
    elif _type == 'expense':
        return get_expense_category


def get_money(_type):
    def _get_money():
        money = None
        while money is None:
            try:
                money = num(input('>>> '))
                if money < 0:
                    print('Amount should be positive')
                    money = None
            except ValueError:
                print('Incorrect number format')
                money = None
        return tuple([money])

    def get_income_money():
        print('New income amount:')
        return _get_money()

    def get_expense_money():
        print('New expense amount:')
        return _get_money()

    if _type == 'income':
        return get_income_money
    elif _type == 'expense':
        return get_expense_money


dispatch_table = \
    {
        1: list_user_data,
        2: show_user_data_per_date,
        3: list_user_expenses_ordered_by_categories,
        4: add_income,
        5: add_expense,
        6: exit
    }

dispatch_take_input_table = \
    {
        1: lambda: None,
        2: get_date('income'),
        3: get_date(),

        4: lambda: get_money('income')() +
                   get_category('income')() +
                   get_date('income')(),

        5: lambda: get_money('expense')() +
                   get_category('expense')() +
                   get_date('expense')(),

        6: lambda: None
    }


menu = [
    'Choose one of the following options to continue:',
    '1 - show all data',
    '2 - show data for specific date',
    '3 - show expenses, ordered by categories',
    '4 - add new income',
    '5 - add new expense',
    '6 - exit'
]


def print_menu(): [print(x) for x in menu]


def main():
    _input = 0
    EXIT = 6
    data = read_data('money_tracker.txt')

    while _input is not EXIT:
        print_menu()
        _input = int(input('>>> '))
        actual_args = dispatch_take_input_table[_input]()
        output = dispatch_table[_input](data=data, *actual_args)
        [print(x) for x in output]
        print()

    exit()


if __name__ == '__main__':
    main()
