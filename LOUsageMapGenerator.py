from Scheduler import scheduler
from distanceCalc import calculateAndMap,getSerial
from time import sleep
import time
import config
import numpy as np
import cv2
import os
import zipfile
import logging
from googleUpload import upload_files



def createZip(name):
    filter=lambda name: '.zip' in name or '.DS_Store' in name
    try:
        with zipfile.ZipFile('{}.zip'.format(name), 'w', zipfile.ZIP_DEFLATED) as zipObj:
            for folderName, subfolders, filenames in os.walk(config.outputPath):
                for filename in filenames:
                    if filter(filename):
                        continue
                    filePath = os.path.join(folderName, filename)
                    zipObj.write(filePath)
                    if (lambda name: '.log' not in name)(filePath):
                        os.remove(filePath)
    except Exception as e:
        print(e)
        logging.debug(e)

''' generates scatter map and overlays on the empty room image for better analysis by the users '''
''' outputs found ROI coordinates and schedules the camera for reducing the battery life conservation '''
def generateMap():
    while True:
        ''' check room brightness '''
        room_default_brightness = config.roomBrightnessThreshold
        capture = cv2.VideoCapture(0)
        _, rawImage = capture.read()
        
        for i in config.furnitureCoordinates:
            x = config.furnitureCoordinates[i].get("x")
            y = config.furnitureCoordinates[i].get("y")
            w = config.furnitureCoordinates[i].get("w")
            h = config.furnitureCoordinates[i].get("h")
            xC = (x+w/2)
            yC = (y+h/2)
            cv2.circle(rawImage, (int(xC), int(yC)), 1, (255, 255, 255), 1)
            cv2.rectangle(rawImage, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.putText(rawImage, i, (x, y), cv2.FONT_HERSHEY_COMPLEX,
                        0.5, (255, 255, 255))
        
        config.inputImageSize=rawImage.shape[:-1][::-1]
        hsv = cv2.cvtColor(rawImage, cv2.COLOR_BGR2HSV)
        avg_color_per_row = np.average(hsv, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        brightness = avg_color[2]
        
        rawImageRGB=cv2.cvtColor(hsv,cv2.COLOR_HSV2RGB)
        
        if brightness > room_default_brightness:
            capture.release()
            try:
                
                (changeCoordinates, personCoordinates, occupancy) = scheduler()
                # print(coordinates)
                ''' imported function for calcuating the distance of a person from the objects '''
                calculateAndMap(rawImageRGB, changeCoordinates,
                                    personCoordinates, occupancy)

                if(config.googleDriveUploadAllowed == 1):
                        
                    sleep(2)
                    createZip('{}newRecording{}'.format(config.outputPath,getSerial()))
                    fileMetaData = {'name': 'newRecording{}'.format(getSerial()), 'time': time.strftime(
                                '%b-%d-%Y_%H%M%S', time.localtime())}
                    results = upload_files('{}newRecording{}'.format(config.outputPath,getSerial()), fileMetaData)
                    print('File uploaded ID: {}'.format(results.get('id')))
                    logging.info('Files uploaded ID: {}'.format(results.get('id')))
                        

                    ''' device goes to sleep '''
                if config.testMode==0:
                    sleep(config.sleepDuration)
                else:
                    logging.info('testing!!! please set testMode to 0 in configuration file for full mode...')
                    break
            except Exception as e:
                print(e)
                logging.debug(e)

        else:
            
            capture.release()
            print('The room is too dark for a photo!')
            logging.info('The room is too dark for a photo {}!'.format(time.strftime('%b-%d-%Y_%H%M%S', time.localtime())))
            if config.testMode==0:
                sleep(config.sleepDuration)
            else:
                logging.info('testing!!! please set testMode to 0 in configuration file for full mode...')
                
                break
        #capture.release()
    
        
def main(): 
    # raw_pic=config.rawImagePath
    logging.basicConfig(filename=
                        '{}LOWatch.log'.format(config.outputPath), level=logging.DEBUG)

    generateMap()

if __name__ == "__main__":
    main()
