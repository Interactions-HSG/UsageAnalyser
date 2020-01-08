import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
import imutils
import config

#%matplotlib inline

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
face_cascade = cv2.CascadeClassifier(config.faceClassifierAddress)

#cv2.startWindowThread()


capture_duration = config.captureDuration
video=cv2.VideoCapture(0)

ww = video.get(cv2.CAP_PROP_FRAME_WIDTH)
hw = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')

firstFrame = None

# detect person in the frame and mark the ROI using a rectangle frame
# return final frame and ROI coordinates
def personDetector(fimage):
    coordinates = []
    frame = cv2.resize(fimage, (int(ww),int(hw)))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    faces = face_cascade.detectMultiScale(frame, 1.1, 4)
    boxes, weights = hog.detectMultiScale(frame, winStride=(4,4))
    
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
    
    #Blur any captured face
    for (x, y, w, h) in faces:
        roi_blur = frame[y:y+h, x:x+w]
        blur = cv2.GaussianBlur(roi_blur, (101,101), 0)       
        frame[y:y+h, x:x+w] = blur

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        height, width, ch = frame.shape
        cv2.rectangle(frame, (int(xA), int(yA)), (int(xB), int(yB)),(0, 255, 0), 2)
        xC=(xA+xB)/2
        yC=(yA+yB)/2 -yA/2
        coordinates.append((xC, yC))
        text="X="+str(xA)+" Y="+str(yA)
        cv2.putText(frame, text, (int(xA), int(yA)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
    
    return (frame, coordinates)

#detect the biggest blobs and mark them down as highest probability of being a human being
def changeDetection(fimage):
    backgroundModelPath = config.rawImagePath
    backgroundModel = cv2.imread(backgroundModelPath)
    backgroundModelresized = cv2.resize(backgroundModel, (1080,720))
    firstFrame = cv2.cvtColor(backgroundModelresized, cv2.COLOR_BGR2GRAY)
    firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
    frame = cv2.resize(fimage, (1080, 720))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 50, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        if w>100 and h>100 :
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            continue
    return frame

# DNN used for people head detection
classNames = {
              0: 'person'
             }

def id_class_name(class_id, classes):
    for key,value in classes.items():
        if class_id == key:
            return value
coordinates = []
def headDetection(fimage):
    model = cv2.dnn.readNetFromTensorflow(config.frozenInferenceGraph, config.trainNodeDescription)

    blurdullimage = fimage
    #blurimage=cv2.blur(image,(1,1)) 
    blurimage=cv2.blur(blurdullimage,(1,1)) 
    #blurimage=cv2.addWeighted(blurdullimage, 1.0, np.zeros(blurdullimage.shape, blurdullimage.dtype), 0, 0)
    image_height, image_width, _ = fimage.shape
    model.setInput(cv2.dnn.blobFromImage(fimage, size=(300, 300), swapRB=True))
    output = model.forward()
    #print(output[0,0,:,:].shape)

    for detection in output[0,0,:,:]:
        confidence = detection[2]
        if confidence > .7:
            class_id = detection[1]
            class_name=id_class_name(class_id,classNames)
            print(str(str(class_id) + " " + str(detection[2])  + " " + class_name ))
            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height
            xC=(box_x+box_width)/2
            yC=(box_y+box_height)/2 -box_y/2
            coordinates.append((xC, yC))
            cv2.rectangle(fimage, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)
            cv2.putText(fimage,str(float(detection[2])*100)+'%'+''+class_name ,(int(box_x), int(box_y+.02*image_height)),cv2.FONT_HERSHEY_SIMPLEX,(1),(0, 0, 255))
    
    return (fimage,coordinates)

# save image and video on a given time interval $
# return ROI coordinates
def startWatching(start_time):
    t = time.localtime()
    starttimestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
    out = cv2.VideoWriter('output'+starttimestamp+'.avi', fourcc, 10, (int(ww),int(hw)))

    while (int(time.time() - start_time) < capture_duration ):
        video=cv2.VideoCapture(0)
        check,frame=video.read()
        if check == True: 
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
            cv2.putText(frame, timestamp, (200,500), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
            faces = face_cascade.detectMultiScale(frame, 1.1, 4)
            for (x, y, w, h) in faces:
                roi_blur = frame[y:y+h, x:x+w]
                blur = cv2.GaussianBlur(roi_blur, (101,101), 0)       
                frame[y:y+h, x:x+w] = blur
            (framedetect,coordinates)=headDetection(frame)
            cv2.imshow('frame',framedetect)
            out.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break 
        
    #(showPic, coordinates)=personDetector(frame)
    
    cv2.imwrite('newCapture'+starttimestamp+'.jpg',frame)
    out.release()
    video.release()
    #implot=plt.imshow(showPic)
    return coordinates
    cv2.destroyAllWindows()
    
#startWatching(time.time())
