import numpy as np
import math
import random as rnd
import cv2
import matplotlib.pyplot as plt
import time
import config
import csv
#%matplotlib inline

usage=[]

counter=0
num=0

countTable={
}
    
def distanceCalculator(x1,y1):
    f = open('output/output'+str(time.time())+'.csv', "w")
    writer = csv.DictWriter(f, fieldnames=["Furniture_Type","Usage_Count"])
    writer.writeheader()
    value=0
    for i in config.furnitureCoordinates:
        (x2,y2)=config.furnitureCoordinates[i]
            #print(x1,y1)
        for j in range(len(x1)):
            distance=math.sqrt( ((x1[j]-x2)**2)+((y1[j]-y2)**2) )
            if (int(distance)<50):
                value=countTable[i]+1
                countTable.update({i:value})
            else:
                continue
        writer.writerow({"Furniture_Type":i,"Usage_Count":value})
    
    f.close()


def iterateNplot(Coordinates,color):
    coordinates_x=[]
    coordinates_y=[]
    if(len(Coordinates)>0):
        for i in Coordinates:
            if (len(i)>0):
                x1=float(i[0])
                y1=float(i[1])
                coordinates_x.append(x1)
                coordinates_y.append(y1)             
            else:
                continue
    plt.plot(coordinates_x,coordinates_y,'ro', markerfacecolor=color)
    return (coordinates_x,coordinates_y)

# calculate distance between roi (extracted centroid coordinate) and objects
# plots the output as a scatter map and overlays it on the given image
def calculateAndMap(raw_image,changeCoordinates,personCoordinates):

    #image=cv2.imread(raw_image)
    image=cv2.resize(raw_image,config.inputImageSize )
    image=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    #table_co_x=200
    #table_co_y=250
    count=0
    cv2.putText(image,"furnitures used:",(50,50),cv2.FONT_HERSHEY_SIMPLEX,(1),(255, 255, 255))
    cv2.line(image, (50, 52), (400, 52), (255,255,255), 2)
    for i in config.furnitureCoordinates:
        countTable.update({i:0})

    #plot scatter plot of the persaon's positions in that pertiular time frame on the current/empty room image 
    for i in config.furnitureCoordinates:
        cv2.putText(image,str(i)+": "+str(countTable[i]),(50,80+count),cv2.FONT_HERSHEY_SIMPLEX,(1),(255, 255, 255))
        count+=20
    implot=plt.imshow(image)

    #Furniture usage counter
    (coordinates_x,coordinates_y) = iterateNplot(personCoordinates,config.red) 
    distanceCalculator(coordinates_x,coordinates_y)
    iterateNplot(changeCoordinates,config.blue)

    #plt.hist2d(coordinates_x,coordinates_y)
    plt.savefig(config.outputPath+'newGraph'+str(time.time())+'.png',bbox_inches='tight')
    plt.show()
    



  