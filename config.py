"""Config.py"""

from pathlib import Path
HOME= str(Path.home())

RAW_IMAGE_PATH = r'images/61-402layout.png'

WINDOW_SIZE = (8, 8)

IMAGE_RESOLUTION = (720, 1080)
FACECLASSIFIER_ADDRESS = HOME + \
    r'/downloads/opencv-3.4/data/haarcascades/haarcascade_frontalface_default.xml'
'''
to run on raspberry pi uncomment the line below 'saved opencv-3.4.0 folder inside the local folder'
'''
#FACECLASSIFIER_ADDRESS= r'opencv-3.4.0/data/haarcascades/haarcascade_frontalface_default.xml'
CAPTURE_DURATION = int(3600*3)
SLEEP_DURATION = 900
COLD_COUNT=2000

FPS=1

OUTPUT_PATH = r'output/'
INPUT_PATH = r'input/'

DEFAULT_DISTANCE = 20
CHANGE_THRESHOLD = 62
CHANGE_THRESHOLD_MAX = 200
CHANGE_DISTANCE_MIN = 50
CHANGE_DISTANCE_MAX = 150


MODEL_FILE = r'tflite_models/detect.tflite'
LABEL_PATH = r'tflite_models/person-labelmap.txt'

INPUT_IMAGE_SIZE = (640, 480)
BLURR_SIZE = (31, 31)

ROOM_BRIGHTNESS_THRESHOLD = 50


"""(x,y,width,height)"""
FURNITURE_COORDINATES = [(30, 150, 50, 70),
                         (30, 215, 40, 70),
                         (80, 130, 130, 100),
                         (70, 230, 120, 110),
                         (400, 240, 130, 90),
                         (400, 30, 90, 180),
                         (70, 50, 70, 20),
                         (40, 350, 70, 20),
                         (400, 350, 110, 120)]

FURNITURE_NAMES = ["Desk1",
                   "Desk2",
                   "Desk3",
                   "Table1",
                   "Hanger",
                   "Table2",
                   "Cupboard1",
                   "Cupboard2",
                   "Door"]
 
 
USAGE = {
    1: "Warm",
    2: "Cold"
}

OCCUPANCY = {
    0: "Free",
    1: "Busy"  
}

BLUE = 'b'
GREEN = 'g'
RED = 'r'
CYAN = 'c'
MAGENTA = 'm'
YELLOW = 'y'
BLACK = 'k'
WHITE = 'w'

GOOGLE_DRIVE_UPLOAD_ALLOWED = 1

TEST_MODE= 0
