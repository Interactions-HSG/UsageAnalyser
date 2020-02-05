import numpy as np
import cv2
import time
import imutils
import config
import tfdetect as tf
from random import seed
from random import randint

'''
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
face_cascade = cv2.CascadeClassifier(config.faceClassifierAddress)
'''
capture_duration = config.captureDuration
firstFrame = None
coordinates = []
changeCoordinates = []
personCoordinates = []

''' detect person in the frame and mark the ROI using a rectangle frame
 return final frame and ROI coordinates '''


def personDetector(fimage):
    coordinates = []
    (ww, hw) = fimage.size
    frame = cv2.resize(fimage, (int(ww), int(hw)))
    # using a greyscale picture, also for faster detection
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    faces = face_cascade.detectMultiScale(frame, 1.1, 4)
    boxes, weights = hog.detectMultiScale(frame, winStride=(4, 4))

    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    ''' Blur any captured face '''
    for (x, y, w, h) in faces:
        roi_blur = frame[y:y+h, x:x+w]
        blur = cv2.GaussianBlur(roi_blur, (101, 101), 0)
        frame[y:y+h, x:x+w] = blur

    for (xA, yA, xB, yB) in boxes:
        ''' display the detected boxes in the colour picture'''
        height, width, ch = frame.shape
        cv2.rectangle(frame, (int(xA), int(yA)),
                      (int(xB), int(yB)), (0, 255, 0), 2)
        xC = (xA+xB)/2
        yC = (yA+yB)/2 - yA/2
        coordinates.append((xC, yC))
        text = "X="+str(xA)+" Y="+str(yA)
        cv2.putText(frame, text, (int(xA), int(yA)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))

    return (frame, coordinates)


''' detect the biggest blobs and mark them down as highest probability of being a human being'''
def changeDetection(fimage, firstImage):
    status = 0
    if hasattr(fimage,'shape'):
        config.inputImageSize=fimage.shape[:-1][::-1]
    else:
        fimage=cv2.imread(fimage)
        config.inputImageSize=fimage.shape[:-1][::-1]
        firstImage=cv2.imread(firstImage)
    backgroundModelresized = cv2.resize(firstImage, config.inputImageSize)
    #firstFrame = cv2.cvtColor(backgroundModelresized, cv2.COLOR_BGR2GRAY)
    #firstFrame = cv2.GaussianBlur(firstFrame, (21, 21), 0)
    frame = cv2.resize(fimage, config.inputImageSize)
    frameDelta = cv2.absdiff(backgroundModelresized, frame)
    gray = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, config.changeThreshold, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=3)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    personDectected = 0

    for c in cnts:

        (x, y, w, h) = cv2.boundingRect(c)

        if ((w < config.changeAreaMin and h < config.changeAreaMin)or(w > config.changeAreaMax and h > config.changeAreaMax)):
            continue
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.drawContours(frame,[c],-1,(0,255,0),2)
        status = 1

        #xC=(x+(x+w))/2
        #yC=(y+(y+h))/2 -y/2
        #changeCoordinates.append([xC, yC])
        
        M = cv2.moments(c)
        xC = int((M["m10"] / M["m00"]))
        yC = int((M["m01"] / M["m00"]))
        changeCoordinates.append([xC, yC])

        #(frame, object_name,coordinate)=tf.detect(frame)
        # personCoordinates.append(coordinate)
        # if(object_name=="person"):
        # personDectected=1
    #return (frame, changeCoordinates, personCoordinates, status, personDectected)
    return (frame, changeCoordinates, status)

# DNN used for people head detection
classNames = {
    0: 'person'
}


def id_class_name(class_id, classes):
    for key, value in classes.items():
        if class_id == key:
            return value


