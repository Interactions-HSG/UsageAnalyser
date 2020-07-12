#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

export DISPLAY=:0.0
cd /
cd home/pi/UsageAnalyser
python3 LOUsageMapGenerator.py -d 4 & 


