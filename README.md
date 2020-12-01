# Usage analyzer
Occupancy and usage monitor for a defined area of interest in Python using openCV. 

## Dependencies

 MacOS:

    pip install -r requirements-mac.txt

RaspberryPI OS:

    sh requirements-pi-aptget.sh

## Connect Google Drive
Make sure you have created a google project and added the credentials.json file in the root folder of the project to recieve files in your Google Drive 

To receive the files on google drive please change the config.py as

GOOGLE_DRIVE_UPLOAD_ALLOWED = 1

or in case of saving these results offline 

GOOGLE_DRIVE_UPLOAD_ALLOWED = 0

## Start the Analyzer

   ### Activate the environment
    source UsageAnalyzer/usageAnalyzerEnv/bin/activate
 
   ### Run the program
    python LOUsageMapGenerator.py
 