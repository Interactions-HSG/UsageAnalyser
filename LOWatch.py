import numpy as np
import cv2
import matplotlib.pyplot as plt
import time

#%matplotlib inline

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()


capture_duration = 30
video=cv2.VideoCapture(0)
w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

# detect person in the frame and mark the ROI using a rectangle frame
# return final frame and ROI coordinates
def personDetector(fimage):
    coordinates = []
    frame = cv2.resize(fimage, (640, 480))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    boxes, weights = hog.detectMultiScale(frame, winStride=(4,4))
    
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        height, width, ch = frame.shape
        cv2.rectangle(frame, (xA, yA), (xB, yB),(0, 255, 0), 2)
        xC=(xA+xB)/2
        yC=(yA+yB)/2
        coordinates.append((xC, yC))
        text="X="+str(xA)+" Y="+str(yA)
        cv2.putText(frame, text, (xA, yA), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
        
    
    return (frame, coordinates)


# save image and video on a given time interval $
# return ROI coordinates
def startWatching(start_time):
    t = time.localtime()
    starttimestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
    out = cv2.VideoWriter('output'+starttimestamp+'.avi', fourcc, 30, (int(w),int(h)))

    while (int(time.time() - start_time) < capture_duration ):
        video=cv2.VideoCapture(0)
        check,frame=video.read()
        if check == True: 
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
            cv2.putText(frame, timestamp, (200,500), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
            out.write(frame)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break 

    (showPic, coordinates)=personDetector(frame)
    cv2.imwrite('newCapture'+starttimestamp+'.jpg',showPic)
    out.release()
    video.release()
    #implot=plt.imshow(showPic)
    return coordinates
    cv2.destroyAllWindows()
    
