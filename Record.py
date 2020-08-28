# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils
import numpy as np
import config
import csv
import threading

#/home/pi/UsageAnalyser1/templates/index.html
LOCK = threading.Lock()
CHANGE_COORDINATES = []
StreamFrame = None
COUNT = None
BLUR_LEVEL = None



def stream_frame():
    """capture and return the most recent frame"""
    global StreamFrame
    if StreamFrame.any() != None:
        return StreamFrame
    else:
        raise Exception("No frames  currently available")

def change_detection(fimage, first_image):
    ''' detect the changes in the frame and return the change array'''
    status = 0
    change_co = []
    trackers_co = []

    if hasattr(fimage, 'shape'):
        config.INPUT_IMAGE_SIZE = fimage.shape[:-1][::-1]
    else:
        fimage = cv2.imread(fimage)
        config.INPUT_IMAGE_SIZE = fimage.shape[:-1][::-1]
        first_image = cv2.imread(first_image)
    background_model_resized = cv2.resize(first_image, config.INPUT_IMAGE_SIZE)
    frame = cv2.resize(fimage, config.INPUT_IMAGE_SIZE)
    

    

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_background = cv2.cvtColor(background_model_resized, cv2.COLOR_BGR2GRAY)
    
  
    # perform histogram equalization using CLAHE on each pixel channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1_frame = clahe.apply(gray_frame)
    cl1_background = clahe.apply(gray_background)
    
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    cl1_frame = cv2.morphologyEx(gray_frame, cv2.MORPH_OPEN, kernel, iterations=3)
    cl1_background = cv2.morphologyEx(gray_background, cv2.MORPH_OPEN, kernel, iterations=3)
    
    
    cl1_background = np.float32(cl1_background)

    cv2.accumulateWeighted(cl1_frame, cl1_background, 0.1)
    
    # get pixel-wise differences between current frame and avg. frame
    
    frame_delta = cv2.absdiff(cl1_frame, cv2.convertScaleAbs(cl1_background))
    
    #frame_delta = cv2.absdiff(cl1_background, cl1_frame)
        
    blur = cv2.GaussianBlur(frame_delta, (5, 5), 0)
    thresh = cv2.threshold(blur, config.CHANGE_THRESHOLD,config.CHANGE_THRESHOLD_MAX, cv2.THRESH_BINARY)[1]
    
    #thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    thresh = cv2.dilate(thresh, None, iterations=3)
    
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:

        (x, y, w, h) = cv2.boundingRect(c)

        if ((w < config.CHANGE_DISTANCE_MIN and h < config.CHANGE_DISTANCE_MIN)or(w > config.CHANGE_DISTANCE_MAX and h > config.CHANGE_DISTANCE_MAX)):
            continue
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        status = 1

        M = cv2.moments(c)
        xC = int((M["m10"] / M["m00"]))
        yC = int((M["m01"] / M["m00"]))
        
        CHANGE_COORDINATES.append([xC, yC])
        change_co = np.array(CHANGE_COORDINATES)



    return (frame, change_co, status)


def blur_images(image, base_image):
    """ blur the current frame and the base_image and return both frames """
    global BLUR_LEVEL
    BLUR_LEVEL=cv2.Laplacian(image, cv2.CV_64F).var()
          
    if base_image is not None:
            first_frame=base_image
    else:
            try:
                first_frame = image
            except Exception as e:
                print(e)
                raise Exception(e)
        
    first_frame = cv2.GaussianBlur(first_frame, config.BLURR_SIZE, 0)
    frame = cv2.GaussianBlur(image, config.BLURR_SIZE, 0)
    
    return first_frame, frame

def show_frame(framedetect, room_status):
    """ Take the frame with the displayed changes, add additional visualisations and show the image"""    

    t = time.localtime()
    timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
    cv2.putText(framedetect, 'WorkSpace is:', (50, 50),
    cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 0, 255))
    if room_status == 0:
                        cv2.putText(framedetect, "Free", (200, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 255, 0))
    else:
                        cv2.putText(framedetect, "Busy", (200, 50),
                                    cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 0, 255))
                        
    cv2.putText(framedetect, "{:.2f}".format(BLUR_LEVEL), (50, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)

    cv2.putText(framedetect, timestamp, (50, 75),cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))

    cv2.imshow('LO-Watch', framedetect)
                  
    
            
def start_recording(start_time, base_image=None):
    """ Start recording the room and return change coordinates and amount of checks"""
    global LOCK
    global COUNT
    COUNT=0
    room_status = 0
    CHANGE_COORDINATES.clear()
    starttimestamp = time.strftime('%b-%d-%Y_%H%M%S', time.localtime())

    # Configure the functionality to save the recording in an AVI file
    height, width, layers = base_image.shape
    size = (width, height)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('{}outputVideo{}.avi'.format(config.OUTPUT_PATH,starttimestamp),fourcc, 15, size)
                    
    # Configure and start the raspberryPi camera to collect frames from the camera port
    camera = PiCamera()   
    camera.resolution = config.IMAGE_RESOLUTION
    camera.framerate = config.FPS
    rawCapture = PiRGBArray(camera, size=config.IMAGE_RESOLUTION)
    # allow the camera to warmup
    time.sleep(0.1)
 
    # capture the frames from the camera in a continous stream, blurr the image, detect changes and show the frame
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        COUNT+=1 
        image = frame.array
        (first_frame, frame) = blur_images(image, base_image)
        (framedetect, change, room_status) = change_detection(frame, first_frame)
        show_frame(framedetect, room_status)
        out.write(framedetect)

        rawCapture.truncate(0)

        with LOCK:
            global StreamFrame
            StreamFrame = framedetect.copy()        
                                   
        if cv2.waitKey(1) & 0xFF == ord('q') or (int(time.time() - start_time) > config.CAPTURE_DURATION):
                       break
                  

    out.release()
    cv2.imwrite('{}outputPicture{}.png'.format(config.OUTPUT_PATH, starttimestamp), framedetect)
    #camera.stop_recording()
    camera.close()

    return(change,COUNT)