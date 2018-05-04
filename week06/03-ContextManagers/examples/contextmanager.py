from contextlib import contextmanager


class ContextManager:
    def __init__(self, generator):
        self.generator = generator

    def __enter__(self):
        try:
            return next(self.generator)
        except TypeError:
            raise RuntimeError('Func is not generator.')

    def __exit__(self, *args):
        try:
            next(self.generator)
        except StopIteration:
            return True
        else:
            raise RuntimeError('Generator was not exhausted.')


def decorator(func):
    def inner_func(*args, **kwargs):
        return ContextManager(func(*args, **kwargs))

    return inner_func


#@contextmanager
@decorator
def random_manager(numb):

    yield 'yielded value'


with random_manager(42) as value:
    print('Value: ', value)
    print('Inside context manager')
