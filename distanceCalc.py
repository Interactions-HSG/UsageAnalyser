'''Post processing calculations'''
import time
import math
import cv2
import numpy as np
import config
from furniture import furniture
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from PIL import Image
import io

COUNTER = 0
NUM = 0

COUNT_TABLE = {
}

def get_serial():
    """get serial number of the device"""

    device_ID = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                device_ID = line[10:26]
        f.close()
    except OSError:
        device_ID = "ERROR000000000"

    return device_ID


def check_continuity(check_array, MOVING, STILL):
    """check continuity in the detected changes"""
    MOVING.clear()
    STILL.clear()
    
    temp=[]
    
    
    
    for i in range(len(check_array)-1):
        count = np.count_nonzero(check_array == check_array[i]) #gives you the count of all the unique values. check each pixel if there is a change
        if count > config.COLD_COUNT:
            STILL.append(check_array[i])
        
        (xC, yC) = check_array[i]
        (x1, y1) = check_array[i+1]
        score = math.sqrt(math.pow(x1-xC, 2)+math.pow(y1-yC, 2))
        
        if 5 < score < 150:
            MOVING.append([x1,y1])
    
        elif score <=1:
            temp.append([x1,y1])
    
    temp = np.array(temp)
    
    for i in range(len(temp)-1):
        count = np.count_nonzero(temp == temp[i])
        if count > config.COLD_COUNT:
            STILL.append(temp[i])
        
    
    '''   
    if len(temp)>0:
        for i in range(len(temp)-1):
            temp = np.array(temp)
            count = np.count_nonzero(temp == temp[i])
            if count > config.COLD_COUNT:
                STILL.append(temp[i])
    
    '''
    #STILL_ = [[400, 250]]            
    MOVING = np.array(MOVING)
    STILL = np.array(STILL)
  
    return (MOVING , STILL)


def distance_calculator(x1, y1, usage_type, writer, count):
    """calculate the distance between the change and the furniture"""
    occupancy = 0
    filtered_array = []
    layout_map = Image.open(r"images/61-402layout.png")
    layout_map = np.asarray(layout_map)
    used_furn_layout = []

    if len(x1) > 0:
        occupancy = 1

    COUNT_TABLE.clear()
    try:
        for i in config.FURNITURE_NAMES:
            COUNT_TABLE.update({i: 0})

        value = 0
        
        furniture_obj = furniture(config.FURNITURE_NAMES, config.FURNITURE_COORDINATES)
        furniture_coordinates = furniture_obj.getCoordinateDict()
        furniture_obj_layout = furniture(config.FURNITURE_NAMES,config.FURNITURE_LAYOUT_COORDINATES)
        furniture_layout_coordinates = furniture_obj_layout.getCoordinateDict()
        
        for i in furniture_coordinates:
            x2 = furniture_coordinates[i].get("x")
            y2 = furniture_coordinates[i].get("y")
            w = furniture_coordinates[i].get("w")
            h = furniture_coordinates[i].get("h")
            xC = x2+w/2
            yC = y2+h/2
    
            for j in range(len(x1)):

                distance = math.sqrt(math.pow((x1[j]-xC), 2)+math.pow((y1[j]-yC), 2))

                if usage_type == 2:
                    config.DEFAULT_DISTANCE = 0

                if (int(distance) < (config.DEFAULT_DISTANCE+(w/2)) or int(distance) < (config.DEFAULT_DISTANCE+(h/2))):
                    value = COUNT_TABLE[i]+1
                    COUNT_TABLE.update({i: value})
                    filtered_array.append((x1[j], y1[j]))
                   
                    for k in furniture_layout_coordinates:
                        if k == i:
                            x2_ = furniture_layout_coordinates[k].get("x")
                            y2_ = furniture_layout_coordinates[k].get("y")
                            w_ = furniture_layout_coordinates[k].get("w")
                            h_ = furniture_layout_coordinates[k].get("h")
                            used_furn_layout.append((k, x2_,y2_,w_,h_,value))
                            break
                
                        else:
                            continue    
                else:
                    continue

            writer.writerow(
                {"Timestamp": time.strftime('%b-%d-%Y_%H%M%S', time.localtime()), "Furniture_Type": i, "Usage_Count": COUNT_TABLE[i],"Total_Checks":count,"Usage_Percentage": round((COUNT_TABLE[i] / count)*100,2), "Usage_Type": config.USAGE.get(usage_type), "Room_Occupancy": config.OCCUPANCY.get(occupancy), "Device_ID": get_serial()})
        
    except Exception as e:
        print(e)
        return False
        # print(x1,y1)
        
    filtered_array = np.array(filtered_array)
    used_furn_layout = np.array(used_furn_layout)
    return filtered_array, used_furn_layout


def newline(p1, p2, color):
    """draw a line between two points"""
    ax = plt.gca()
    l = mlines.Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=color)
    ax.add_line(l)


def iterate(coordinates):
    """iterate over the recived coordinates"""

    coordinates_x = []
    coordinates_y = []
    if(len(coordinates) > 0):
        for i in coordinates:
            if (len(i) > 0):
                x = float(i[0])
                y = float(i[1])
                coordinates_x.append(x)
                coordinates_y.append(y)
            else:
                continue
        coordinates_x = np.array(coordinates_x)
        coordinates_y = np.array(coordinates_y) 
    return (coordinates_x, coordinates_y)


