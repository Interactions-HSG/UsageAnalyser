from LOWatch import startWatching
from time import sleep
import time

def scheduler():
    while True:
        # imported function for person detection and image/video saving
        # return coordinates
        coordinate=startWatching(time.time())
        return coordinate