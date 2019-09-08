#!/bin/sh
pip3 install -r $(dirname $0)/requirements
sudo apt-get install libusb-1.0-0-dev portaudio19-dev libasound2-dev
pip3 install $(dirname $0)/wxPython-4.0.6-cp36-cp36m-linux_x86_64.whl