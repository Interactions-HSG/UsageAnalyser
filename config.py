
from pathlib import Path
home = str(Path.home())

frozenInferenceGraph= r'pre-trained-set/frozen_inference_graph.pb'
trainNodeDescription= r'pre-trained-set/output.pbtxt'

rawImagePath = r'images/61-402layout.png'

windowSize= (8,8)

imageResolution= (720, 1080)
faceClassifierAddress= home+r'/downloads/opencv-3.4/data/haarcascades/haarcascade_frontalface_default.xml'
'''
to run on raspberry pi uncomment the line below 'saved opencv-3.4.0 folder inside the local folder'
'''
#faceClassifierAddress= r'opencv-3.4.0/data/haarcascades/haarcascade_frontalface_default.xml'
captureDuration = 120
sleepDuration = 3600

outputPath= r'output/'

modelFile = r'tflite_models/detect.tflite'
labelPath = r'tflite_models/person-labelmap.txt'

inputImageSize = (640,480)
blurrSize = (1,1)


furnitureCoordinates={
    "table" : (300,200),
    "cupboard" :(100,50)
}
blue='b'
green='g'
red='r'
cyan='c'
magenta='m'
yellow='y'
black='k'
white='w'