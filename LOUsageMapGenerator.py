import time
import zipfile
import logging
import csv
import os
import cv2
import numpy as np
from googleUpload import upload_files
import Record
import config
from distanceCalc import calculate_and_map, get_serial
from furniture import furniture

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


def generate_map():
    """ generates scatter map and overlays on the empty room image for better analysis by the users 
     outputs found ROI coordinates and schedules the camera for reducing the battery life conservation """
    capture1 = cv2.VideoCapture(0)
    _, raw_image = capture1.read()
    capture1.release()
    room_default_brightness = config.ROOM_BRIGHTNESS_THRESHOLD
    while True:
        ''' check room brightness '''
        capture = cv2.VideoCapture(0)
        _,sample=capture.read()
        furniture_obj = furniture(config.FURNITURE_NAMES, config.FURNITURE_COORDINATES)
        furniture_coordinates = furniture_obj.getCoordinateDict()
        
        for i in furniture_coordinates:
            x = furniture_coordinates[i].get("x")
            y = furniture_coordinates[i].get("y")
            w = furniture_coordinates[i].get("w")
            h = furniture_coordinates[i].get("h")
            xC = (x+w/2)
            yC = (y+h/2)
            cv2.circle(raw_image, (int(xC), int(yC)), 1, (255, 255, 255), 1)
            cv2.rectangle(raw_image, (x, y), (x + w, y + h),
                          (255, 255, 255), 2)
            cv2.putText(raw_image, i, (x, y), cv2.FONT_HERSHEY_COMPLEX,
                        0.5, (255, 255, 255))

        config.INPUT_IMAGE_SIZE = raw_image.shape[:-1][::-1]
        hsv = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)
        avg_color_per_row = np.average(hsv, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        brightness = avg_color[2]
        raw_image_RGB = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)

        if brightness > room_default_brightness:
            capture.release()
            try:

                change = Record.start_recording(time.time(), raw_image)
                # print(coordinates)

                ''' imported function for calcuating the distance of a person from the objects '''
                f = open('{}outputTable{}.csv'.format(config.OUTPUT_PATH, time.strftime(
                    '%b-%d-%Y_%H%M%S', time.localtime())), "w")
                writer = csv.DictWriter(f, fieldnames=[
                    "Timestamp", "Furniture_Type", "Usage_Count", "Usage_Type", "Room_Occupancy", "Device_ID"])
                writer.writeheader()
                calculate_and_map(raw_image, change, writer)
                f.close()

                if(config.GOOGLE_DRIVE_UPLOAD_ALLOWED == 1):

                    time.sleep(2)
                    create_zip('{}newRecording{}'.format(
                        config.OUTPUT_PATH, get_serial()))
                    file_meta_data = {'name': 'newRecording{}'.format(get_serial()), 'time': time.strftime(
                        '%b-%d-%Y_%H%M%S', time.localtime())}
                    results = upload_files('{}newRecording{}'.format(
                        config.OUTPUT_PATH, get_serial()), file_meta_data)
                    print('File uploaded ID: {}'.format(results.get('id')))
                    logging.info(
                        'Files uploaded ID: {}'.format(results.get('id')))

            except Exception as e:
                print(e)
                logging.debug(e)

            if config.TEST_MODE == 1:
                logging.info(
                    'testing!!! please set testMode to 0 in configuration file for full mode...')
                break
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            capture.release()
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
    generate_map()


if __name__ == "__main__":
    main()
