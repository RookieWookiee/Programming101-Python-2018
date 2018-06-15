from datetime import datetime
from encrypt import encrypt
from functools import wraps

def log(fname):
    def accepter(func):
        @wraps(func)
        def decorator(*args):
            with open(fname, 'a') as f:
                f.write(f'{func.__name__} was called at {str(datetime.now())}\n')
            return func(*args)
        return decorator
    return accepter


@log('log.txt')
@encrypt(2)
def get_low():
    return "Get get get low"
