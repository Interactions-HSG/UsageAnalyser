"""create furniture dictionary"""

class furniture(object):
    """furniture class"""
    def __init__(self, name_list, coordniate_list):
        self.names = name_list
        self.coordniates = coordniate_list
    
    
    def createCoordinates(self):
        """iterate through the coordinates list and create a dictionary"""
        coordinate_dict =[] 
        
        for i in range(len(self.coordniates)):
            coordinate_dict.append({"x": self.coordniates[i][0],
                                    "y": self.coordniates[i][1],
                                    "w": self.coordniates[i][2],
                                    "h": self.coordniates[i][3],
                                   })
        return coordinate_dict
    
    
    def getCoordinateDict(self):
        """return a name based dictionary"""
        co_dict= self.createCoordinates()
        return dict(zip(self.names,co_dict))
    
    
   