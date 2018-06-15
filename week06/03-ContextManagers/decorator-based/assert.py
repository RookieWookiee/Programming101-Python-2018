from contextlib import contextmanager


@contextmanager
def assertRaises(extype, msg=None):
    if not issubclass(extype, BaseException):
        raise ValueError('extype must be derived from BaseException')

    try:
        yield
        raise ValueError(f'{extype.__name__} was not raised')
    except Exception as e:
        if type(e) != extype:
            print(f'Wrong exception raised: expected "{extype.__name__}" got "{e.__class__.__name__}"')
            raise e
        if msg != None and msg != str(e):
            print(f'Messages differ: expected "{msg}", got "{str(e)}"')
            raise e


if __name__ == '__main__':
    def raise_value_error(msg=None):
        raise ValueError(msg)
    def raise_type_error(msg=None):
        raise TypeError(msg)

    with assertRaises(ValueError, msg='test'):
        raise_value_error('test')
