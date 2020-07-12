# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils
import numpy as np
import config
# from LOUsageMapGenerator import camera


VIDEO_BASE_FOLDER = r'output/'
now = time.localtime()
OUTPUT_PATH = r'output/'
img_array = []
  
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

def get_video_filename(now):
    now = str(now)
    #return VIDEO_BASE_FOLDER+str(now)+'_video.mpjg'
    return '{}OutputVideo{}.mjpeg'.format(config.OUTPUT_PATH, now)

#     out = cv2.VideoWriter('{}OutputVideo{}.avi'.format(config.OUTPUT_PATH, starttimestamp), fourcc, 34, (int(ww), int(hw)))



def start_recording(start_time, base_image=None):
    room_status = 0
    CHANGE_COORDINATES.clear()
    t = time.localtime()
    starttimestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
    
    
    #start_time = time.time()
    # initialize the camera and grab a reference to the raw camera capture
    width = 720
    height = 1280
    camera = PiCamera()

#    camera = LOUsageMapGenerator.camera
    

    camera.resolution = (1280, 720)
    camera.framerate = 32
    time.sleep(2)

    
    with PiRGBArray(camera) as output:
        camera.capture(output, 'rgb')
        base_image = output.array
        
        output.truncate(0)
        

   
    camera.resolution = (1280, 720)
    camera.framerate = 32
    

    rawCapture = PiRGBArray(camera, size=(1280, 720))
    camera.start_recording(get_video_filename(starttimestamp), format='bgr') 
    # allow the camera to warmup
    time.sleep(0.1)
 
    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
        image = frame.array
        check = True
        
#         
        
        if base_image is not None:
            first_frame=base_image
        else:
            try:
                first_frame = image
                check = check
            except Exception as e:
                print(e)
                raise Exception(e)
        
        first_frame = cv2.GaussianBlur(first_frame, config.BLURR_SIZE, 0)
        count=0
        
#        while (int(time.time() - start_time) < config.CAPTURE_DURATION):
        frame = image
        count+=1
        if check == False:
            break
        frame = cv2.GaussianBlur(frame, config.BLURR_SIZE, 0)
        if check == True:
                    t = time.localtime()
                    timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
                    (framedetect, change, room_status) = change_detection(frame, first_frame)
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
                    rawCapture.truncate(0)
                    """
                    img = cv2.imread(framedetect)
                    height, width, layers = img.shape
                    size = (width, height)
                    img_array.append(img)
                    out = cv2.VideoWriter('{}outputVideo{}.avi'.format(config.OUTPUT_PATH,starttimestamp),cv2.VideoWriter_fourcc(*'MPJG'), 15, size)
                    out.write(framedetect)
                    """

#                    out.write(framedetect)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        check = False
                        camera.stop_recording()

                        break
                        
        else:
                        break
            
        
    cv2.imwrite('{}outputPicture{}.png'.format(config.OUTPUT_PATH, starttimestamp), framedetect)
    cv2.destroyAllWindows()

#    out.release()
#    camera.stop_recording()

    return(change,count)
"""            
       
"""
