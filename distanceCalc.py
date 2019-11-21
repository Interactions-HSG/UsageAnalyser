import numpy as np
import math
import random as rnd
import cv2
import matplotlib.pyplot as plt
#%matplotlib inline


# calculate distance between roi (extracted centroid coordinate) and objects
# plots the output as a scatter map and overlays it on the given image
def calculateAndMap(raw_image,coordinates):

    image=cv2.imread(raw_image)
    image=cv2.resize(image,(640,480))
    image=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    #table_co_x=200
    #table_co_y=250

    usage=[]
    coordinates_x=[]
    coordinates_y=[]
    for i in coordinates:
        for j in i:
            x=j[0]
            y=j[1]
            coordinates_x.append(x)
            coordinates_y.append(y)
            #print (x,y)
            #d=math.sqrt(((table_co_x-x)**2)+((table_co_y-y)**2))
            #print(d)
            #if d<150:
                #print ("table is being used")
                #usage.append(d)
            #else:
                #print ("table empty")
        #print distance from the furniture        
        #print(usage)

    #plot scatter plot of the persaon's positions in that pertiular time frame on the current/empty room image 
    implot=plt.imshow(image)
    plt.plot(coordinates_x,coordinates_y,'ro', markerfacecolor='w')
    #plt.hist2d(coordinates_x,coordinates_y)
    plt.show()


  