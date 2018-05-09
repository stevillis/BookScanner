#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
# export PATH=/home/pi/.local/lib/python3.5/site-packages/pyudev/


cd /
cd home/pi/ProjetoScanner/boot
sudo python3 checkusb.py
cd /
