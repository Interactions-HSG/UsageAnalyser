'''Start file and Output file generators'''
import time
import zipfile
import logging
import csv
import os
import cv2
import numpy as np
from googleUpload import upload_files
from googleUpload import get_file
import Record
import config
import requests
import webserver
import threading

from distanceCalc import calculate_and_map, get_serial
from checkInternetConnection import connect
from picamera.array import PiRGBArray
from picamera import PiCamera

def adapt_blur(raw_image):
    """Check blur level of the raw image and adapt the additional internal level depending on blur level of the raw image"""
    BLUR_LEVEL=cv2.Laplacian(raw_image, cv2.CV_64F).var()
    print(BLUR_LEVEL)
    try:
        if BLUR_LEVEL > 15:
            config.BLURR_SIZE = (3,3)
        elif (BLUR_LEVEL > 9) and (BLUR_LEVEL < 15):
            config.BLURR_SIZE = (3,3)
        elif BLUR_LEVEL < 9:
            config.BLURR_SIZE = (5,5)
    except Exception as e:
            print(e)
            raise Exception(e)

def create_zip(name):
    """create zip file for the final output"""
    def filter(name): return '.zip' in name or '.DS_Store' in name
    try:
        with zipfile.ZipFile('{}.zip'.format(name), 'w', zipfile.ZIP_DEFLATED) as zip_obj:
            for folder_name, subfolders, filenames in os.walk(config.OUTPUT_PATH):
                for filename in filenames:
                    if filter(filename):
                        continue
                    file_path = os.path.join(folder_name, filename)
                    zip_obj.write(file_path)
                    if (lambda name: '.log' not in name)(file_path):
                        os.remove(file_path)
    except Exception as e:
        print(e)
        logging.debug(e)

def create_base_image():
    """Take a first frame that will be used as groundtruth to compare subsequent frames and return the frame"""
    camera = PiCamera()

    camera.resolution = config.IMAGE_RESOLUTION
    camera.framerate = config.FPS
    time.sleep(2)
        
    with PiRGBArray(camera) as output:
        camera.capture(output, format='bgr')
        raw_image = output.array
            
            #print('Captured %dx%d image' % (
            #        output.array.shape[1], output.array.shape[0]))
            
        output.truncate(0)
        camera.close()
    camera.close()
    return raw_image

def generate_map():
    """ generates scatter map and overlays on the empty room image for better analysis by the users 
     outputs found ROI coordinates and schedules the camera for reducing the battery life conservation """
    
    raw_image = create_base_image()
    adapt_blur(raw_image)
    room_default_brightness = config.ROOM_BRIGHTNESS_THRESHOLD
    
    while True:
        ''' check room brightness '''

        config.INPUT_IMAGE_SIZE = raw_image.shape[:-1][::-1]
        hsv = cv2.cvtColor(raw_image.copy(), cv2.COLOR_BGR2HSV)
        avg_color_per_row = np.average(hsv, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        brightness = avg_color[2]

        
        if brightness > room_default_brightness:
            #capture.release()
            try:  
                (change,count) = Record.start_recording(time.time(), raw_image)
                ''' imported function for calcuating the distance of a person from the objects '''
                f = open('{}outputTable{}.csv'.format(config.OUTPUT_PATH, time.strftime(
                    '%b-%d-%Y_%H%M%S', time.localtime())), "w")
                writer = csv.DictWriter(f, fieldnames=[
                    "Timestamp", "Furniture_Type", "Usage_Count", "Total_Checks", "Usage_Percentage", "Usage_Type", "Room_Occupancy", "Usage amount", "Device_ID"])
                writer.writeheader()
                
                calculate_and_map(raw_image, change, writer, count)
                f.close()

                if(config.GOOGLE_DRIVE_UPLOAD_ALLOWED == 1 and connect() == True):
                    serial = get_serial()
                    time_ = time.strftime(
                        '%b-%d-%Y_%H%M%S', time.localtime())
                    name = serial+time_
                    
                    time.sleep(2)
                    create_zip('{}newRecording{}'.format(
                        config.OUTPUT_PATH, name))
                    file_meta_data = {'name': 'newRecording{}'.format(name), 'time': time.strftime(
                        '%b-%d-%Y_%H%M%S', time.localtime())}
                    results = upload_files('{}newRecording{}'.format(
                        config.OUTPUT_PATH, name), file_meta_data)
                    print("results are",results)
                    print('File uploaded ID: {}'.format(results.get('id')))
                    logging.info(
                        'Files uploaded ID: {}'.format(results.get('id')))
                    
                  
                    
                    
                elif(connect() == False):
                    logging.info("Output files are being stored on local device because system is not connected to the internet!")
                    
                

            except Exception as e:
                print(e)
                logging.debug(e)

            if config.TEST_MODE == 1:
                logging.info(
                    'Testing! please set testMode to 0 in configuration file for full mode...')
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            #capture.release()
            print('The room is too dark for a photo!')
            logging.info('The room is too dark for a photo {}!'.format(
                time.strftime('%b-%d-%Y_%H%M%S', time.localtime())))
            if config.TEST_MODE == 0:
                time.sleep(config.SLEEP_DURATION)
            else:
                logging.info(
                    'testing!!! please set testMode to 0 in configuration file for full mode...')

                break
        # capture.release()
        cv2.destroyAllWindows()

def main():
    """main function"""
    
    logging.basicConfig(filename='{}LOWatch.log'.format(
        config.OUTPUT_PATH),format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S', level=logging.DEBUG)
    
    # start a thread that will perform motion detection
    t = threading.Thread(target=generate_map, args=())
    t.daemon = True
    t.start()





    webserver.main()
    

if __name__ == "__main__":
    main()

