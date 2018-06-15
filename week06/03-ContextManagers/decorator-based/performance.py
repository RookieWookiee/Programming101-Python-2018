from contextlib import contextmanager
from time import time, sleep
from datetime import datetime


@contextmanager
def performance(fname):
    start = time()
    yield
    end = time()
    date = datetime.now()
    with open(fname, 'a') as f:
        f.write(f'Date {date}. Execution time: {end - start}\n')

if __name__ == '__main__':
    def one_sec():
        sleep(1)

    with performance('log_perf.txt'):
        one_sec()
