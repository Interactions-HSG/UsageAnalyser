from Scheduler import scheduler
from distanceCalc import calculateAndMap
from time import sleep
import time
import matplotlib.pyplot as plt
import config
import numpy as np
import cv2
import os

#%matplotlib inline
#raw_pic=config.rawImagePath
capture=cv2.VideoCapture(0)
check,rawImage=capture.read()


# generates scatter map and overlays on the empty room image for better analysis by the users
# outputs found ROI coordinates and schedules the camera for reducing the battery life conservation
def generateMap():
    while True:
        (changeCoordinates,personCoordinates)=scheduler()
        #print(coordinates)
        # imported function for calcuating the distance of a person from the objects
        calculateAndMap(rawImage,changeCoordinates,personCoordinates)
        # device goes to sleep for an hour 60*60
        sleep(config.sleepDuration)  

#check room brightness
room_default_brightness=50
hsv=cv2.cvtColor(rawImage, cv2.COLOR_BGR2HSV)
avg_color_per_row = np.average(hsv, axis=0)
avg_color = np.average(avg_color_per_row, axis=0)
brightness=avg_color[2]
if brightness>room_default_brightness:
    capture.release()
    generateMap()
else:
    capture.release()
    print('The room is too dark for a photo!')
    

