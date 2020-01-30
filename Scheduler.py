from LOWatch import startWatching
from time import sleep
import time


def scheduler():
    while True:
        '''imported function for person detection and image/video saving
         returns coordinates'''
        (changeCoordinates, personCoordinates,
         occupancy) = startWatching(time.time())
        return (changeCoordinates, personCoordinates, occupancy)
