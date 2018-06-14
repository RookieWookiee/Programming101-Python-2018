from mpd import MPDClient
from functools import wraps
from contextlib import contextmanager
import os


def with_mpd_client(func):
    from pmp import HOST, PORT
    @wraps(func)
    def decorator(*args, **kwargs):
        client = MPDClient()
        client.connect(HOST, PORT)
        ret = func(client=client, *args, **kwargs)
        client.close()
        client.disconnect()

        return ret
    return decorator


@contextmanager
def open_client(host, port):
    client = MPDClient()
    client.connect(host, port)
    yield client
    client.close()
    client.disconnect()


@contextmanager
def popen(*args, **kwargs):
    pipe = os.popen(*args, **kwargs)
    yield pipe
    pipe.close()
