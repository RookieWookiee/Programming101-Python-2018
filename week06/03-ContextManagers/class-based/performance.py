import time
from datetime import datetime


class performance:
    def __init__(self, fname):
        self.filename = fname

    def __enter__(self):
        self.start = time.time()

    def __exit__(self, type, val, traceback):
        self.end = time.time()
        with open(self.filename, 'a') as f:
            f.write(f'{datetime.now()}. Execution time: {self.end - self.start}\n')


if __name__ == '__main__':
    with performance('log_perf.txt'):
        time.sleep(1)
