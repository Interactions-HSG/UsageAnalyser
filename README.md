# Usage analyzer
Occupancy and usage monitor for a defined area of interest in Python using openCV. 

## Dependencies

for macos:
(Use requirement.txt to install updated list)

- google-api-python-client==1.7.11
- google-auth==1.10.0
- google-auth-httplib2==0.0.3
- google-auth-oauthlib==0.4.1
- httplib2==0.17.0
- imutils==0.5.3
- matplotlib==3.1.2
- numpy==1.18.1
- oauthlib==3.1.0
- opencv-contrib-python==4.1.1.26
- opencv-python==4.1.1.26
- PyQt5==5.12.3
- pytest==5.3.2
- QtPy==1.9.0
- zipp==0.6.0

for Raspberry PI:

(Execute the below mentioned commands)

First install python3 and check the accessibility then using pip3 or pip,

pip3 install opencv-python

sudo apt-get install libjasper-dev

sudo apt-get install libqt4-test

sudo apt-get install libatlas-base-dev

pip install opencv-contrib-python==4.1.0.25

pip install imutils

pip install --upgrade httplib2==0.15.0

pip install --upgrade google-api-python-client

pip install google-auth-oauthlib

pip3 install pyqrcode

pip3 install pypng


sudo apt-get install python3-flask




Make sure you have created a google project and added the credentials.json file in the root folder of the project to recieve files in your Google Drive 

To receive the files on google drive please change the config.py as

GOOGLE_DRIVE_UPLOAD_ALLOWED = 1

or in case of saving these results offline 

GOOGLE_DRIVE_UPLOAD_ALLOWED = 0