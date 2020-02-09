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
CAPTURE_DURATION = 43200
SLEEP_DURATION = 900

OUTPUT_PATH = r'output/'
INPUT_PATH = r'input/'

DEFAULT_DISTANCE = 50
CHNGAE_THRESHOLD = 50
CHNAGE_AREA_MIN = 50
CHANGE_AREA_MAX = 300


MODEL_FILE = r'tflite_models/detect.tflite'
LABEL_PATH = r'tflite_models/person-labelmap.txt'

INPUT_IMAGE_SIZE = (640, 480)
BLURR_SIZE = (31, 31)

ROOM_BRIGHTNESS_THRESHOLD = 50

FURNITURE_COORDINATES = {
    "table": {"x": 250, "y": 130, "w": 180, "h": 108},
    "whiteBoard": {"x": 320, "y": 350, "w": 150, "h": 150},
    "glassBoard":{"x": 50, "y": 150, "w": 110, "h": 90}
    
}

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

GOOGLE_DRIVE_UPLOAD_ALLOWED = 0

TEST_MODE= 0