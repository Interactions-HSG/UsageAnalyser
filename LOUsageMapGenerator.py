from Scheduler import scheduler
from distanceCalc import calculateAndMap
from time import sleep
import time
import matplotlib.pyplot as plt
#%matplotlib inline
raw_pic='/Users/sanjivjha/Desktop/peoplegroups.jpg'
coordinates=[]

# generates scatter map and overlays on the empty room image for better analysis by the users
# outputs found ROI coordinates and schedules the camera for reducing the battery life conservation
def generateMap():
    while True:
        coordinate=scheduler()
        coordinates.append(coordinate)
        print(coordinates)
        # imported function for calcuating the distance of a person from the objects
        calculateAndMap(raw_pic,coordinates)
        # device goes to sleep for an hour 60*60
        sleep(60*1)        
generateMap()