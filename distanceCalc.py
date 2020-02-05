import numpy as np
import math
import random as rnd
import cv2
import matplotlib.pyplot as plt
import time
import config
import csv

usage = []

counter = 0
num = 0

countTable = {
}
def getSerial():
  deviceID = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        deviceID = line[10:26]
    f.close()
  except:
    deviceID = "ERROR000000000"
 
  return deviceID

def distanceCalculator(x1, y1, occupancy):
    countTable.clear()
    for i in config.furnitureCoordinates:
        countTable.update({i: 0})
  
    try:
        f = open('{}outputTable{}.csv'.format(config.outputPath,time.strftime('%b-%d-%Y_%H%M%S', time.localtime())), "w")
        writer = csv.DictWriter(f, fieldnames=["Furniture_Type", "Usage_Count", "Occupancy","Device ID"])
        writer.writeheader()
        
    except Exception as e:
        print(e)
        
    
    value = 0
    for i in config.furnitureCoordinates:
        x2 = config.furnitureCoordinates[i].get("x")
        y2 = config.furnitureCoordinates[i].get("y")
        w = config.furnitureCoordinates[i].get("w")
        h = config.furnitureCoordinates[i].get("h")
        xC = x2+w/2
        yC = y2+h/2
        # print(x1,y1)
        for j in range(len(x1)):
            distance = math.sqrt(((x1[j]-xC)**2)+((y1[j]-yC)**2))
            if (int(distance) < (config.defaultDistance+(w/2)) or int(distance) < (config.defaultDistance+(h/2))):
                value = countTable[i]+1
                countTable.update({i: value})
            else:
                continue
        writer.writerow({"Furniture_Type": i, "Usage_Count": countTable[i],
                         "Occupancy": config.occupancy.get(occupancy),"Device ID":getSerial()})
    
    f.close()

def iterateNplot(Coordinates, color):
    coordinates_x = []
    coordinates_y = []
    if(len(Coordinates) > 0):
        for i in Coordinates:
            if (len(i) > 0):
                x1 = float(i[0])
                y1 = float(i[1])
                coordinates_x.append(x1)
                coordinates_y.append(y1)
            else:
                continue
    plt.plot(coordinates_x, coordinates_y, 'ro', markerfacecolor=color)
    return (coordinates_x, coordinates_y)

''' calculate distance between roi (extracted centroid coordinate) and objects
 plots the output as a scatter map and overlays it on the given image '''


def calculateAndMap(raw_image, changeCoordinates, personCoordinates, occupancy):

    # image=cv2.imread(raw_image)
    if hasattr(raw_image,'shape'):
        config.inputImageSize=raw_image.shape[:-1][::-1]
        image = cv2.resize(raw_image, config.inputImageSize)
    else:
        raw_image=cv2.imread(raw_image)
        config.inputImageSize=raw_image.shape[:-1][::-1]
        image = cv2.resize(raw_image, config.inputImageSize)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # table_co_x=200
    # table_co_y=250
    count = 0
    cv2.putText(image, "furnitures used:", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, (1), (255, 255, 255))
    cv2.line(image, (50, 52), (400, 52), (255, 255, 255), 2)

    ''' Furniture usage counter '''
    
    #(coordinates_x,coordinates_y) = iterateNplot(personCoordinates,config.red) 
    #distanceCalculator(coordinates_x,coordinates_y)
    #iterateNplot(changeCoordinates,config.blue)
    
    (coordinates_x, coordinates_y) = iterateNplot(changeCoordinates, config.red)
    distanceCalculator(coordinates_x, coordinates_y, occupancy)
    iterateNplot(personCoordinates, config.blue)

    ''' plot scatter plot of the persaon's positions in that pertiular time frame on the current/empty room image '''
    ''' create furniture regions on raw_pic '''
    for i in config.furnitureCoordinates:
        cv2.putText(image,"{}: {}".format(i,countTable[i]), (50, 80+count), cv2.FONT_HERSHEY_SIMPLEX, (1), (255, 255, 255))
        count += 20
        
    
    implot = plt.imshow(image)
    # plt.hist2d(coordinates_x,coordinates_y)
    plt.savefig('{}outputGraph{}.png'.format(config.outputPath,time.strftime('%b-%d-%Y_%H%M%S', time.localtime())), bbox_inches='tight')
    #plt.show()
    plt.close('all')
   
    



