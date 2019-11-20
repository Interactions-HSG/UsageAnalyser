from Scheduler import scheduler
from distanceCalc import calculateAndMap
from time import sleep
import time
import matplotlib.pyplot as plt
#%matplotlib inline
raw_pic='/Users/sanjivjha/Desktop/peoplegroups.jpg'
coordinates=[]
def generateMap():
    while True:
        coordinate=scheduler()
        coordinates.append(coordinate)
        print(coordinates)
        calculateAndMap(raw_pic,coordinates)
        sleep(60*1)        
generateMap()