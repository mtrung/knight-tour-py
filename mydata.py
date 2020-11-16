import random
from concurrent.futures import ThreadPoolExecutor
from time import sleep

from msg_announcer import announcer
from algo import Algorithm


executor = ThreadPoolExecutor(1)
algo = Algorithm()


def getContent():
    return f'## Knight\'s Tour Solver\n\n{algo}\n'


def loop():
    print('- Data loop started')
    while algo.move():
        announcer.announceSse(getContent())
        sleep(1)
    # algo.placeAt()
    print('- Data loop ended')


def runDataPollingLoop():
    algo.placeAt()
    executor.submit(loop)
