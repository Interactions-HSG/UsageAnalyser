# import the necessary packages
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import time
import math


class CentroidTracker():
    """ calculate the number of warm/cold objects using the furniture and return the number"""
    def __init__(self):
        # initialize the next unique object ID along with two ordered
        # dictionaries used to keep track of mapping a given object
        # ID to its centroid and number of consecutive frames it has
        # been marked as "disappeared", respectively
        self.nextObjectID = 0
        self.objects = OrderedDict()
        
    def delete(self):
        objectIDs = list(self.objects.keys())
        for i in range(len(objectIDs)):
            objectID = objectIDs[i]
            del self.objects[objectID]
        return

    def register(self, centroid):
        # when registering an object we use the next available object
        # ID to store the centroid
    
        self.objects[self.nextObjectID] = centroid   
        self.nextObjectID += 1
        

    def update(self, rects):
        # check to see if the list of input bounding box rectangles
        # is empty
        objectID_ = ""
        distance_ = ""
        if len(rects) == 0:
            return (self.objects) 

        print(rects[0])
        cX = int(rects[0])
        cY = int(rects[1])
        
        inputCentroids = (cX, cY)
    
        
        # if we are currently not tracking any objects take the input
        # centroids and register each of them
        if len(self.objects) == 0:
                self.register(inputCentroids)

        # otherwise, are are currently tracking objects so we need to
        # try to match the input centroids to existing object
        # centroids
        else:
            # grab the set of object IDs and corresponding centroids
            objectIDs = list(self.objects.keys())
            #print("objectID", objectIDs)

            objectCentroids = list(self.objects.values())
            
            #print("object centroids", objectCentroids)
            #print("object centroids 2", objectCentroids)
            
            
            """ Compare the centroids coordinates to the exisiting registered centroids"""
            """ Find the existing centroid that is closest to the incoming centroid"""
            for i in range(len(objectIDs)):
                    #print("im loop")
                    objectID = objectIDs[i]
                    centroid = self.objects[objectID]
                    #print("objectCENTER", centroid)

                    #centroid = centroid[i]
                    #print("nach i CENTROID", centroid)
                    xC = centroid[0]
                    yC = centroid[1]
                    #print("xC", xC)
                    
                    distance = math.sqrt(math.pow((cX-xC), 2)+math.pow((cY-yC), 2))
                    #print("distance", distance)
                    
                    if i == 0:
                        distance_ = distance
                        objectID_ = objectID_
                    else:
                        if distance_ <= distance:
                            continue
                        if distance_ > distance:
                            distance_ = distance
                            objectID_ = objectID
            
            """ For the """
            if distance_ > 20:
                    self.register(inputCentroids)
            elif distance_ < 20:
                    self.objects[objectID_] = inputCentroids

                    
                
        return (self.objects)
        #return self.objects