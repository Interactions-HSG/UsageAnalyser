
from pathlib import Path
home = str(Path.home())

frozenInferenceGraph = r'pre-trained-set/frozen_inference_graph.pb'
trainNodeDescription = r'pre-trained-set/output.pbtxt'

rawImagePath = r'images/61-402layout.png'

windowSize = (8, 8)

imageResolution = (720, 1080)
faceClassifierAddress = home + \
    r'/downloads/opencv-3.4/data/haarcascades/haarcascade_frontalface_default.xml'
'''
to run on raspberry pi uncomment the line below 'saved opencv-3.4.0 folder inside the local folder'
'''
#faceClassifierAddress= r'opencv-3.4.0/data/haarcascades/haarcascade_frontalface_default.xml'
captureDuration = 120
sleepDuration = 3600

outputPath = r'output/'

modelFile = r'tflite_models/detect.tflite'
labelPath = r'tflite_models/person-labelmap.txt'

inputImageSize = (640, 480)
blurrSize = (51, 51)


furnitureCoordinates = {
    "table": {"x": 300, "y": 200, "w": 100, "h": 200},
    "cupboard": {"x": 100, "y": 50, "w": 50, "h": 150}
}

occupancy = {
    0: "unknown",
    1: "Warm",
    2: "Cold",
    3: "Free"
}

blue = 'b'
green = 'g'
red = 'r'
cyan = 'c'
magenta = 'm'
yellow = 'y'
black = 'k'
white = 'w'

googleDriveUploadAllowed = 1

testMode = 0