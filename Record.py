'''record.py'''

import time
import cv2
import imutils
import numpy as np
import config

  
CHANGE_COORDINATES = []

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
    
    frame = cv2.fastNlMeansDenoisingColored(frame, None, 10, 10, 7, 15)
    background_model_resized = cv2.fastNlMeansDenoisingColored(background_model_resized, None, 10, 10, 7, 15)
    

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_background = cv2.cvtColor(background_model_resized, cv2.COLOR_BGR2GRAY)
    
  
    # perform histogram equalization using CLAHE on each pixel channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1_frame = clahe.apply(gray_frame)
    cl1_background = clahe.apply(gray_background)
    

    
    
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    cl1_frame = cv2.morphologyEx(gray_frame, cv2.MORPH_OPEN, kernel, iterations=3)
    cl1_background = cv2.morphologyEx(gray_background, cv2.MORPH_OPEN, kernel, iterations=3)
    """
    
    
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

''' original
def change_detection(fimage, first_image):
    ''' detect the chamges in the frame and return the change array'''
    status = 0
    change_co = []
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
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl1_frame = clahe.apply(gray_frame)
    cl1_background = clahe.apply(gray_background)
    
    cols1, rows1 = cl1_background.shape
    brightness1 = np.sum(cl1_background) / (255 * cols1 * rows1)
    
    
    cols2, rows2 = cl1_frame.shape
    brightness2 = np.sum(cl1_frame) / (255 * cols2 * rows2)
   
    
    frame_delta = cv2.absdiff(cl1_background, cl1_frame)
    
    #cv2.imshow('diff', frame_delta)
    
    blur = cv2.GaussianBlur(frame_delta, (5, 5), 0)
    thresh = cv2.threshold(blur, config.CHANGE_THRESHOLD,
                        255, cv2.THRESH_BINARY)[1]
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

'''
def start_recording(start_time, base_image=None):
    '''save image and video on a given time interval, returns ROI coordinates'''
    room_status = 0
    CHANGE_COORDINATES.clear()
    t = time.localtime()
    if config.TEST_MODE == 1:
        video = cv2.VideoCapture('input/input.avi')
    else:
        video = cv2.VideoCapture(0)
        time.sleep(2)
    ww = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    hw = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    starttimestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
    out = cv2.VideoWriter('{}OutputVideo{}.avi'.format(config.OUTPUT_PATH, starttimestamp), fourcc, 34, (int(ww), int(hw)))
    
    if base_image is not None:
        first_frame=base_image
    else:
        try:
            check, first_frame = video.read()
        except Exception as e:
            print(e)
            raise Exception(e)
        
    first_frame = cv2.GaussianBlur(first_frame, config.BLURR_SIZE, 0)
    
    count=0
    while (int(time.time() - start_time) < config.CAPTURE_DURATION):
        check, frame = video.read()
        count+=1
        if not check:
            break
        frame = cv2.GaussianBlur(frame, config.BLURR_SIZE, 0)
        if check == True:
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)

            (framedetect, change, room_status) = change_detection(
                frame, first_frame)

            cv2.putText(framedetect, 'WorkSpace is:', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 0, 255))
            if room_status == 0:
                cv2.putText(framedetect, "Free", (200, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 255, 0))
            else:
                cv2.putText(framedetect, "Busy", (200, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 0, 255))

            cv2.putText(framedetect, timestamp, (50, 75),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))

            cv2.imshow('LO-Watch', framedetect)
            out.write(framedetect)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cv2.imwrite('{}outputPicture{}.png'.format(config.OUTPUT_PATH, starttimestamp), framedetect)
    out.release()
    video.release()
    return(change,count)
