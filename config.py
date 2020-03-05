"""Config.py"""

from pathlib import Path
HOME= str(Path.home())

RAW_IMAGE_PATH = r'images/61-402layout.png'

WINDOW_SIZE = (8, 8)

IMAGE_RESOLUTION = (640, 360)
FACECLASSIFIER_ADDRESS = HOME + \
    r'/downloads/opencv-3.4/data/haarcascades/haarcascade_frontalface_default.xml'
'''
to run on raspberry pi uncomment the line below 'saved opencv-3.4.0 folder inside the local folder'
'''
#FACECLASSIFIER_ADDRESS= r'opencv-3.4.0/data/haarcascades/haarcascade_frontalface_default.xml'
CAPTURE_DURATION = 120
SLEEP_DURATION = 900
COLD_COUNT=1000

OUTPUT_PATH = r'output/'
INPUT_PATH = r'input/input.avi'

DEFAULT_DISTANCE = 50
CHNGAE_THRESHOLD = 50
CHNAGE_AREA_MIN = 50
CHANGE_AREA_MAX = 300


MODEL_FILE = r'tflite_models/detect.tflite'
LABEL_PATH = r'tflite_models/person-labelmap.txt'

INPUT_IMAGE_SIZE = (640, 480)
BLURR_SIZE = (31, 31)

ROOM_BRIGHTNESS_THRESHOLD = 50


"""(x,y,width,height)"""
FURNITURE_COORDINATES = [(20, 150, 50, 70),
                         (20, 215, 50, 70),
                         (80, 110, 150, 80),
                         (80, 215, 150, 80),
                         (400, 240, 130, 60),
                         (400, 30, 90, 180),
                         (100, 50, 70, 50),
                         (40, 330, 70, 50),
                         (400, 300, 110, 170)]

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