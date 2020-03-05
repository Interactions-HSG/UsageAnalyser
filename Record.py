'''record.py'''

import time
import cv2
import imutils
import numpy as np
import config
 
  
CHANGE_COORDINATES = []

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
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpen_frame = cv2.filter2D(frame, -1, sharpen_kernel)
    sharpen_background_model_resized = cv2.filter2D(background_model_resized, -1, sharpen_kernel)
    frame_delta = cv2.absdiff(sharpen_background_model_resized, sharpen_frame)
    gray = cv2.cvtColor(frame_delta, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, config.CHNGAE_THRESHOLD,
                        255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=3)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:

        (x, y, w, h) = cv2.boundingRect(c)

        if ((w < config.CHNAGE_AREA_MIN and h < config.CHNAGE_AREA_MIN)or(w > config.CHANGE_AREA_MAX and h > config.CHANGE_AREA_MAX)):
            continue
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        status = 1

        M = cv2.moments(c)
        xC = int((M["m10"] / M["m00"]))
        yC = int((M["m01"] / M["m00"]))
        CHANGE_COORDINATES.append([xC, yC])
        
        change_co = np.array(CHANGE_COORDINATES)
    return (frame, change_co, status)


def start_recording(start_time, base_image=None):
    '''save image and video on a given time interval, returns ROI coordinates'''
    room_status = 0
    CHANGE_COORDINATES.clear()
    t = time.localtime()
    if config.TEST_MODE == 1:
        video = cv2.VideoCapture(config.INPUT_PATH)
    else:
        video = cv2.VideoCapture(0)
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
    while (int(time.time() - start_time) < config.CAPTURE_DURATION):
        check, frame = video.read()
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
    return change
