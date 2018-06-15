from functools import wraps


def accepts(*args):
    def accepter(func):
        if len(args) != func.__code__.co_argcount:
            raise ValueError('len of decorator args must be the same as the decorated function')
        @wraps(func)
        def decorated(*fargs):
            if any(type(x) != y for x, y in zip(fargs, args)):
                raise TypeError('type mismatch')
            return func(*fargs)
        return decorated
    return accepter


@accepts(str, int, int)
def func1(a, b, c):
    print(a, b, c)
