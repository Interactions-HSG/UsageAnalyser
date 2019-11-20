from LOWatch import startWatching
from time import sleep
import time

def scheduler():
    while True:
        coordinate=startWatching(time.time())
        return coordinate
        sleep(60*1)