def headDetection(fimage):
    model = cv2.dnn.readNetFromTensorflow(
        config.frozenInferenceGraph, config.trainNodeDescription)

    blurdullimage = fimage
    # blurimage=cv2.blur(image,(1,1))
    blurimage = cv2.blur(blurdullimage, (1, 1))
    #blurimage=cv2.addWeighted(blurdullimage, 1.0, np.zeros(blurdullimage.shape, blurdullimage.dtype), 0, 0)
    image_height, image_width, _ = fimage.shape
    model.setInput(cv2.dnn.blobFromImage(
        fimage, size=config.inputImageSize, swapRB=True))
    output = model.forward()
    # print(output[0,0,:,:].shape)

    for detection in output[0, 0, :, :]:
        confidence = detection[2]
        if confidence > .5:
            class_id = detection[1]
            class_name = id_class_name(class_id, classNames)
            print(str(str(class_id) + " " +
                      str(detection[2]) + " " + class_name))
            box_x = detection[3] * image_width
            box_y = detection[4] * image_height
            box_width = detection[5] * image_width
            box_height = detection[6] * image_height
            xC = (box_x+box_width)/2
            yC = (box_y+box_height)/2 - box_y/2
            coordinates.append((xC, yC))
            cv2.rectangle(fimage, (int(box_x), int(box_y)), (int(
                box_width), int(box_height)), (23, 230, 210), thickness=1)
            cv2.putText(fimage, str(round((float(detection[2])*100), 2))+'%'+''+class_name, (int(
                box_x), int(box_y+.02*image_height)), cv2.FONT_HERSHEY_SIMPLEX, (1), (0, 0, 255))

    return (fimage, coordinates)


def decision(personDetected, status):
    Occupancy = 0
    if(personDetected == 1 and status == 1):
        Occupancy = 1
    elif(personDetected == 0 and status == 1):
        Occupancy = 2
    elif(status == 0 and personDetected == 0):
        Occupancy = 3 
    elif(status== 0 and personDetected == 1):
        Occupancy = 1   
    return Occupancy

''' save image and video on a given time interval $
 return ROI coordinates'''


def startWatching(start_time):
    RoomStatus = 0
    personDectected = 0
    personCoordinates.clear()
    changeCoordinates.clear()
    frameArray=[]
    t = time.localtime()
    video = cv2.VideoCapture(0)
    ww = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    hw = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    starttimestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
    out = cv2.VideoWriter('{}outputVideo{}.avi'.format(config.outputPath,starttimestamp), fourcc, 10, (int(ww), int(hw)))
    check, firstFrame = video.read()
    firstFrame = cv2.GaussianBlur(firstFrame, config.blurrSize, 0)
    while (int(time.time() - start_time) < capture_duration):
        check, frame = video.read()
        frameArray.append(frame)
        frame = cv2.GaussianBlur(frame, config.blurrSize, 0)
        if check == True:
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M%S', t)
            '''
            faces = face_cascade.detectMultiScale(frame, 1.1, 4)
            
            for (x, y, w, h) in faces:
                roi_blur = frame[y:y+h, x:x+w]
                blur = cv2.GaussianBlur(
                    roi_blur, (101, 101), cv2.BORDER_TRANSPARENT)
                frame[y:y+h, x:x+w] = blur
            '''
            (framedetect, change, RoomStatus) = changeDetection(frame, firstFrame)

            cv2.putText(framedetect, 'WorkSpace is:', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, (0.5), (0, 0, 255))
            if RoomStatus == 0:
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
    
    if len(frameArray)>0:
        seed(1)
        
        for _ in range(5):
            i=randint(0,len(frameArray)-1)
            (frame, object_name, coordinate) = tf.detect(frameArray[i])
            personCoordinates.append(coordinate)
            if(object_name == "person"):
                personDectected = 1
    assert (RoomStatus==1 or RoomStatus==0), 'RoomStatus must be bool'
    occupancy = decision(personDectected, RoomStatus)
    #(showPic, coordinates)=personDetector(frame)
    cv2.putText(frame, "People: {}".format(personDectected), (50, 100),
                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))

    cv2.imwrite('{}outputPicture{}.png'.format(config.outputPath,starttimestamp), framedetect)
    
    out.release()
    video.release()
    cv2.destroyAllWindows()
    return (change, personCoordinates, occupancy)
