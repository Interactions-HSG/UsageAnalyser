import time
import math
import cv2
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import config
from furniture import furniture

COUNTER = 0
NUM = 0

COUNT_TABLE = {
}

MOVING_COORDINATES = []
STILL_COORDINATES = []

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


def check_continuity(check_array):
    """check continuity in the detected changes"""

    MOVING_COORDINATES.clear()
    STILL_COORDINATES.clear()
    for i in range(0, len(check_array)-1):
        (xC, yC) = check_array[i]
        (x1, y1) = check_array[i+1]
        score = math.sqrt(math.pow(x1-xC, 2)+math.pow(y1-yC, 2))
        if 5 < score < 150:
            MOVING_COORDINATES.append((x1, y1))
        elif score < 5:
            STILL_COORDINATES.append((x1, y1))

    if(len(MOVING_COORDINATES) > 10):
        return True
    return False


def distance_calculator(x1, y1, usage_type, writer):
    """calculate the distance between the change and the furniture"""
    occupancy = 0
    filtered_array = []

    if len(x1) > 0:
        occupancy = 1

    COUNT_TABLE.clear()
    try:
        for i in config.FURNITURE_NAMES:
            COUNT_TABLE.update({i: 0})

        value = 0
        
        furniture_obj = furniture(config.FURNITURE_NAMES, config.FURNITURE_COORDINATES)
        furniture_coordinates = furniture_obj.getCoordinateDict()
        
        for i in furniture_coordinates:
            x2 = furniture_coordinates[i].get("x")
            y2 = furniture_coordinates[i].get("y")
            w = furniture_coordinates[i].get("w")
            h = furniture_coordinates[i].get("h")
            xC = x2+w/2
            yC = y2+h/2
    except Exception as e:
        print(e)
        return False
        # print(x1,y1)
        for j in range(len(x1)):

            distance = math.sqrt(math.pow((x1[j]-xC), 2)+math.pow((y1[j]-yC), 2))

            if usage_type == 2:
                config.DEFAULT_DISTANCE = 0

            if (int(distance) < (config.DEFAULT_DISTANCE+(w/2)) or int(distance) < (config.DEFAULT_DISTANCE+(h/2))):
                value = COUNT_TABLE[i]+1
                COUNT_TABLE.update({i: value})
                filtered_array.append((x1[j], y1[j]))
            else:
                continue

        writer.writerow(
            {"Timestamp": time.strftime('%b-%d-%Y_%H%M%S', time.localtime()), "Furniture_Type": i, "Usage_Count": COUNT_TABLE[i], "Usage_Type": config.USAGE.get(usage_type), "Room_Occupancy": config.OCCUPANCY.get(occupancy), "Device_ID": get_serial()})
    
    filtered_array = np.array(filtered_array)
    return filtered_array


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
    #plt.plot(coordinates_x, coordinates_y, 'ro', markerfacecolor=color)
    for i in range(0, len(coordinates)-1):
        (xC, yC) = coordinates[i]
        (x1, y1) = coordinates[i+1]
        newline((xC, yC), (x1, y1), color)


''' calculate distance between roi (extracted centroid coordinate) and objects
 plots the output as a scatter map and overlays it on the given image '''


def calculate_and_map(raw_image, change, writer):
    """map on the first image"""
    # image=cv2.imread(raw_image)
    if hasattr(raw_image, 'shape'):
        config.INPUT_IMAGE_SIZE = raw_image.shape[:-1][::-1]
        image = cv2.resize(raw_image, config.INPUT_IMAGE_SIZE)
    else:
        raw_image = cv2.imread(raw_image)
        config.INPUT_IMAGE_SIZE = raw_image.shape[:-1][::-1]
        image = cv2.resize(raw_image, config.INPUT_IMAGE_SIZE)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # table_co_x=200
    # table_co_y=250
    count = 0
    cv2.putText(image, "furnitures used:", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, (1), (255, 255, 255))
    cv2.line(image, (50, 52), (400, 52), (255, 255, 255), 2)

    ''' Furniture usage COUNTER '''

    continuity = check_continuity(change)
    if(continuity is True):
        (coordinates_x, coordinates_y) = iterate(
            MOVING_COORDINATES)
        filtered_array = distance_calculator(coordinates_x, coordinates_y, 1, writer)
        start_plot(filtered_array, config.RED)
    (coordinates_x, coordinates_y) = iterate(
        STILL_COORDINATES)
    filtered_array = distance_calculator(coordinates_x, coordinates_y, 2, writer)
    start_plot(filtered_array, config.BLUE)

    ''' plot scatter plot of the persaon's positions in that pertiular time frame on the current/empty room image '''
    ''' create furniture regions on raw_pic '''
    '''
    for i in config.FURNITURE_COORDINATES:
        cv2.putText(image, "{}: {}".format(i, COUNT_TABLE[i]), (50, 80+count), cv2.FONT_HERSHEY_SIMPLEX, (1), (255, 255, 255))
        count += 20
    '''
    implot = plt.imshow(image)
    # plt.hist2d(coordinates_x,coordinates_y)
    plt.savefig('{}outputGraph{}.png'.format(config.OUTPUT_PATH, time.strftime(
        '%b-%d-%Y_%H%M%S', time.localtime())), bbox_inches='tight')
    # plt.show()
    plt.close('all')