def start_plot(coordinates, color):
    """plot the line on graph"""
    (coordinates_x, coordinates_y) = iterate(coordinates)
    if color == config.BLUE:
        plt.plot(coordinates_x, coordinates_y, 'ro', markersize=6, color=color)
        
    elif color == config.RED:
        for i in range(0, len(coordinates)-1):
            (xC, yC) = coordinates[i]
            (x1, y1) = coordinates[i+1]
            distance = math.sqrt(math.pow((x1-xC), 2)+math.pow((y1-yC), 2))
            if distance<50:
                newline((xC, yC), (x1, y1), color)
        plt.plot(coordinates_x, coordinates_y, 'ro', markersize=2, color=color)
    else:
        return False

def Layiterate(coordinates):
    """iterate over the recived coordinates"""
    furniture_name = []
    coordinates_x = []
    coordinates_y = []
    coordinates_w = []
    coordinates_h = []
    value = []

    if(len(coordinates) > 0):
        for i in coordinates:
            if (len(i) == 6):
                k = i[0]
                x = int(i[1])
                y = int(i[2])
                w = int(i[3])
                h = int(i[4])
                value_ = int(i[5])

                furniture_name.append(k)
                coordinates_x.append(x)
                coordinates_y.append(y)
                coordinates_w.append(w)
                coordinates_h.append(h)
                value.append(value_)
            else:
                raise Exception("coordinates in coordinates list has less than 6 positions")
        coordinates_x = np.array(coordinates_x)
        coordinates_y = np.array(coordinates_y) 
        coordinates_w = np.array(coordinates_w) 
        coordinates_h = np.array(coordinates_h) 
        value = np.array(value) 
    else:
        raise Exception('No furniture has been used')


    return (furniture_name,coordinates_x, coordinates_y, coordinates_w, coordinates_h, value)


def start_plot_layout(coordinates, color, layout_map):
    (furniture_name, coordinates_x, coordinates_y, coordinates_w, coordinates_h, value) = Layiterate(coordinates)
  #  layout_map = Image.open(r"images/61-402layout.png")
    layout_map = np.asarray(layout_map)
    plt.imshow(layout_map)
    ax = plt.gca()
    PatchesWarm = []
    PatchesCold = []
    #WarmPatchesHigh = []



    for i in range(0, len(coordinates)):
        x = coordinates_x[i]
        y = coordinates_y[i]
        w = coordinates_w[i]
        h = coordinates_h[i]
        k = furniture_name[i]
        value_ = value[i]
        xC = x+w/2
        yC = y+h/2
        ax.text(xC,yC,k, fontsize=7, rotation=0, multialignment="center")
        alpha = (0.3+ (value_ // 50000))

        if color == config.RED:
            rect = Rectangle((x, y),w,h,fill=True, alpha=alpha, color=(.9, .3, .3))
            PatchesWarm.append(rect)
            #newline((xC, yC), (x, y), color)




        elif color == config.BLUE:
            rect = Rectangle((xC, yC),(w/3),(h/3),fill=True, alpha=alpha, color=(.4, .8, .9))
            PatchesCold.append(rect)
            #ax.plot(xC, yC, 'bo', markersize=6, color=color)
            #newline((xC, yC), (x, y-20), color)


      
        else: 
            raise Exception('Wrong color')


    ax.add_collection(PatchCollection(PatchesWarm,match_original=True))
    ax.add_collection(PatchCollection(PatchesCold,match_original=True))

    
    #plt.show
    #plt.savefig('{}outputLayout{}.png'.format(config.OUTPUT_PATH, time.strftime(
    #   '%b-%d-%Y_%H%M%S', time.localtime())), bbox_inches='tight') 

''' calculate distance between roi (extracted centroid coordinate) and objects
 plots the output as a scatter map and overlays it on the given image '''



def calculate_and_map(raw_image, change, writer, count):
    """map on the first image"""
    #raw_image = Image.open(r"images/61-402layout.png")
    raw_image = Image.open(r"images/inputNew.png")
    raw_image = np.asarray(raw_image)
    MOVING_COORDINATES = []
    STILL_COORDINATES = []
    if hasattr(raw_image, 'shape'):
        config.INPUT_IMAGE_SIZE = raw_image.shape[:-1][::-1]
        image = cv2.resize(raw_image, config.INPUT_IMAGE_SIZE)
    else:
        raw_image = cv2.imread(raw_image)
        config.INPUT_IMAGE_SIZE = raw_image.shape[:-1][::-1]
        image = cv2.resize(raw_image, config.INPUT_IMAGE_SIZE)
   

    (MOVING_COORDINATES, STILL_COORDINATES) = check_continuity(change, MOVING_COORDINATES, STILL_COORDINATES)
    if len(MOVING_COORDINATES)>10:
        (coordinates_x, coordinates_y) = iterate(
            MOVING_COORDINATES)
        filtered_array_warm, used_furn_layout_warm = distance_calculator(coordinates_x, coordinates_y, 1, writer, count)
       # start_plot(filtered_array_warm, config.RED)
        start_plot_layout(used_furn_layout_warm,config.RED, raw_image)

       
    if len(STILL_COORDINATES)>0:
        (coordinates_x, coordinates_y) = iterate(
            STILL_COORDINATES)
        filtered_array_cold, used_furn_layout_cold = distance_calculator(coordinates_x, coordinates_y, 2, writer, count)
       # start_plot(filtered_array_cold, config.BLUE)
        #used_furn_layout_cold = [["Chair", "150", "130", "50", "50","1"]]
        start_plot_layout(used_furn_layout_cold,config.BLUE, raw_image)

    implot = plt.imshow(image)

    plt.savefig('{}outputGraph{}.png'.format(config.OUTPUT_PATH, time.strftime(
        '%b-%d-%Y_%H%M%S', time.localtime())), bbox_inches='tight')
    # plt.show()
    plt.close('all')
