from time import sleep
from performance import performance
from log import log


@log('log.txt')
@performance('log.txt')
def something_heavy():
    sleep(2)
    return 'I am done'

something_heavy()
