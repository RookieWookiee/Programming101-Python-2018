import signal
from contextlib import wraps

def interruptable(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except KeyboardInterrupt:
            print()
            return
        return res
    return decorated
