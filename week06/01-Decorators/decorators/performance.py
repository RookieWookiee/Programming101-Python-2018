from functools import wraps
import time

def performance(fname):
    def accepter(func):
        @wraps(func)
        def decorator(*args):
            start = time.time()
            res = func(*args)
            end = time.time()

            with open(fname, 'a') as f:
                f.write(f'{func.__name__} was called and took {end - start:.2f} seconds to complete\n')

            return res
        return decorator
    return accepter
